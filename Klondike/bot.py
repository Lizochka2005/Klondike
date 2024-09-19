from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

main_keyboard = [['Мое расписание', 'Расписание других организаторов', 'Информация об участнике']]
my_schedule_keyboard = [['Нынешняя точка', 'Полное расписание', 'Мое дальнейшее расписание'], ['Назад']]
organizers_schedule_keyboard = [['Расписание всего отдела', 'Расписание конкретного организатора'], ['Назад']]
participant_info_keyboard = [['По фамилии', 'По нику в ТГ', 'По номеру комнаты'], ['Назад']]


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Чинааазес, сюдаааа:",
        reply_markup=ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )


async def message_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    if text == 'Мое расписание':
        await update.message.reply_text("Введите фамилию с большой буквы:")
        context.user_data['state'] = 'my_schedule_waiting_surname'

    elif text == 'Расписание других организаторов':
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=ReplyKeyboardMarkup(organizers_schedule_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )

    elif text == 'Информация об участнике':
        await update.message.reply_text(
            "Выберите способ поиска:",
            reply_markup=ReplyKeyboardMarkup(participant_info_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )

    elif text == 'Нынешняя точка':
        await update.message.reply_text("Текущая точка.")

    elif text == 'Полное расписание':
        await update.message.reply_text("Полное расписание.")

    elif text == 'Мое дальнейшее расписание':
        await update.message.reply_text("Дальнейшее расписание.")

    elif text == 'Расписание всего отдела':
        await update.message.reply_text("Введите название отдела:")
        context.user_data['state'] = 'department_schedule_waiting_name'

    elif text == 'Расписание конкретного организатора':
        await update.message.reply_text("Введите фамилию организатора с большой буквы:")
        context.user_data['state'] = 'organizer_schedule_waiting_surname'

    elif text == 'По фамилии':
        await update.message.reply_text("Введите фамилию с большой буквы:")
        context.user_data['state'] = 'participant_info_waiting_surname'

    elif text == 'По нику в ТГ':
        await update.message.reply_text("Введите Telegram ник:")
        context.user_data['state'] = 'participant_info_waiting_nickname'

    elif text == 'По номеру комнаты':
        await update.message.reply_text("Введите номер комнаты:")
        context.user_data['state'] = 'participant_info_waiting_room'

    elif text == 'Назад':
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )

    else:
        state = context.user_data.get('state')
        if state == 'my_schedule_waiting_surname':
            await update.message.reply_text(f"Ваше расписание для фамилии {text}: [здесь будет информация]")
            context.user_data['state'] = None
        elif state == 'department_schedule_waiting_name':
            await update.message.reply_text(f"Расписание для отдела {text}: [здесь будет информация]")
            context.user_data['state'] = None
        elif state == 'organizer_schedule_waiting_surname':
            await update.message.reply_text(f"Расписание для организатора {text}: [здесь будет информация]")
            context.user_data['state'] = None
        elif state == 'participant_info_waiting_surname':
            await update.message.reply_text(f"Информация об участнике {text}: [здесь будет информация]")
            context.user_data['state'] = None
        elif state == 'participant_info_waiting_nickname':
            await update.message.reply_text(f"Информация об участнике {text}: [здесь будет информация]")
            context.user_data['state'] = None
        elif state == 'participant_info_waiting_room':
            await update.message.reply_text(
                f"Информация об участнике {text}: [здесь будет информация]")
            context.user_data['state'] = None
        else:
            await update.message.reply_text("Команда не распознана.")


if __name__ == '__main__':
    application = ApplicationBuilder().token("7767795518:AAHyp07SVczH6joO3zD2_VbrtRZd24yzlqQ").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    application.run_polling()
