import gzip
import logging
from cStringIO import StringIO

import requests
import ijson.backends.yajl2 as ijson

logger = logging.getLogger(__name__)


class GithubArchiveParser(object):
    '''
    Fetches and parses data archives from githubarchive.org
    '''

    TIMEOUT = 30
    url_template = 'http://data.githubarchive.org/{0}-{1}-{2}-{3}.json.gz'

    def __init__(self, year, month, day, hour):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour

        self.url = self._normalize_url()

    def _normalize_url(self):
        month = self.month
        if self.month < 10:
            month = '0' + str(month)

        day = self.day
        if self.day < 10:
            day = '0' + str(day)

        return self.url_template.format(self.year, month, day, self.hour)

    def _fetch(self):
        '''
        Fetches a githubarchive.org archive file (.gz) for the given
        year, month, day and hour

        These exceptions are subclasses of RequestException
        @raises requests.exceptions.Timeout on timeout
        @raises requests.exceptions.HTTPError on bad status code response
        '''

        logger.debug('Fetching {0}'.format(self.url))
        resp = requests.get(self.url, timeout=self.TIMEOUT)

        if not resp.ok:
            logger.warn('Failed to fetch {0}. Status: {1}'.format(
                self.url, resp.status_code))
            resp.raise_for_status()
        else:
            logger.debug('Fetched {0} successfully'.format(self.url))

        return resp

    def parse(self):
        '''
        Fetches and parses the appropriate github timeline archive from
        githubarchive.org

        @raises IOError on invalid gzip archive file
        @raises ijson.JSONError on invalid JSON
        '''

        resp = self._fetch()

        # Raises IOError on invalid gzipped file
        opener = gzip.GzipFile(fileobj=StringIO(resp.content))

        # Raises ijson.JSONError on invalid JSON
        for obj in ijson.common.items(ijson.parse(opener, multiple_values=True), ''):
            yield obj
