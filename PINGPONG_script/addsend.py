# -*- coding:utf-8 -*-
# @FileName  :addsend.py
# @Time      :2023/01/12 16:38:33
# @Author    :D0WE1L1N
import sys
sys.path.append("..")
import main, config_set
def App_send(App, printf, conn, addr, my_addr):
    try:
        if printf:
            main.print_normal("PINGPONG>[*]Sending application......")
        conn.send(bytes(App, 'utf8'))
        data = conn.recv(1024)
        if data.decode() == "OK":
            if printf:
                main.print_normal("PINGPONG>[*]Application done, everything is OK")
            return True
        if data.decode() == 'Unfound':
            main.print_error("PINGPONG>[-]This payload Doesn't have this usage")
            return False
    except:
        main.print_error("PINGPONG>[-]PINGPONG session Died, reason: Connection refused")
        connection_pool = main.get_value('connect_pool')
        connection_pool.remove([conn, my_addr[0], my_addr[1], addr[0], int(addr[1]), 'PINGPONG session'])
        main.print_normal("handler>[*]Quiting......")
        main.main()