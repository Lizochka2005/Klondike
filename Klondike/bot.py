from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, JobQueue
from table import *
from info_psrticipants import *

main_keyboard = [['Мое расписание', 'Расписание других организаторов', 'Информация об участнике']]
                 # ['Подключить напоминания', 'Отключить напоминания']]
my_schedule_keyboard = [['Текущая точка', 'Дальнейшее расписание', 'Все расписание'], ['Назад']]
organizers_schedule_keyboard = [['Расписание всего отдела', 'Расписание конкретного организатора'], ['Назад']]
organizers_info_keyboard = [['По фамилии', 'По нику в ТГ'], ['Назад']]
participant_info_keyboard = [['По фамилии', 'По нику в ТГ', 'По номеру комнаты'], ['Назад']]

reminder_users = []

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
            await update.message.reply_text("Текущая точка:\n" + str(my_timetable_now(username)), reply_markup=ReplyKeyboardMarkup(my_schedule_keyboard, one_time_keyboard=True, resize_keyboard=True))
            context.user_data['state'] = 'schedule_options'

        elif text == 'Дальнейшее расписание':
            await update.message.reply_text(my_timetable_continue(username), reply_markup=ReplyKeyboardMarkup(my_schedule_keyboard, one_time_keyboard=True, resize_keyboard=True))
            context.user_data['state'] = 'schedule_options'

        elif text == 'Все расписание':
            await update.message.reply_text("Полное расписание:\n" + str(my_timetable_all(username)), reply_markup=ReplyKeyboardMarkup(my_schedule_keyboard, one_time_keyboard=True, resize_keyboard=True))
            context.user_data['state'] = 'schedule_options'

        else:
            await update.message.reply_text(
                "Выберите действие:",
                reply_markup=ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True, resize_keyboard=True)
            )
            context.user_data['state'] = None

    # elif text == 'Подключить напоминания':
    #     reminder_users.append(username)
    #     await update.message.reply_text(
    #         "Бот будет напоминать за 10 минут, за 5 минут до точки и в момент начала.")
    #     print(reminder_users)
    #
    # elif text == 'Отключить напоминания':
    #     reminder_users.remove(username)
    #     await update.message.reply_text("Вы отключили напоминания.")

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
                reply_markup=ReplyKeyboardMarkup(organizers_schedule_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True)
            )
            context.user_data['state'] = 'schedule_orginizers_options'

    elif context.user_data.get('state') == 'familia':
        familia = text
        if not timetable_by_familia(familia):
            await update.message.reply_text('Такой фамилии нет в таблице, перепроверь введённые данные!', reply_markup=ReplyKeyboardMarkup(organizers_info_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True))
        else:
            await update.message.reply_text(timetable_by_familia(familia), reply_markup=ReplyKeyboardMarkup(organizers_info_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True))
        context.user_data['state'] = 'orginizers'

    elif context.user_data.get('state') == 'username':
        username = text
        if not timetable_by_username(username):
            await update.message.reply_text('Такого ника нет в таблице, перепроверь введённые данные!', reply_markup=ReplyKeyboardMarkup(organizers_info_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True))
        else:
            await update.message.reply_text(timetable_by_username(username), reply_markup=ReplyKeyboardMarkup(organizers_info_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True))
        context.user_data['state'] = 'orginizers'

    elif context.user_data.get('state') == 'department':
        department = text
        if not timetable_department(department):
            await update.message.reply_text('Такого отдела нет в таблице, перепроверь введённые данные!', reply_markup=ReplyKeyboardMarkup(organizers_schedule_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True))
        else:
            await update.message.reply_text(timetable_department(department), reply_markup=ReplyKeyboardMarkup(organizers_schedule_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True))
        context.user_data['state'] = 'schedule_orginizers_options'

    elif text == 'Информация об участнике':
        await update.message.reply_text(
            "Выберите способ поиска:",
            reply_markup=ReplyKeyboardMarkup(participant_info_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        context.user_data['state'] = 'info_participants_options'

    elif context.user_data.get('state') == 'info_participants_options':
        if text == 'По фамилии':
            await update.message.reply_text('Введите фамилию участника с большой буквы:')
            context.user_data['state'] = 'participant_familia'
        elif text == 'По нику в ТГ':
            await update.message.reply_text('Введите тг ник участника без @: ')
            context.user_data['state'] = 'participant_username'
        elif text == 'По номеру комнаты':
            await update.message.reply_text('Введите номер комнаты: ')
            context.user_data['state'] = 'room_num'
        else:
            await update.message.reply_text(
                "Выберите действие:",
                reply_markup=ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True, resize_keyboard=True)
            )

    elif context.user_data.get('state') == 'participant_familia':
        familia = text
        if not info_by_familia(familia):
            await update.message.reply_text('Такой фамилии нет в таблице, перепроверь введённые данные!',reply_markup=ReplyKeyboardMarkup(participant_info_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True))
        else:
            await update.message.reply_text(info_by_familia(familia), reply_markup=ReplyKeyboardMarkup(participant_info_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True))
        context.user_data['state'] = 'info_participants_options'

    elif context.user_data.get('state') == 'participant_username':
        username = text
        if not info_by_username(username):
            await update.message.reply_text('Такого ника нет в таблице, перепроверь введённые данные!')
            await update.message.reply_text(
                reply_markup=ReplyKeyboardMarkup(participant_info_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True)
            )
        else:
            await update.message.reply_text(info_by_username(username))
            await update.message.reply_text(
                reply_markup=ReplyKeyboardMarkup(participant_info_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True)
            )
        context.user_data['state'] = 'info_participants_options'

    elif context.user_data.get('state') == 'room_num':
        room_num = text
        if info_by_room_num(room_num) == 0:
            await update.message.reply_text('Такого номера комнаты нет в таблице, перепроверь введённые данные!')
            await update.message.reply_text(
                reply_markup=ReplyKeyboardMarkup(participant_info_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True)
            )
        else:
            await update.message.reply_text(info_by_room_num(room_num))
            await update.message.reply_text(
                reply_markup=ReplyKeyboardMarkup(participant_info_keyboard, one_time_keyboard=True,
                                                 resize_keyboard=True)
            )
        context.user_data['state'] = 'info_participants_options'

    elif text == 'Назад':
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
    else:
        await update.message.reply_text("Команда не распознана.")

# async def reminder_job(update: Update, context: CallbackContext) -> None:
#     username = update.message.from_user.username
#     if username in reminder_users:
#         await update.message.reply_text(reminder(username))

if __name__ == '__main__':
    application = ApplicationBuilder().token("7767795518:AAHyp07SVczH6joO3zD2_VbrtRZd24yzlqQ").build()

    job_queue = JobQueue()
    job_queue.set_application(application)

    # job_queue.run_repeating(reminder_job, interval=60)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    job_queue.start()

    application.run_polling()
