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
# print(name_columns)

# print(columns)
def my_timetable_all(username,arr):
    for el in arr:
        if el[2] == username:
            for i in range(len(name_columns)):
                print(name_columns[i], ' ', el[i+9])
            break

def my_timetable_continue(username,arr):
    for el in arr:
        if el[2] == username:
            print('Дальнейшее расписание: ')
            for i in range(len(name_columns)):
                if name_columns[i] >= time:
                    index = i
                    break
            for i in range(index, len(name_columns)):
                print(name_columns[i], ' ', el[i+9])
            break

def my_timetable_now(username,arr):
    for el in arr:
        if el[2] == username:
            for i in range(len(name_columns)-1):
                if name_columns[i] <= time and name_columns[i+1] > time:
                    print(name_columns[i], ' ', el[i+9])
                    break
            break

def timetable_by_familia(familia,arr):
    for el in arr:
        if el[0] == familia:
            print(el[0],' ', el[1])
            print('Отдел: ', el[5])
            print('Сейчас на точке: ', end = ' ')
            my_timetable_now(el[2], arr)
            my_timetable_continue(el[2],arr)

def timetable_department(name, arr):
    print(name.upper())
    for el in arr:
        if len(el[5].split(',')) > 1:
            a = el[5].split(',')
            if name.lower() in a:
                print((el[0] + ' ' + el[1] + ':').upper())
                print('Сейчас на точке: ', end=' ')
                my_timetable_now(el[2], arr)
                my_timetable_continue(el[2], arr)

