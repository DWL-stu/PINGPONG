import os
import shutil
import time
import sys
import traceback
from pathlib import Path
sys.path.append("..")
from main import print_good, print_normal
import PINGPONG_script.addsend as addsend
global is_open
is_open = True
def Upload(ip, file_dir, to_dir, printf, APP_SEND, conn, sendobj, addr, my_addr):
    try:
        if APP_SEND:
            IS_C =  sendobj.App_send("UPLOAD_APP", False, conn, adder, my_addr)
        else:
            IS_C = True
        if IS_C:
            if printf:
                print_normal("PINGPONG>[*]Sending dir......")
            conn.send(bytes(to_dir, "utf8"))
            path = "temp"
            if os.path.exists(path):
                shutil.rmtree(path)
            if not os.path.exists(path):
                os.makedirs(path)
            if printf:
                print_normal("PINGPONG>[*]Copy to file to " + path + "......")
            #判断是否为文件/文件夹
            if not os.path.isfile(file_dir):
                try:
                    file_names = os.listdir(file_dir)
                    # dir_list = Path(file_dir)
                    # dirs = [e for e in dir_list.iterdir() if e.is_dir()]
                    # for dir in dirs:
                    #     file_names = file_names_l.remove(str(dir))
                    # for dir in dirs:
                    #     na = dir.resolve()
                    #     start = str(na).rindex('/')
                    #     name = str(na)[start+1:]
                    #     file_names.remove(name)
                except:
                    print(traceback.print_exc())
                    ch = input("PINGPONG>[-]The location is NOT valuable, again?[y/n]>")
                    if ch == "y" or ch == "yes" or ch == "YES" or ch == "Y":
                        file_dir = input("PINGPONG>[*]Please input the location of the file in your host>")
                        to_dir = input("PINGPONG>[*]Please input the location of the file where you uploaded>")
                        Upload(ip, file_dir, to_dir, printf, APP_SEND, conn, sendobj)
                    else:
                        return True
                for fi in os.listdir(file_dir):
                    if not os.path.isdir(fi):
                        full_file_name = os.path.join(file_dir, fi)
                        if os.path.isfile(full_file_name):
                            shutil.copy(full_file_name, path)
                for file in file_names:
                    if not os.path.isdir(file):
                        old_n = os.path.join(path, file)
                        new_name = file + ".txt"
                        os.rename(old_n, new_name)
                        with open(new_name, "rb") as f:
                            se_data = f.read()
                            conn.send(bytes(new_name, "utf8"))
                            name_data = conn.recv(1024)
                            while True:
                                time.sleep(1)
                                if name_data:
                                    break
                            len_data = len(se_data)
                            conn.send(bytes(str(len_data), "utf8"))
                            len_recv = conn.recv(1024)
                            while True:
                                time.sleep(1)
                                if len_recv:
                                    break
                            conn.sendall(se_data)
                            upload_data = conn.recv(1024)
                            while True:
                                time.sleep(1)
                                if upload_data.decode() != 'Unfound':
                                    print_normal(ip + ">[*]File Upload Succeed: " + old_n + " >>> " + to_dir + "/" + file)
                                    break
                            f.close()
                            try:
                                os.remove(new_name)
                            except:
                                pass
            else:
                file = file_dir[file_dir.rindex('/') + 1:len(file_dir)]
                try:
                    shutil.copy(file_dir, path)
                except:
                    ch = input("PINGPONG>[-]The location is NOT valuable, again?[y/n]>")
                    if ch == "y" or ch == "yes" or ch == "YES" or ch == "Y":
                        file_dir = input("PINGPONG>[*]Please input the location of the file in your host>")
                        to_dir = input("PINGPONG>[*]Please input the location of the file where you uploaded>")
                        Upload(ip, file_dir, to_dir, printf, APP_SEND, conn, sendobj)
                old_n = os.path.join(path, file)
                new_name = file + ".txt"
                os.rename(old_n, new_name)
                file_name = file_dir.split(".txt")[0]
                file_names =  file_name[file_name.rindex('/') + 1:len(file_name)]
                if printf:
                    print_normal("PINGPONG>[*]Sending file......")
                f = open(file_names + ".txt", "rb")    
                se_data = f.read()
                conn.send(bytes(new_name, "utf8"))
                name_data = conn.recv(1024)
                while True:
                    time.sleep(1)
                    if name_data:
                        break
                len_data = len(se_data)
                conn.send(bytes(str(len_data), "utf8"))
                len_recv = conn.recv(1024)
                while True:
                    time.sleep(1)
                    if len_recv:
                        break
                conn.sendall(se_data)
                upload_data = conn.recv(1024)
                while True:
                    time.sleep(1)
                    if upload_data:
                        print_normal(ip + ">[*]File Upload Succeed: " + old_n + " >>> " + to_dir + "/" + file)
                        break
                f.close()
                try:
                    os.remove(new_name)
                except:
                    pass
        # for check_d in file_names:
        #     if os.path.isdir(check_d):
        #         Upload(os.path.join(file_dir, check_d), os.path.join(to_dir, check_d), False, False)
        conn.send(bytes("END", 'utf8'))
        print_good("PINGPONG>[+]FILE UPLOAD DONE")
    except Exception as e:
        print(traceback.print_exc())
        restart = input("PINGPONG>[-]Something went WRONG, restart?[y/n]")
        if restart == "y" or restart == "yes" or restart == "YES" or restart == "Y":
            file_dir = input("PINGPONG>[*]Please input the location of the file in your host>")
            to_dir = input("PINGPONG>[*]Please input the location of the file where you uploaded>")
            Upload(ip, file_dir, to_dir, printf, APP_SEND, conn, sendobj)
        else:
            return True
    finally:
        shutil.rmtree(path)
def run(conn, addr, my_addr):
    if addsend.App_send('UPLOAD_APP', False, conn, addr, my_addr):
        file_dir = input("PINGPONG>[*]Please input the location of the file in your host>")
        to_dir = input("PINGPONG>[*]Please input the location of the file where you uploaded>")
        Upload(addr[0], file_dir, to_dir, True, True, conn, addsend, addr, my_addr)
