# Copyright (C) 2014/15 - Iraklis Diakos (hdiakos@outlook.com)
# Pilavidis Kriton (kriton_pilavidis@outlook.com)
# All Rights Reserved.
# You may use, distribute and modify this code under the
# terms of the MIT license.
#

"""Part of the service module."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
# Python native libraries.
from abc import ABCMeta
from abc import abstractmethod
import sys

import crapi.ipc.ServerPipe as ServerPipe
from crapi.service.DaemonError import DaemonError
from crapi.service.DaemonTimeoutError import DaemonTimeoutError

# Python 3rd party libraries.
if sys.platform.startswith('win'):
    import win32event as w32ev
    import win32serviceutil as w32scu
    import servicemanager as scm
    __SERVICE_KLASS__ = w32scu.ServiceFramework
else:
    __SERVICE_KLASS__ = object


class Daemon(__SERVICE_KLASS__):

    """A class that enables implementation of Windows/Linxu services."""

    __metaclass__ = ABCMeta

    _svc_name_ = None
    _svc_display_name_ = None
    _svc_description_ = None

    def __init__(self, args, name='crapi',
                 display_name='CRAPI: Common Range API',
                 description='CRAPI service: Brought to you by Kounavi',
                 timeout=0):

        w32scu.ServiceFramework.__init__(self, args)

        self.name = name
        self._svc_name_ = self.name
        self.display_name = display_name
        self._svc_display_name_ = self.display_name
        self.description = description
        self._svc_description_ = description

        if timeout == 0:
            self.__timeout = w32ev.INFINITE
        elif timeout > 30000 and sys.platform.startswith('win'):
            raise DaemonTimeoutError(
                'Windows timeout should adhere to < 30 seconds time limit!',
                'timeout',
                timeout
            )
        else:
            self.__timeout = timeout

        self.__hStop = w32ev.CreateEvent(None, False, False, None)
        self.__hShutdown = w32ev.CreateEvent(None, False, False, None)
        self.__svcPipe = ServerPipe.ServerPipe(name='main')
        self.__event = w32ev.QS_ALLEVENTS

    def SvcDoRun(self):
        scm.LogInfoMsg(self.display_name + ": Starting service...")
        self.run()

    def SvcStop(self):
        scm.LogInfoMsg(self.display_name + ": Stopping service...")
        w32ev.SetEvent(self.hStop)

    def SvcShutdown(self):
        scm.LogInfoMsg(self.display_name + ": Shutting down service...")
        self.__svcPipe.shutdown()
        w32ev.SetEvent(self.hShutdown)

    def run(self):

        self.__hEvents = self.__hStop, self.__hShutdown, self.pipeStream.hEvent
        self.__svcPipe.listen()

        while True:

            rc = w32ev.MsgWaitForMultipleObjects(
                self.__hEvents,
                False,
                self.__timeout,
                self.__event
            )

            if rc == w32ev.WAIT_OBJECT_0:
                scm.LogInfoMsg(
                    self.display_name + ": Received stop event..."
                )
                break
            elif rc == w32ev.WAIT_OBJECT_0+1:
                scm.LogInfoMsg(
                    self.display_name + ": Received shutdown event..."
                )
            elif rc == w32ev.WAIT_OBJECT_0+2:
                scm.LogInfoMsg(self.display_name + ": Received pipe event...")

                    #scm.LogInfoMsg(
                    #    self._svc_display_name_
                    #    + ": Pipe content: " + self.pipeContent
                    #)

                    #scm.LogErrorMsg(
                    #    self._svc_display_name_
                    #    + ": Pipe Error (status code): " + statusCode
                    #)

            elif rc == w32ev.WAIT_OBJECT_0+len(self.hEvents):
                scm.LogInfoMsg(self.display_name + ": All events...")
            elif rc == w32ev.WAIT_TIMEOUT:
                scm.LogInfoMsg(
                    self.display_name + ": Event timeout expired..."
                )
            else:
                raise RuntimeError("What is this? Quack quack!")

        self.__svcPipe.close()
        scm.LogInfoMsg(self.display_name + ": Exiting service...")

    #@abstractmethod
    #def start(self):
    #    raise NotImplementedError(
    #        "Unimplemented client function! Please override it!"
    #    )

    #@abstractmethod
    #def stop(self):
    #    raise NotImplementedError(
    #        "Unimplemented client function! Please override it!"
    #    )

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def advance(self):
        pass
