# -*- coding:utf-8 -*-
# @FileName  :listpid.py
# @Time      :2023/01/29 20:43:21
# @Author    :D0WE1L1N
from sys import path as _envir_path
_envir_path.append('..')
from main import *
import PINGPONG_script.addsend as send
def init_is_open():
    return True
def run(conn, addr, myaddr):
    if send.App_send('LISTPID_APP', False, conn, addr, myaddr):
        conn.send(b'OK')
        len_pid = int(conn.recv(1024).decode('utf8'))
        conn.send(b'OK')
        print('----------pid----------name----------')
        for i in range(1, len_pid):
            pid = conn.recv(1024).decode('utf8')
            conn.send(b'OK')
            name = conn.recv(1024).decode('utf8')
            conn.send(b'OK')
            print_normal(f'          {pid}          {name}          ')
            