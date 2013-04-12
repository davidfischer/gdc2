from core import *

try:
    from localsettings import *
except ImportError:
    msg = 'No settings/localsettings.py found! See localsettings_sample.py.'
    raise Exception(msg)
