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
# Python native libraries.
import sys
import platform

import crapi.messaging.MessageEnvelope as MessageEnvelope

# Python 3rd party libraries.
if sys.platform.startswith('win'):
    import win32com.client


class MessageQueue(object):

    def __init__(self, name='Message-Broker-Queue'):
        self.__hostname = platform.uname()[1]
        self.__name = name
        self.__queue_t = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
        self.__queue_t.FormatName = ("direct=os:" + self.__hostname
                                     + "\\PRIVATE$\\" + self.__name)

    def dispatch(self, msg=None):
        if msg is None:
            msg = MessageEnvelope.MessageEnvelope()
        message = win32com.client.Dispatch("MSMQ.MSMQMessage")
        message.Label = msg.header
        message.Body = msg.payload
        self.__queue = self.__queue_t.Open(2, 0)
        message.Send(self.__queue)
        self.__queue.Close()

    def fetch(self):
        self.__queue = self.__queue_t.Open(1, 0)
        message = self.__queue.Receive()
        self.__queue.Close()
        return MessageEnvelope.MessageEnvelope(message.Label, message.Body)

    @property
    def name(self):
        return self.__name
