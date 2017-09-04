#!/usr/bin/env python3
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2016, Benjamin P. Trachtenberg"
__credits__ = None
__license__ = 'The MIT License (MIT)'
__status__ = 'prod'
__version_info__ = (1, 0, 1, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'


class BadUniCastIP(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadUniCastIpNetwork(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadMultiCastIpNetwork(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadMultiCastIp(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadBgpCommunity(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadBgpAsNumber(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadEigrpAsNumber(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadVlanNumber(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadDeviceType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SequenceError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidNatType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidNatArguments(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidLeGeType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidCidrValue(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidPermitOrDenyType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidMatchOrSetType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidMatchType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidSetType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RequiredEigrpProcessName(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NotNumber(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidSwitchPortType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidInterfaceType(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BgpAsRequiredForMpls(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)