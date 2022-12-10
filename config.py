import os
import json
import main
def load_conf_dict(dict):
    for key in dict.keys():
        data = dict[f'{key}']
        main.set_config(key, data)
def config_load():
    main.config_load_init()
    if os.path.exists("./config/config.json"):
        # 提取信息
        main.print_normal("settings>[*]load config......")
        with open('./config/config.json', 'r', encoding='utf-8') as conf:
            config = json.loads(conf.read())
            handler_conf = config['handler']
            payload_conf = config['payload']
            load_conf_dict(handler_conf)
            load_conf_dict(payload_conf)
    else:
        #初始化
        if not os.path.exists('./config'):
            os.mkdir('./config')
        main.print_normal("settings>[*]Initializing......")
        init = {
            "handler" : {
                'Default_ip' : "127.0.0.1",
                'Default_port' : "624",
            },
            "payload" : {
                'cmd' : True,
                'upload' : True,
                'cam_shot' : False,
                'priv_vbp_listen' : True 
            }
        }
        try:
            with open("./config/config.json", "w", encoding='utf-8') as fc:
                json.dump(init, fc)
        except IOError as e:
            main.print_error(f"settings>[-]Something Wrong when initializing, print out: {e}")
        else:
            main.print_good("settings>[+]Initializing done, loading the settings")
            config_load()