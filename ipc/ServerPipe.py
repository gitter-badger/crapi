# Copyright (C) 2014/15 - Iraklis Diakos (hdiakos@outlook.com)
# Pilavidis Kriton (kriton_pilavidis@outlook.com)
# All Rights Reserved.
# You may use, distribute and modify this code under the
# terms of the ASF 2.0 license.
#

"""Part of the ipc module."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
# Python native libraries.
from enum import Enum

import crapi.ipc.Pipe as Pipe
from crapi.ipc.PipeError import PipeError


class ServerPipe(Pipe.Pipe):

    class POLICY(Enum):
        RW = 'rw'
        WR = 'wr'
        RO = 'ro'
        WO = 'wo'

    def _listen(self, policy=POLICY.RW, repeat=True):
        status_code = self.connect()
        if status_code == 0:
            pipe_status, pipe_bytes, pipe_content = self.read()
            self.close()
        else:
            raise PipeError(
                'Pipe encountered an error while attempting a connection!',
                'status_code',
                status_code
            )
        return status_code, pipe_status, pipe_bytes, pipe_content

    def _shutdown(self):
        self.__hPipe.Close()

    def listen(self):
        return self._listen()

    def shutdown(self):
        return self._shutdown()
