# -*- coding:utf-8 -*-
# @FileName  :config_set.py
# @Time      :2023/01/12 16:38:19
# @Author    :D0WE1L1N
import os
import pickle
import main
from random import randint
def load_config_for_main_py(key):
    try:
        value = main.get_value(key)
        return value
    except:
        return None
def set_config_for_main_py(key, value):
    main.set_config(key, value)
def load_modl():
    output = [dI for dI in os.listdir('./PINGPONG_script') if os.path.isdir(os.path.join('./PINGPONG_script',dI))]
    try:
        output.remove('__pycache__')
    except:
        pass
    return output
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
        init_dict = {}
        mods = load_modl()
        for mod in mods:
            scripts = os.listdir(f'PINGPONG_script/{mod}')
            if 'TEMP' in scripts:
                scripts.remove('TEMP')
            if 'SOURCE_FILE' in scripts:
                scripts.remove('SOURCE_FILE')
            if '__pycache__' in scripts:
                scripts.remove('__pycache__')
            for script in scripts:
                script = os.path.splitext(script)[0]
                try:
                    exec(f'import PINGPONG_script.{mod}.{script} as _script', globals())
                    is_open = _script.init_is_open()
                except:
                    is_open = randint(1, 2)
                    if is_open == 1:
                        is_open = True
                    else:
                        is_open = False
                init_dict[script] = is_open
        init = {
            "handler" : {
                'listen_Default_ip' : "127.0.0.1",
                'listen_Default_port' : "624",
                'Autocommand' : ''
            },
            "payload" : {
                'Default_ip' : "127.0.0.1",
                'Default_port' : "624",
                'usage' : init_dict
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