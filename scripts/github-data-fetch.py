import sys
import os
import json
import argparse
import pprint
import time

import httplib2
import requests

from apiclient.discovery import build
from apiclient.errors import HttpError

from oauth2client.client import AccessTokenRefreshError, \
    SignedJwtAssertionCredentials
from oauth2client.file import Storage
from oauth2client.tools import run


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# Read bigquery configuration
try:
    with open(os.path.join(ROOT_DIR, '../config/bigquery.json'), 'r') as f:
        config = json.loads(f.read())

    with open(os.path.join(ROOT_DIR, '../config/bigquery.p12'), 'rb') as f:
        SERVICE_ACCOUNT_KEY = f.read()

    PROJECT_NUMBER = config['PROJECT_NUMBER']
    SERVICE_ACCOUNT_EMAIL = config['SERVICE_ACCOUNT_EMAIL']
except IOError, KeyError:
    sys.stderr.write('Bigquery config goes in config/\n')
    raise


credentials = SignedJwtAssertionCredentials(
    SERVICE_ACCOUNT_EMAIL,
    SERVICE_ACCOUNT_KEY,
    scope='https://www.googleapis.com/auth/bigquery')

http = httplib2.Http()
http = credentials.authorize(http)

bigquery_service = build('bigquery', 'v2', http=http)


## Queries
SELECT_CLAUSE = """SELECT type AS event_type,
    UPPER(actor_attributes_location) AS location,
    COUNT(*) AS num_events
FROM [publicdata:samples.github_timeline]"""

WHERE_CLAUSE = """WHERE actor_attributes_location IS NOT NULL
    AND actor_attributes_location != ''"""

GROUPBY_CLAUSE = "GROUP BY event_type, location"
ORDERBY_CLAUSE = "ORDER BY num_events DESC"

REPOSITORY_QUERY = "%s %s AND repository_url = '{0}' %s %s" %(
        SELECT_CLAUSE, WHERE_CLAUSE, GROUPBY_CLAUSE, ORDERBY_CLAUSE
    )
LANGUAGE_QUERY = "%s %s AND repository_language = '{0}' %s %s" %(
        SELECT_CLAUSE, WHERE_CLAUSE, GROUPBY_CLAUSE, ORDERBY_CLAUSE
    )
ALL_LANGUAGE_QUERY = "%s %s %s %s" %(
        SELECT_CLAUSE, WHERE_CLAUSE, GROUPBY_CLAUSE, ORDERBY_CLAUSE
    )

ALL_LOCATION_QUERY = """SELECT UPPER(actor_attributes_location) AS location
FROM [publicdata:samples.github_timeline]
GROUP BY location
ORDER BY location"""


NOMINATIM_URL = 'http://nominatim.openstreetmap.org/search'
TIMEOUT = 30    # seconds

try:
    with open(os.path.join(ROOT_DIR, '../www/data/locations.json'), 'r') as f:
        LOCATIONS = json.loads(f.read())
except IOError:
    LOCATIONS = []


# Copyright (c) OpenStreetMap Contributors
def nominatim(location):
    """
    Returns a lat/lng pair for a location or None

    This should be called no more than once per sec
    """

    args = {
        'q': location,
        'format': 'json',
        'limit': '1',
        'addressdetails': '1',
    }

    try:
        resp = requests.get(NOMINATIM_URL, params=args, timeout=TIMEOUT)
    except Exception:
        return None

    if resp.ok:
        try:
            data = resp.json()
        except Exception:
            return None

        if len(data) > 0 and data[0].get('lat') is not None and data[0].get('lon') is not None:
            return (float(data[0].get('lat')), float(data[0].get('lon')))

    return None

def geocode(location):
    """
    Returns a lat/lng pair for a location or None
    """

    return nominatim(location)

def query(sql):
    try:
        request = bigquery_service.jobs()
        query_data = {
            'query': sql,
            'maxResults': 100000
        }

        response = request.query(projectId=PROJECT_NUMBER,
                                body=query_data).execute()

        for row in response['rows']:
            data = {}
            for t in zip(response['schema']['fields'], row['f']):
                if t[0]['type'] == 'INTEGER' and t[1]['v'] is not None:
                    data[t[0]['name']] = int(t[1]['v'])
                elif t[1]['v'] is not None:
                    data[t[0]['name']] = t[1]['v'].strip()
                else:
                    data[t[0]['name']] = t[1]['v']
            yield data
    except HttpError as err:
        sys.stderr.write('Error: {0}'.format(pprint.pformat(err.content)))

    except AccessTokenRefreshError:
        sys.stderr.write("Credentials have been revoked or expired, please "
            "re-run the application to re-authorize")

def groupby_location(data):
    grouper = {}
    for d in data:
        if d['location'] not in grouper:
            grouper[d['location']] = {'name': d['location']}
        grouper[d['location']][d['event_type']] = d['num_events']

    out = grouper.values()
    for d in out:
        if d['name'] in LOCATIONS:
            d['lat'] = LOCATIONS[d['name']]['lat']
            d['lng'] = LOCATIONS[d['name']]['lng']
        else:
            d['lat'] = None
            d['lng'] = None

    return out

def fetch_geocodes(data):
    for d in data:
        if d['location'] in LOCATIONS:
            d['lat'] = LOCATIONS[d['location']]['lat']
            d['lng'] = LOCATIONS[d['location']]['lng']
            continue

        t = geocode(d['location'])
        if t is not None:
            d['lat'] = t[0]
            d['lng'] = t[1]
        time.sleep(1)

    out = {}
    for d in data:
        out[d['location']] = {
            'name': d['location'],
            'lat': d.get('lat'),
            'lng': d.get('lng'),
        }
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data aggregator')
    parser.add_argument('--repo', metavar='REPO_URL', dest='repo_url',
                       help='Fetch data for a particular repository')
    parser.add_argument('--language', metavar='LANG', dest='language',
                       help='Fetch data for a particular language')
    parser.add_argument('--locations', action='store_true',
                       help='Fetch and geocode locations')
    parser.add_argument('--outfile', '-o', metavar='OUTFILE', dest='outfile',
                       help='Write output to a file [stdout]')
    args = parser.parse_args()

    if args.repo_url:
        data = groupby_location(list(query(REPOSITORY_QUERY.format(args.repo_url))))
    elif args.language:
        data = groupby_location(list(query(LANGUAGE_QUERY.format(args.language))))
    elif args.locations:
        data = fetch_geocodes(list(query(ALL_LOCATION_QUERY)))
    else:
        data = groupby_location(list(query(ALL_LANGUAGE_QUERY)))

    out = json.dumps(data, indent=1)
    if args.outfile:
        with open(args.outfile, 'w') as f:
            f.write(out)
    else:
        sys.stdout.write('{0}\n'.format(out))
