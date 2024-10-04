import telebot
import pandas as pd
from datetime import datetime, timedelta

dt = datetime.now()
today = dt.date()
time = dt.time()


df = pd.read_excel(r'C:\Users\Лиза\Downloads\СЕТКА.xlsx', sheet_name = 'ЛИЧНЫЕ СЕТКИ')
n = 109 #количество значимых строк(кол-во оргов + первые 2)

arr = df.to_numpy()
name_columns = arr[0][8::]
arr = arr[1:n-1]


token = "6621864497:AAHQHmbHAfexHVDm4B0yx2k357mZyzg693M"
bot = telebot.TeleBot(token)

def reminder(username, id):
    text = ''
    for el in arr:
        if el[1][1::] == username:
            for i in range(len(name_columns)):
                start = name_columns[i].split('-')[0]
                start1 = timedelta(hours=int(start.split(':')[0]), minutes=int(start.split(':')[1]))
                now = timedelta(hours=time.hour, minutes=time.minute)
                difference = start1 - now
                if difference == timedelta(hours=0,minutes=10):
                    text += 'Через 10 минут у тебя запланированно: '
                    text += str(el[i+8])
                    bot.send_message(id, text)
                if difference == timedelta(hours=0,minutes=5):
                    text += 'Через 5 минут у тебя запланированно: '
                    text += str(el[i+8])
                    bot.send_message(id, text)
                if difference == timedelta(hours=0,minutes=0):
                    text += 'Сейчас у тебя запланированно: '
                    text += str(el[i+8])
                    bot.send_message(id, text)