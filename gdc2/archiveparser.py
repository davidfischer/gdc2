import gzip
import json
import logging


logger = logging.getLogger(__name__)


class GitHubArchiveParser(object):
    """
    Parses gzipped archive files from githubarchive.org
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def _flatten(self, data):
        """
        Flattens a dictionary containing other dictionaries

        See: https://gist.github.com/igrigorik/2426614

        Note: currently ignores array types (eg. "shas")
        """

        out = {}

        for key in data:
            if isinstance(data[key], dict):
                d = self._flatten(data[key])
                for k in d:
                    out[key + "_" + k] = d[k]
            elif not isinstance(data[key], list) and data[key] is not None:
                out[key] = data[key]

        return out


    def parse(self):
        """
        Parses the githubarchive file

        @raises IOError on invalid gzip archive file
        """

        with open(self.filepath, 'r') as f:
            # Assumes one JSON object per line which isn't true of older
            # githubarchive.org JSON files
            for i, line in enumerate(gzip.GzipFile(fileobj=f)):
                # There are occasionally records with invalid utf-8
                # See: https://github.com/igrigorik/githubarchive.org/issues/25
                line = line.decode('utf-8', 'ignore')
                try:
                    yield self._flatten(json.loads(line))
                except ValueError:
                    logger.exception('JSON parse error on line: {0}'.format(i))
