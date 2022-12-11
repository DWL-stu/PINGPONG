# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2022/11/07 20:27:59
# @Author    :D0WE1L1N\
import handler
import payload.payload_packer
import config
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
            # payload.payload_packer.pack("_basic_conn.py", ip, port, False)
            payload.payload_packer.pack("PINGPONG_payload/PINGPONG_payload", True, upx_dir)
    if choice == "PING":
        print("PONG")
        sub_main()
    elif choice == "exit":
        print("exiting......")
    elif choice == "reload":
        config.config_load()
        print_normal('Done')
    else:
        print("error:no such choice")
        main()
def main():
    print_normal("Active choice:")
    print_normal("1) Start a PINGPONG handler")
    print_normal("2) Make payload(s)")
    # print_normal("type 'reload' to reload your settings!")
    # print_normal("3) Settings")
    sub_main()
def startserver():
    handler.startserver(True, False, is_input=True)
def config_load_init():
    global _global_dict
    _global_dict = {}
def set_config(key, value):
    _global_dict[key] = value
def get_value(key, defValue=None):
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
if __name__ == "__main__":
    config.config_load()
    print_main()
