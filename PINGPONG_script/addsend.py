import sys
sys.path.append("..")
import main
def App_send(App, printf, conn):
        try:
            if printf:
                print("PINGPONG>[*]Sending application......")
            conn.send(bytes(App, 'utf8'))
            while True:
                data = conn.recv(1024)
                if data.decode() == "OK":
                    if printf:
                        print("PINGPONG>[*]Application done, everything is OK")
                    return True
        except:
            print("PINGPONG>[-]PINGPONG session Died, reason: Connection refused")
            print("handler>[*]Back to main console......")
            main.main()