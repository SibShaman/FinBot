"""Хендлер для обработки суммы входящего дохода"""
from aiogram import types
import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.main_handler import start_handler
from handlers.create_handler import dp, my_command
from db.servce_db import mysql_connect


class FSMAddIncome(StatesGroup):
    """Класс для временного хранилища информации"""
    amount = State()        # amount - сумма которая будет заносится в базу данных
    description = State()   # description - описание
    kind_income = State()   # kind_income - статья доходов
    project = State()       # project - название проекта по которому будет проходить соответствующая сумма
    date_income = State()   # date_income - дата прихода
    date_write = State()    # date_change_income - дата внесения записи (или изменения)


@dp.callback_query_handler(my_command.filter(action='add_income'), state=None)
async def initial_state(call: types.CallbackQuery):
    """ Добавление дохода - начальное состояние"""
    await FSMAddIncome.amount.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('add_income')
    await call.message.edit_text('Введите сумму дохода')


@dp.message_handler(state=FSMAddIncome.amount)
async def add_amount(message: types.Message, state: FSMContext):
    """ Добавление суммы - вводим переключаемся на следующее состояние"""
    async with state.proxy() as data:
        data['amount'] = message.text
    # переключаемся на следующее состояние
    await FSMAddIncome.next()
    await message.answer('Введите описание дохода')


@dp.message_handler(state=FSMAddIncome.description)
async def add_description(message: types.Message, state: FSMContext):
    """ Добавление описания - вводим и переключаемся на следующее состояние"""
    async with state.proxy() as data:
        data['description'] = message.text
    # переключаемся на следующее состояние
    await FSMAddIncome.next()
    markup_kind = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    cursor = mysql_connect.cursor()
    sql_kind = "SELECT tittle FROM kind_income"
    cursor.execute(sql_kind)
    row = (item[0] for item in cursor.fetchall())
    for a in row:
        markup_kind.add(a)
    await message.answer('Выберите вид дохода', reply_markup=markup_kind)


@dp.message_handler(state=FSMAddIncome.kind_income)
async def add_kind_income(message: types.Message, state: FSMContext):
    """ Добавление вида доходов - вводим и переключаемся на следующее состояние"""
    async with state.proxy() as data:
        data['kind_income'] = message.text
    # переключаемся на следующее состояние
    await FSMAddIncome.next()
    markup_project = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    cursor = mysql_connect.cursor()
    sql_project = "SELECT name FROM projects"
    cursor.execute(sql_project)
    # mysql_connect.commit()
    row = (item[0] for item in cursor.fetchall())
    for a in row:
        markup_project.add(a)
    await message.answer('Введите название проекта', reply_markup=markup_project)


@dp.message_handler(state=FSMAddIncome.project)
async def add_name_project(message: types.Message, state: FSMContext):
    """ Добавление названия проекта - вводим переключаемся на следующее состояние"""
    async with state.proxy() as data:
        data['project'] = message.text
    # переключаемся на следующее состояние
    await FSMAddIncome.next()
    await message.answer('Введите дату прихода', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=FSMAddIncome.date_income)
async def add_date_income(message: types.Message, state: FSMContext):
    """ Добавление даты прихода и дату и время записи в БД - вводим и выходим из машины состояний"""
    async with state.proxy() as data:
        data['date_income'] = message.text
    # переключаемся на следующее состояние
    await FSMAddIncome.next()
    # Записываем текущую дату
    async with state.proxy() as data:
        my_date = datetime.datetime.now()
        data['date_write'] = str(my_date)
        # это вставка того что получилось в базу данных
        amount = data['amount']
        description = data['description']
    # Вид дохода и тип проекта стоит корявый, надо проверку добавить и вставлять тот который выбирает user
        # kind_income = data['kind_income']
        # project_id = data['project']
        kind_income = int(1)
        project_id = int(1)
        created_at = data['date_income']
        update_at = data['date_write']

        cursor = mysql_connect.cursor()
        sql = "INSERT INTO income (amount, description, kind_income_id, project_id, created_at, update_at)" \
              "VALUES (%s,%s,%s,%s,%s,%s)"
        t = (amount, description, kind_income, project_id, created_at, update_at)
        cursor.execute(sql, t)
        mysql_connect.commit()
        mysql_connect.close()

        await message.answer('Готово')

    await state.finish()    # выход из машины состояний
    await start_handler(message)    # Возврат меню
