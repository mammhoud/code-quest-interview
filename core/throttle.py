from ninja_extra.throttling import UserRateThrottle

## DOCS : https://eadwincode.github.io/django-ninja-extra/tutorial/throttling/
"""
This file contains the throttling classes for the API.
it is used to limit the rate of API calls that may be made by a given user.
there are a few classes that are used to limit the rate of API calls.
usage of these classes is optional.
example: # noqa
    `@api.get('/', throttle=[BurstRateThrottle(), ...])` # noqa


"""


class BurstRateThrottle(UserRateThrottle):
    """
    Limits the rate of API calls that may be made by a given user in bursts.
    """
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    """
    Limits the rate of API calls that may be made by a given user over a sustained period.
    """
    scope = 'sustained'

