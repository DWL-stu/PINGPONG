from tkinter import *
import sys
sys.path.append('..')
import config_set as config
import main
import json
# handler_value_list_tmp = []
# payload_value_list_tmp = []
# payload_usage_value_list_tmp = []
def load_all_config():
    local_var = globals()
    for con in main.get_all_keys():
        data = main.get_value(con)
        local_var[f'{con}'] = data
def load_list(key_list, value_list, GUI_window, name ,type='checkbutton'):
    exec(f'{name}_value_list_tmp = {value_list}', globals())
    if type == 'checkbutton':
        for use in key_list:
            exec(f'{name}_value_list_tmp.append(StringVar())')
            exec(f"b = Checkbutton(GUI_window, text=use, font=('Time', 10),variable={name}_value_list_tmp[-1])")
            exec(f'b.focus_get()')
            location = key_list.index(use)
            exec(f'value = {name}_value_list_tmp[location]')
            exec(f'{name}_value_list_tmp[-1].set(value)')
            exec('b.pack(anchor=W)')
    elif type == 'entry':
        for use in key_list:
            exec(f'{name}_value_list_tmp.append(StringVar())')
            location = key_list.index(use)
            exec(f"value = {name}_value_list_tmp[location]")
            exec(f'{name}_value_list_tmp[-1].set(value)')
            exec(f"en = Entry(GUI_window, textvariable={name}_value_list_tmp[-1])")
            exec('en.focus_get()')
            text = Label(GUI_window,text=use, font=('Times', 10))
            text.pack(anchor=W)
            exec('en.pack(anchor=W)')
def turn_list_to_dict(key_list, value_list, name, iskey=True):
    sub_dict = {}
    value_list = value_list[int(len(value_list) / 2) : len(value_list)]
    if iskey:
        for key in key_list:
            location = key_list.index(key)
            value = value_list[location].get()
            sub_dict[key] = value
        dict = {name: sub_dict} 
        return dict
    else:
        for key in key_list:
            location = key_list.index(key)
            value = value_list[location].get()
            sub_dict[key] = value
        return sub_dict
def settings_GUI_INIT():
    global handler_settings_key
    handler_settings_key = list(handler.keys())
    global handler_settings_value
    handler_settings_value = list(handler.values())
    global payload_settings_key
    payload_settings_key = list(payload.keys())
    payload_settings_key.remove("usage")
    payload_settings_usage = list(payload.values()).pop(len(list(payload.values())) - 1)
    global payload_settings_value
    payload_settings_value = list(payload.values())
    payload_settings_value.pop(len(payload_settings_value) - 1)
    global payload_settings_usage_key
    payload_settings_usage_key = list(payload_settings_usage.keys())
    global payload_settings_usage_value
    payload_settings_usage_value = list(payload_settings_usage.values())
    del payload_settings_usage
    GUI_window = Tk()
    config.config_load()
    def generate():
        def load(name):
            exec(f'alllist = {name}_value_list_tmp', globals())
            return alllist
        handler_settings_value_new = load('handler')
        payload_settings_value_new = load('payload')
        payload_settings_usage_value_new = load('payload_usage')
        handler_dict = turn_list_to_dict(handler_settings_key, handler_settings_value_new, 'handler')
        payload_dict = turn_list_to_dict(payload_settings_key, payload_settings_value_new, 'payload', False)
        payload_usage_dict = turn_list_to_dict(payload_settings_usage_key, payload_settings_usage_value_new, '', False)
        payload_dict['usage'] = payload_usage_dict
        handler_dict['payload'] = payload_dict
        with open('./config/config.json', 'w', encoding='utf-8') as con:
            json.dump(handler_dict, con)
        GUI_window.quit()
    GUI_window.title("Settings GUI tool") 
    GUI_window.geometry('1068x681+10+10')
    GUI_window.iconbitmap('./config/icon/window_logo.png')
    text=Label(GUI_window,text="PINGPONG settings GUI", font=('Times', 20))
    text.pack()
    button=Button(GUI_window,text="Generate Settings",command=generate)
    button.pack(side='bottom')
    text=Label(GUI_window,text="HANDLER", font=('Times', 15))
    text.pack(anchor=W)
    load_list(handler_settings_key, handler_settings_value, GUI_window ,'handler' ,type='entry')
    p_text=Label(GUI_window,text="PAYLOAD", font=('Times', 15))
    p_text.pack(anchor=W)
    load_list(payload_settings_key, payload_settings_value, GUI_window ,'payload', type='entry')
    ps_text=Label(GUI_window,text="PAYLOAD_USAGE", font=('Times', 13))
    ps_text.pack(anchor=W)
    load_list(payload_settings_usage_key, payload_settings_usage_value, GUI_window, 'payload_usage')
    GUI_window.mainloop()
# load_all_config()
# print(Default_ip)
# print(usage)