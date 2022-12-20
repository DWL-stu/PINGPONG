import sys
sys.path.append("..")
from main import print_normal, print_error, main
def App_send(App, printf, conn):
        try:
            if printf:
                print_normal("PINGPONG>[*]Sending application......")
            conn.send(bytes(App, 'utf8'))
            while True:
                data = conn.recv(1024)
                if data.decode() == "OK":
                    if printf:
                        print_normal("PINGPONG>[*]Application done, everything is OK")
                    return True
                if data.decode() == 'Unfound':
                    print_error("PINGPONG>[-]This payload Doesn't have this usage")
                    return False
        except:
            print_error("PINGPONG>[-]PINGPONG session Died, reason: Connection refused")
            print_normal("handler>[*]Quiting......")
            main()