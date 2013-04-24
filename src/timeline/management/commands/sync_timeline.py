from optparse import make_option
import calendar
import logging
import sys

from django.core.management.base import NoArgsCommand, CommandError
from django.utils.timezone import now
import pytz
from datetime import timedelta

from timeline.models import Actor, Repository, GithubEvent
from timeline.archiveparser import GithubArchiveParser

logger = logging.getLogger(__name__)

MONTHS = range(1, 13)
DAYS = range(1, 32)
HOURS = range(0, 24)


class Command(NoArgsCommand):
    help = 'Syncs github events from githubarchive.org'

    option_list = NoArgsCommand.option_list + (
        make_option('--year',
            dest='year',
            type='int',
            help='Used for importing a single year/month/day/hour [2011,]'),
        ) + (
        make_option('--month',
            dest='month',
            type='int',
            help='Used for importing a single year/month/day/hour [1,12]'),
        ) + (
        make_option('--day',
            dest='day',
            type='int',
            help='Used for importing a single year/month/day/hour [1,31]'),
        ) + (
        make_option('--hour',
            dest='hour',
            type='int',
            help='Used for importing a single year/month/day/hour [0,23]'),
        )

    def handle_noargs(self, **options):
        self.records = 0

        year = options.get('year')
        month = options.get('month')
        day = options.get('day')
        hour = options.get('hour')

        if year or month or day or hour:
            if not year:
                raise CommandError('--year must be specified if month/day/hour specified')
            if month:
                if day:
                    if hour:
                        sys.stdout.write('Processing timeline archives for {0}-{1}-{2}-{3}\n'.format(year, month, day, hour))
                        self.do_hour(year, month, day, hour)
                    else:
                        sys.stdout.write('Processing timeline archives for {0}-{1}-{2}\n'.format(year, month, day))
                        self.do_day(year, month, day)
                else:
                    sys.stdout.write('Processing timeline archives for {0}-{1}\n'.format(year, month))
                    self.do_month(year, month)
            else:
                sys.stdout.write('Processing timeline archives for {0}\n'.format(year))
                self.do_year(year)
        else:
            sys.stdout.write('Processing timeline to current\n')
            self.do_catchup()

        if self.records > 0:
            sys.stdout.write('Saved {0} new records\n'.format(self.records))

    def do_year(self, year):
        if year < 2011 or year > 2020:
            raise CommandError('Invalid time spec: {0}'.format(year))

        for month in MONTHS:
            self.do_month(year, month)

    def do_month(self, year, month):
        if month not in MONTHS:
            raise CommandError('Invalid time spec: {0}-{1}-{2}'.format(year, month))

        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            self.do_day(year, month, day)

    def do_day(self, year, month, day):
        if month not in MONTHS or day not in DAYS:
            raise CommandError('Invalid time spec: {0}-{1}-{2}'.format(year, month, day))

        for hour in HOURS:
            self.do_hour(year, month, day, hour)

    def do_hour(self, year, month, day, hour):
        if month not in MONTHS or day not in DAYS or hour not in HOURS:
            raise CommandError('Invalid time spec: {0}-{1}-{2}-{3}'.format(year, month, day, hour))

        archive = GithubArchiveParser(year, month, day, hour)

        try:
            for record in archive.parse():
                event = GithubEvent.from_archive(record)

                # We keep track of only a subset of events
                # Specifically we aren't looking at gists for example
                if event is not None:
                    self.records += 1
        except Exception:
            logger.exception('Error processing {0}-{1}-{2}-{3}'.format(year, month, day, hour))

    def do_catchup(self):
        # sadly githubarchive uses Pacific time instead of UTC
        # There is a DST bug here during "negative time"
        # See: https://github.com/igrigorik/githubarchive.org/issues/33
        pacific = pytz.timezone('US/Pacific')

        events = GithubEvent.objects.order_by('-created_at').values('created_at')[:1]
        if len(events) > 0:
            # Start processing at the next hour after the latest event
            # Sometimes githubarchive records go into the next hour by a couple mins
            # See: https://github.com/igrigorik/githubarchive.org/issues/23
            last_event = pacific.normalize(events[0]['created_at']) + timedelta(minutes=45)
        else:
            # By default, process the last 90 days
            last_event = pacific.normalize(now()) - timedelta(days=90)

        while last_event < (pacific.normalize(now()) - timedelta(hours=6)):
            self.do_hour(last_event.year, last_event.month, last_event.day, last_event.hour)
            last_event += timedelta(hours=1)
