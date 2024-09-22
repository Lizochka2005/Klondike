from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, JobQueue
from datetime import datetime, timedelta
import asyncio
from table import *


main_keyboard = [['Мое расписание', 'Расписание других организаторов', 'Информация об участнике'],
                 ['Подключить напоминания', 'Отключить напоминания']]
my_schedule_keyboard = [['Текущая точка', 'Дальнейшее расписание', 'Все расписание'], ['Назад']]
organizers_schedule_keyboard = [['Расписание всего отдела', 'Расписание конкретного организатора'], ['Назад']]
organizers_info_keyboard = [['По фамилии', 'По нику в ТГ'], ['Назад']]
participant_info_keyboard = [['По фамилии', 'По нику в ТГ', 'По номеру комнаты'], ['Назад']]

reminder_users = set()


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Мяу:",
        reply_markup=ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )


async def message_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    username = update.message.from_user.username

    if text == 'Мое расписание':
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=ReplyKeyboardMarkup(my_schedule_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        context.user_data['state'] = 'schedule_options'

    elif context.user_data.get('state') == 'schedule_options':
        if text == 'Текущая точка':
            await update.message.reply_text("Текущая точка:\n" + str(my_timetable_now(username)))

        elif text == 'Дальнейшее расписание':
            await update.message.reply_text(my_timetable_continue(username))

        elif text == 'Все расписание':
            await update.message.reply_text("Полное расписание:\n" + str(my_timetable_all(username)))

        else:
            await update.message.reply_text(
                "Выберите действие:",
                reply_markup=ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True, resize_keyboard=True)
            )
            context.user_data['state'] = None

    elif text == 'Подключить напоминания':
        reminder_users.add(username)
        await update.message.reply_text(
            "Бот будет напоминать за 10 минут до точки и в момент начала.")

    elif text == 'Отключить напоминания':
        reminder_users.discard(username)
        await update.message.reply_text("Вы отключили напоминания.")

    elif text == 'Расписание других организаторов':
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=ReplyKeyboardMarkup(organizers_schedule_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        context.user_data['state'] = 'schedule_orginizers_options'

    elif context.user_data.get('state') == 'schedule_orginizers_options':
        if text == 'Расписание всего отдела':
            await update.message.reply_text('Введите название отдела: ')
            context.user_data['state'] = 'department'

        elif text == 'Расписание конкретного организатора':
            await update.message.reply_text(
                "Выберите действие:",
                reply_markup=ReplyKeyboardMarkup(organizers_info_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True)
            )
            context.user_data['state'] = 'orginizers'

        else:
            await update.message.reply_text(
                "Выберите действие:",
                reply_markup=ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True, resize_keyboard=True)
            )
            context.user_data['state'] = None

    elif context.user_data.get('state') == 'orginizers':
        if text == 'По фамилии':
            await update.message.reply_text('Введите фамилию организатора с большой буквы:')
            context.user_data['state'] = 'familia'

        elif text == 'По нику в ТГ':
            await update.message.reply_text('Введите тг ник организатора без @: ')
            context.user_data['state'] = 'username'

        else:
            await update.message.reply_text(
                "Выберите действие:",
                reply_markup=ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True, resize_keyboard=True)
            )
            context.user_data['state'] = None

    elif context.user_data.get('state') == 'familia':
        familia = text
        await update.message.reply_text(timetable_by_familia(familia))

    elif context.user_data.get('state') == 'username':
        username = text
        await update.message.reply_text(timetable_by_username(username))

    elif context.user_data.get('state') == 'department':
        department = text
        await update.message.reply_text(timetable_department(department))

    elif text == 'Информация об участнике':
        await update.message.reply_text(
            "Выберите способ поиска:",
            reply_markup=ReplyKeyboardMarkup(participant_info_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )

    elif text == 'Назад':
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
    else:
        await update.message.reply_text("Команда не распознана.")


async def reminder_job(context: CallbackContext) -> None:
    current_time = datetime.now()
    pass


if __name__ == '__main__':
    application = ApplicationBuilder().token("7767795518:AAHyp07SVczH6joO3zD2_VbrtRZd24yzlqQ").build()

    job_queue = JobQueue()
    job_queue.set_application(application)

    job_queue.run_repeating(reminder_job, interval=60, first=10)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    job_queue.start()

    application.run_polling()
