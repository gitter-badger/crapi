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
import win32serviceutil as w32scu

import crapi.service.Daemon as Daemon


class WindowsDaemon(Daemon.Daemon):

    def _setup(self):
        w32scu.HandleCommandLine(WindowsDaemon)

    def _advance(self):
        return self.srvPipe.read()

    def setup(self):
        self._setup()

    def advance(self):
        return self._advance()
