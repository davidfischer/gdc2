from optparse import make_option
import logging
import sys
import time

from django.core.management.base import NoArgsCommand, CommandError

from timeline.models import Location
from timeline.utils import geocode

logger = logging.getLogger(__name__)


class Command(NoArgsCommand):
    help = 'Geocodes github timeline event locations to lat/lng'

    option_list = NoArgsCommand.option_list + (
        make_option('--redo-failed',
            action='store_true',
            dest='redo',
            help='Redo locations that have previously failed geocoding'),
        )

    def handle_noargs(self, **options):
        try:
            self.geocode(redo=options.get('redo', False))
        except Exception:
            logger.exception('Geocoding error')
            raise()

    def geocode(self, redo=False):
        locations = Location.objects.filter(lat=None)

        if not redo:
            locations = locations.filter(is_invalid=False)

        count = locations.count()
        sys.stdout.write('Geocoding {0} locations (1 per second)\n'.format(count))

        for i, loc in enumerate(locations):
            result = geocode(loc)
            if result is not None:
                loc.lat = result[0]
                loc.lng = result[1]
                loc.save()

            sys.stdout.write('\r{0} / {1}'.format(i, count))
            sys.stdout.flush()

            # Nominatim asks that you hit their service not more than 1/s
            time.sleep(1)

        sys.stdout.write('\n')