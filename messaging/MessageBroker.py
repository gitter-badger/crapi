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

import crapi.messaging.MessageQueue as MessageQueue
import crapi.messaging.MessageEnvelope as MessageEnvelope


class MessageBroker(object):

    def __init__(self, name=None):
        if name is None:
            self.queue = MessageQueue.MessageQueue()
        else:
            self.queue = MessageQueue.MessageQueue(name.lower())

    def dispatch(self, header='CRAPI Message Broker: Header label',
                 payload='CRAPI Message Broker: Message body.',
                 envelope=None):

        if envelope is None:
            msg = MessageEnvelope.MessageEnvelope(header, payload)
        else:
            msg = envelope
        if sys.platform.startswith('win'):
            self.queue.dispatch(msg)

    def fetch(self):
        if sys.platform.startswith('win'):
            return self.queue.fetch()
