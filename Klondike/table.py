import pandas as pd
import datetime

dt = datetime.datetime.now()
today = dt.date()
time = dt.time()


df = pd.read_excel(r'C:\Users\Лиза\Downloads\СЕТКА.xlsx', sheet_name = 'Лист1')
n = 115 #количество значимых строк(кол-во оргов + первые 2)

arr = df.to_numpy()
arr = arr[:n-1]
name_columns = arr[0][9::]

def my_timetable_all(username):
    text = ''
    for el in arr:
        if el[2][1::] == username:
            for i in range(len(name_columns)):
                text += str(name_columns[i]) + ' ' + el[i+9] +'\n'
            return text

def my_timetable_continue(username):
    text = ''
    if (today != '2024-10-09' and today != '2024-10-10') or (today == '2024-10-09' and time < datetime.time(9,30,0)):
        text += 'Дальнейшее расписание: \n'
        text += my_timetable_all(username)
        return text
    for el in arr:
        if el[2][1::] == username:
            text += 'Дальнейшее расписание: \n'
            for i in range(len(name_columns)):
                if name_columns[i] >= time:
                    index = i
                    break
            for i in range(index, len(name_columns)):
                text += str(name_columns[i]) + ' ' + el[i+9] +'\n'
            return text

def my_timetable_now(username):
    text = ''
    if (today != '2024-10-09' and today != '2024-10-10') or (today == '2024-10-09' and time < datetime.time(9,30,0)):
        text = 'Посвят ещё не начался!\n'
        return text
    for el in arr:
        if el[2][1::] == username:
            for i in range(len(name_columns)-1):
                if name_columns[i] <= time and name_columns[i+1] > time:
                    text += str(name_columns[i]) + ' ' + el[i+9] +'\n'
                    return text

def timetable_by_familia(familia):
    text = ''
    for el in arr:
        if el[0] == familia:
            text += el[0] + ' ' + el[1] + '\n'
            text += 'Отдел: ' + el[5] + '\n'
            text += 'Сейчас на точке: '
            text += my_timetable_now(el[2][1::])
            text += my_timetable_continue(el[2][1::])
            return text
    return False

def timetable_by_username(username):
    text = ''
    for el in arr:
        if el[2][1::] == username:
            text += el[0] + ' ' + el[1] + '\n'
            text += 'Отдел: ' + el[5] + '\n'
            text += 'Сейчас на точке: '
            text += my_timetable_now(el[2][1::])
            text += my_timetable_continue(el[2][1::])
            return text
    return False

def timetable_department(name):
    text = str(name).upper() + '\n'
    flag = False
    for el in arr:
        a = el[5].split(', ')
        if str(name).lower() in a:
             flag = True
             text += (el[0] + ' ' + el[1] + ': ').upper()
             text += str(my_timetable_now(el[2][1::]))
    if flag:
        return text
    return False


