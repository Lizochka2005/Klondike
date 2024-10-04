import pandas as pd
import datetime
import math

dt = datetime.datetime.now()
today = dt.date()
time = dt.time()


df = pd.read_excel(r'C:\Users\Лиза\Downloads\СЕТКА.xlsx', sheet_name = 'ЛИЧНЫЕ СЕТКИ')
n = 109 #количество значимых строк(кол-во оргов + первые 2)

arr = df.to_numpy()
name_columns = arr[0][8::]
arr = arr[1:n-1]

def my_timetable_all(username):
    text = ''
    for el in arr:
        if el[1][1::] == username:
            for i in range(len(name_columns)):
                text += str(name_columns[i]) + ' ' + str(el[i+8]) +'\n'
            return text

def my_timetable_continue(username):
    text = ''
    # if (today != '2024-10-09' and today != '2024-10-10') or (today == '2024-10-09' and time < datetime.time(9,30,0)):
    #     text += 'Дальнейшее расписание: \n'
    #     text += my_timetable_all(username)
    #     return text
    for el in arr:
        if el[1][1::] == username:
            text += 'Дальнейшее расписание: \n'
            for i in range(len(name_columns)):
                t = name_columns[i].split('-')[0]
                t = datetime.datetime.strptime(t, '%H:%M').time()
                if t >= time:
                    index = i
                    break
            for i in range(index, len(name_columns)):
                text += str(name_columns[i]) + ' ' + str(el[i+8]) +'\n'
            return text

def my_timetable_now(username):
    text = ''
    # if (today != '2024-10-09' and today != '2024-10-10') or (today == '2024-10-09' and time < datetime.time(9,30,0)):
    #     text = 'Посвят ещё не начался!\n'
    #     return text
    for el in arr:
        if el[1][1::] == username:
            for i in range(len(name_columns)-1):
                start = name_columns[i].split('-')[0]
                start = datetime.datetime.strptime(start, '%H:%M').time()
                end = name_columns[i].split('-')[1]
                end = datetime.datetime.strptime(end, '%H:%M').time()
                if start <= time and end > time:
                    text += str(name_columns[i]) + ' ' + str(el[i+8]) +'\n'
                    return text

def timetable_by_familia(familia):
    text = ''
    for el in arr:
        if familia in el[0].split():
            text += el[0] + '\n'
            text += 'Отдел: ' + str(el[3]) + '\n'
            text += 'Сейчас на точке: '
            text += my_timetable_now(el[1][1::])
            text += my_timetable_continue(el[1][1::])
            return text
    return False

def timetable_by_username(username):
    text = ''
    for el in arr:
        if el[1][1::] == username:
            text += el[0] + '\n'
            text += 'Отдел: ' + str(el[3]) + '\n'
            text += 'Сейчас на точке: '
            text += my_timetable_now(el[1][1::])
            text += my_timetable_continue(el[1][1::])
            return text
    return False

def timetable_department(name):
    text = str(name).upper() + '\n'
    flag = False
    for el in arr:
        a = list(map(lambda x: x.lower(), el[3].split(',')))
        if str(name).lower() in a:
             flag = True
             text += (el[0] + ': ').upper()
             text += str(my_timetable_now(el[1][1::]))
    if flag:
        return text
    return False

# def reminder(username):
#     text = ''
#     for el in arr:
#         if el[1][1::] == username:
#             for i in range(len(name_columns)):
#                 start = name_columns[i].split('-')[0]
#                 start = datetime.datetime.strptime(start, '%H:%M').time()
#                 difference = datetime.timedelta(start).total_seconds()
#                 defference = math.floor(difference/60)
#                 if defference == 10:
#                     text += 'Через 10 минут у тебя запланированно: '
#                     text += str(el[i])
#                 if defference == 5:
#                     text += 'Через 5 минут у тебя запланированно: '
#                     text += str(el[i])
#                 if defference == 0:
#                     text += 'Сейчас у тебя запланированно: '
#                     text += str(el[i])
#     return text