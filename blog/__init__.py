VERSION = (0, 6, 5, 'beta', 0)

def get_version():
    from django.utils.version import get_version
    return get_version(VERSION)