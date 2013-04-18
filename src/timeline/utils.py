import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

try:
    USER_AGENT = settings.ADMINS[0][1]
except IndexError:
    USER_AGENT = 'github-data-challenge'

NOMINATIM_URL = 'http://nominatim.openstreetmap.org/search'
TIMEOUT = 30    # seconds

def nominatim(location):
    """
    Returns a lat/lng pair for a location or None
    """

    args = {
        'q': location,
        'format': 'json',
        'limit': '1',
    }
    headers = {'User-Agent': USER_AGENT}

    try:
        resp = requests.get(NOMINATIM_URL, params=args, headers=headers, timeout=TIMEOUT)
    except Exception:
        logger.error('Request timeout for {0}'.format(location))
        return None

    if resp.ok:
        try:
            data = resp.json()
        except Exception:
            logger.error('JSON decoding failed for {0}'.format(location))
            return None

        if len(data) > 0 and data[0].get('lat') is not None and data[0].get('lon') is not None:
            return (float(data[0].get('lat')), float(data[0].get('lon')))

    return None

def geocode(location):
    """
    Returns a lat/lng pair for a location or None
    """

    return nominatim(location)
