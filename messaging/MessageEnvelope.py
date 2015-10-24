# Copyright (C) 2014/15 - Iraklis Diakos (hdiakos@outlook.com)
# Pilavidis Kriton (kriton_pilavidis@outlook.com)
# All Rights Reserved.
# You may use, distribute and modify this code under the
# terms of the ASF 2.0 license.
#

"""Part of the messaging module."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class MessageEnvelope(object):

    def __init__(self, header, payload):
        self.__header = header
        self.__payload = payload

    @property
    def header(self):
        return self.__header

    @property
    def payload(self):
        return self.__payload

    @header.setter
    def header(self, value):
        self.__header = value

    @payload.setter
    def payload(self, value):
        self.__payload = value

    def __str__(self):
        return 'Label: ' + self.header + '\r\nMessage: ' + self.payload
