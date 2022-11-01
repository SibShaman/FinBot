"""Запуск чат бота - точка входа"""
from aiogram import executor, types
from handlers.create_handler import dp, my_command


@dp.message_handler(commands='start')
async def start_handler(message: types.Message):
    """ Запуск бота с инлайн клавиатурой и выбором действия"""
    row_buttons = [
        types.InlineKeyboardButton(
            text='Добавить доход', callback_data=my_command.new(action='add_income')),
        types.InlineKeyboardButton(
            text='Добавить расход', callback_data=my_command.new(action='add_expense')),
        # types.InlineKeyboardButton(
        #     text='Показать всю книгу', callback_data=my_command.new(action='show_contact')),
    ]
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    keyboard_markup.add(*row_buttons)

    await message.answer("Онлайн-Бухгалтер", reply_markup=keyboard_markup)


# старт
def run_bot():
    executor.start_polling(dp, skip_updates=True)
