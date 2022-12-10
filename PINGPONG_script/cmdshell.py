# -*- coding:utf-8 -*-
# @FileName  :cmdshell.py
# @Time      :2022/11/08 18:19:18
# @Author    :D0WE1L1N
# CMDshell库：定义了一个开启cmd远程命令的函数
import socket
import sys
sys.path.append("..")
import random
from main import print_good, print_normal, print_error
try:
    import handler
    import main
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
            print_error("handler>[-]port input error")
    try:
        cmd_session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cmd_session.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cmd_session.bind((ip, port))
        cmd_session.listen(10)
    except socket.error as msg:
        print_error("handler>[-]something went WRONG, print out the wrong msg: " + str(msg))
        sys.exit(1)
    while True:
        cmd_SessObj,addr = cmd_session.accept()
        _ip = addr[0]
        _port = addr[1]
        print_normal("CMD_SHELL>[*]CMD session Created:" + ip + ":" + str(port) + " >>> " + _ip + ":" + str(_port))
        while True:
            try:
                cmd_command = input("CMD_SHELL>")
                cmd_SessObj.send(bytes(cmd_command, 'utf8'))
                if cmd_command == "exit" or cmd_command == "EXIT":
                    print("CMD_SHELL>[*]exiting......")
                    main_port = random.randint(9000, 10000)
                    cmd_SessObj.send(bytes(str(main_port), 'utf8'))
                    handler.startserver(False, False, ip=ip, port=main_port)
                CMD_re = cmd_SessObj.recv(1024)
                try:
                    print(str(ip) + ">"+ CMD_re.decode('utf-8'))
                except:
                    print(str(ip) + ">" + CMD_re.decode('gbk'))
            except:
                print_error("CMD_SHELL>[-]CMD session Died, reason: Connection refused")
                print_normal("handler>[*]Back to main console......")
                main.main()
        cmd_SessObj.close()
        break
    cmd_session.close()
