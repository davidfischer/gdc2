import json
import sys
import time

import requests
import unicodecsv


NOMINATIM_URL = 'http://nominatim.openstreetmap.org/search'
TIMEOUT = 30 # seconds

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

    headers = {'User-Agent': 'gdc2 geocoder -- REPLACE WITH YOUR EMAIL'}

    try:
        resp = requests.get(NOMINATIM_URL, params=args, headers=headers, timeout=TIMEOUT)
    except Exception:
        return None

    if resp.ok:
        try:
            return resp.json()
        except Exception:
            pass

    return None

def geocode(location):
    """
    Returns a lat/lng pair for a location or None
    """

    return nominatim(location)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('USAGE: python gdc2/geocoder.py locations.csv')
        sys.exit(1)

    locations = []
    OUTFILE = 'www/data/locations.json'
    try:
        with open(OUTFILE, 'r') as f:
            outs = json.loads(f.read())
        print "Found %s with %d / %d geocoded locations" %(OUTFILE, len([k for k in outs if outs[k] is not None]), len(outs.keys()))
    except Exception:
        outs = {}

    with open(sys.argv[1]) as f:
        reader = unicodecsv.DictReader(f)
        for row in reader:
            line = row['location']
            locations.append(' '.join(line.replace(',', ' ').replace('.', ' ').split()))

    newlocations = [l for l in locations if l not in outs.keys()]
    print "Geocoding %d new locations" %len(newlocations)
    for i, location in enumerate(newlocations):
        # Geocode locations we have not previously geocoded
        if not location in outs or outs[location] is None:
            outs[location] = geocode(location)
            time.sleep(1)   # Nominatim should be called only once per sec

        if i % 10 == 0:
            print " - %d / %d" %(i, len(newlocations))

    with open(OUTFILE, 'w') as f:
        f.write(json.dumps(outs, indent=1))
