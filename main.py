# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2022/11/07 20:27:59
# @Author    :D0WE1L1N
print("Loading the PINGPONG console......")
import handler
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
def sub_main():
    choice = input("choose your choice>")
    if choice == "1":
       startserver()
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
    sub_main()
def startserver():
    ip = input("handler>[*]Please input the IP for the attack machine(blank for 127.0.0.1)>")
    port = input("handler>[*]Please input the PORT(blank for 624)>")
    handler.startserver(ip, port, True)
if __name__ == "__main__":
    main()
