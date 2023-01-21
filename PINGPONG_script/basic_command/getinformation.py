# -*- coding:utf-8 -*-
# @FileName  :getinformation.py
# @Time      :2023/01/12 16:37:53
# @Author    :D0WE1L1N
from sys import path as _envir_path
_envir_path.append('..')
from main import *
import PINGPONG_script.addsend as send
global is_open
is_open = True
def run(conn, addr, my_addr):
    if send.App_send('GETINFO_APP', False, conn, addr, my_addr):
        len_info = conn.recv(1024)
        conn.send(b'OK')
        info = conn.recv(int(len_info))
        try:
            info = info.decode('utf8')
        except:
            info = info.decode('gbk')
        conn.send(b'OK')
        print_normal(f'''PINGPONG>[*]INFO:
{info}
        ''')
        return True
def init_is_open():
    return True