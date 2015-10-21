# Copyright (C) 2014/15 - Iraklis Diakos (hdiakos@outlook.com)
# Pilavidis Kriton (kriton_pilavidis@outlook.com)
# All Rights Reserved.
# You may use, distribute and modify this code under the
# terms of the MIT license.
#

"""Part of the ipc module."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import crapi.ipc.Pipe as Pipe


class ClientPipe(Pipe.Pipe):

    def listen(self):
        raise NotImplementedError(
            'This should only be done from a ServerPipe!'
        )

    def shutdown(self):
        raise NotImplementedError(
            'This should only be done from a ServerPipe!'
        )
