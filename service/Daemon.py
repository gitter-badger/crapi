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
# from operator import itemgetter
from enum import Enum
# Python 3rd party libraries.
#import win32api as w32api
import win32pipe as w32p
import win32file as w32f
import win32event as w32ev
#import win32security as w32sec
#import win32service as w32svc
import win32serviceutil as w32scu
import servicemanager as scm
import pywintypes as w32t


class Daemon(w32scu.ServiceFramework):

    """A class that enables monitoring of VMs for proper configuration."""

    """
        Discovers unused ports and IP address blocks so as to determine proper
        configuration of VM images such as port forwarding rules (template
        stage) and IP address of network adapters (provisioning stage).
    """

    _svc_name_ = "osaum-vmcore"
    _svc_display_name_ = "OS-AUtoMaton VM Core Templating Engine"
    _svc_description_ = "Discovers inactive TCPv4 connections on this local " \
                        "machine (ip, port) for configuration of VM images."

    def __init__(
            self,
            args,
            name='osaum-vmcore',
            display_name='OS-AUtoMaton VM Core Templating Engine',
            description='Discovers inactive TCPv4 connections on this local ' +
                        'machine (ip, port) for configuration of VM images.',
            timeout=w32ev.INFINITE,
            event_type=w32ev.QS_ALLEVENTS
    ):
        w32scu.ServiceFramework.__init__(self, args)
        self.timeout = timeout
        #self.sa = w32sec.SECURITY_ATTRIBUTES()
        #self.sa.bInheritHandle = True
        self.hStop = w32ev.CreateEvent(None, False, False, None)
        self.hShutdown = w32ev.CreateEvent(None, False, False, None)
        self.server_pipe =

    def SvcDoRun(self):
        scm.LogInfoMsg(self._svc_display_name_ + ": Starting service...")
        self.run()

    def SvcStop(self):
        scm.LogInfoMsg(
            self._svc_display_name_ + ": Stopping service..."
        )
        w32ev.SetEvent(self.hStop)

    def SvcShutdown(self):
        scm.LogInfoMsg(self._svc_display_name_ + ": Shutting down service...")
        w32ev.SetEvent(self.hShutdown)

    def listen():
        pass

    def close():
        pass

    #TODO: Provide as override functionality!
    def run(self):

        self.hEvents = self.hStop, self.hShutdown, self.pipeStream.hEvent
        w32p.ConnectNamedPipe(self.hPipe, self.pipeStream)
        while True:

            rc = w32ev.MsgWaitForMultipleObjects(
                self.hEvents,
                False,
                self.timeout,
                self.event
            )

            if rc == w32ev.WAIT_OBJECT_0:
                scm.LogInfoMsg(
                    self._svc_display_name_ + ": Received stop event..."
                )
                break
            elif rc == w32ev.WAIT_OBJECT_0+1:
                scm.LogInfoMsg(
                    self._svc_display_name_ + ": Received shutdown event..."
                )
            elif rc == w32ev.WAIT_OBJECT_0+2:
                scm.LogInfoMsg(self._svc_display_name_ + ": Pipe event...")
                buf_sz = w32f.GetOverlappedResult(
                    self.hPipe, self.pipeStream, True
                )
                self.msg = self.strbuf[:buf_sz]
                statusCode, self.pipeContent = w32f.ReadFile(
                    self.hPipe, self.pipeBuffer, self.pipeStream
                )
                if statusCode == 0:
                    scm.LogInfoMsg(
                        self._svc_display_name_
                        + ": Pipe content: " + self.pipeContent
                    )
                else:
                    scm.LogErrorMsg(
                        self._svc_display_name_
                        + ": Pipe Error (status code): " + statusCode
                    )
            elif rc == w32ev.WAIT_OBJECT_0+len(self.hEvents):
                scm.LogInfoMsg(self._svc_display_name_ + ": All events...")
            elif rc == w32ev.WAIT_TIMEOUT:
                scm.LogInfoMsg(
                    self._svc_display_name_ + ": Event timeout expired..."
                )
            else:
                raise RuntimeError("What is this? Quack quack!")

        w32p.DisconnectNamedPipe(self.hPipe)
        scm.LogInfoMsg(self._svc_display_name_ + ": Exiting...")

    def start(self):
        raise NotImplementedError(
            "Unimplemented client function! Please override it!"
        )

    def stop(self):
        raise NotImplementedError(
            "Unimplemented client function! Please override it!"
        )


#def hRebootFunc(svc_name, *args):
#    scm.LogInfoMsg(svc_name + ": System reboot detected!")
#    return True

if __name__ == "__main__":
    #w32api.SetConsoleCtrlHandler(hRebootFunc, True)
    w32scu.HandleCommandLine(Daemon)
