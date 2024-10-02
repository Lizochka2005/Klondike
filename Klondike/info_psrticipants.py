import pandas as pd
import datetime

dt = datetime.datetime.now()
today = dt.date()
time = dt.time()


df = pd.read_excel(r'C:\Users\Лиза\Downloads\Participants.xlsx', sheet_name = 'result')
n = 352 #количество значимых строк(кол-во участников)

arr = df.to_numpy()
name_columns = df.columns.tolist()[:9]

def info_by_familia(familia):
    text = ''
    # if (today != '2024-10-09' and today != '2024-10-10') or (today == '2024-10-09' and time < datetime.time(9,30,0)):
    #     text = 'Посвят ещё не начался! Пока ты не можешь узнать эти данные:(\n'
    #     return text
    for el in arr:
        if el[0] == familia:
            text += el[0] + ' ' + el[1] + ' ' + el[2] + '\n'
            text += 'telegram: ' + el[3] + '\n'
            text += 'vk: ' + el[4] + '\n'
            text += 'number: ' + str(el[5]) + '\n'
            text += 'room: ' + str(el[8]) + '\n'
            return text
    return False

def info_by_username(username):
    text = ''
    # if (today != '2024-10-09' and today != '2024-10-10') or (today == '2024-10-09' and time < datetime.time(9,30,0)):
    #     text = 'Посвят ещё не начался! Пока ты не можешь узнать эти данные:(\n'
    #     return text
    for el in arr:
        if el[3][1::] == username:
            return info_by_familia(el[0])
    return False

def info_by_room_num(num):
    text = ''
    flag = False
    # if (today != '2024-10-09' and today != '2024-10-10') or (today == '2024-10-09' and time < datetime.time(9, 30, 0)):
    #     text = 'Посвят ещё не начался! Пока ты не можешь узнать эти данные:(\n'
    #     return text
    for el in arr:
        if str(el[8]) == num:
            text += (el[0] + ' ' + el[1] + ' ' + el[2]).upper()
            text += '\ntelegram: ' + el[3] + '\n'
            text += 'vk: ' + el[4] + '\n'
            text += 'number: ' + str(el[5]) + '\n'
            text += 'room: ' + str(el[8]) + '\n\n'
            flag = True
    if flag: return text
    return False