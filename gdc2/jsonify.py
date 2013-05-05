import logging
import json
import sys

import unicodecsv

logger = logging.getLogger(__name__)


try:
    with open('www/data/locations.json', 'r') as f:
        LOCATIONS = json.loads(f.read())
except IOError:
    sys.stderr.write('www/data/locations.json should be there\n')
    sys.exit(1)


def cleanup_location(location):
    return ' '.join(location.replace(',', ' ').replace('.', ' ').split())

def format_repo(repo_url):
    return repo_url.replace('https://github.com/', '')

def location_data(location):
    if location in LOCATIONS and LOCATIONS[location] is not None and len(LOCATIONS[location]) > 0:
        lat = float(LOCATIONS[location][0]['lat'])
        lng = float(LOCATIONS[location][0]['lon'])
        return (lat, lng)
    return None

def main(filepath):
    data = {}

    with open(filepath, 'r') as f:
        reader = unicodecsv.DictReader(f)
        for row in reader:
            loc = cleanup_location(row['actor_attributes_location'])
            lang = row['repository_language']
            url = format_repo(row['repository_url'])
            user = row['actor_attributes_login']

            if loc not in data:
                geo = location_data(loc)
                data[loc] = {
                        'name': loc,
                        'lat': geo[0] if geo is not None else None,
                        'lng': geo[1] if geo is not None else None,
                        'repositories': {},
                        'languages': {},
                        'users': {},
                    }

            if lang not in data[loc]['languages']:
                data[loc]['languages'][lang] = 0
            data[loc]['languages'][lang] += 1

            if user not in data[loc]['users']:
                data[loc]['users'][user] = 0
            data[loc]['users'][user] += 1

            if url not in data[loc]['repositories']:
                data[loc]['repositories'][url] = 0
            data[loc]['repositories'][url] += 1

    output = []
    for loc in data:
        if data[loc]['lat'] is not None and \
            data[loc]['lng'] is not None and \
            len(data[loc]['name']) > 0:

            # Gets the top 3 users for each location
            data[loc]['users'] = [u[0] for u in sorted(data[loc]['users'].items(), lambda x, y: cmp(y[1], x[1]))][:3]
            output.append(data[loc])

    with open('www/data/events.json', 'w') as f:
        f.write(json.dumps(output, indent=1))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("USAGE: jsonify <csvfile>\n")
        sys.exit(1)

    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT)

    main(sys.argv[1])