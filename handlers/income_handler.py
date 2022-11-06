# amount - сумма которая будет заносится в базу данных
# description - описание
# kind_income - статья доходов
        # 2.1 Учет доходов:
        # - доходы от продажи основных средств
        # - доходы от реализации товара
        # - доходы за оказание услуг
        # - инвестиции
        # - кредититование
        # - аренда(техники, имущества, зданий и сооружений)
        # - формирование дебиторской задолженности(сдача проекта, внесение суммы задолженности, готовность проекта)
        # - прочие
# project - название проекта по которому будет проходить соответствующая сумма
# date_income - дата прихода
# date_change_income - дата внесения записи (или изменения)


from aiogram import types
import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.main_handler import start_handler
from handlers.create_handler import dp, my_command


class FSMAddIncome(StatesGroup):
    """Класс для временного хранилища информации"""
    amount = State()
    description = State()
    kind_income = State()
    project = State()
    date_income = State()
    date_write = State()


@dp.callback_query_handler(my_command.filter(action='add_income'), state=None)
async def initial_state(call: types.CallbackQuery):
    """ Добавление дохода - начальное состояние"""
    await FSMAddIncome.amount.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('add_income')
    await call.message.edit_text('Введите сумму дохода')


@dp.message_handler(state=FSMAddIncome.amount)
async def add_first_name(message: types.Message, state: FSMContext):
    """ Добавление суммы - вводим переключаемся на следующее состояние"""
    async with state.proxy() as data:
        data['amount'] = message.text
    # переключаемся на следующее состояние
    await FSMAddIncome.next()
    await message.answer('Введите описание дохода')


@dp.message_handler(state=FSMAddIncome.description)
async def add_second_name(message: types.Message, state: FSMContext):
    """ Добавление описания - вводим и переключаемся на следующее состояние"""
    async with state.proxy() as data:
        data['description'] = message.text
    # переключаемся на следующее состояние
    await FSMAddIncome.next()
    await message.answer('Введите вид расхода из предложенных')


@dp.message_handler(state=FSMAddIncome.kind_income)
async def add_second_name(message: types.Message, state: FSMContext):
    """ Добавление вида доходов - вводим и переключаемся на следующее состояние"""
    async with state.proxy() as data:
        data['kind_income'] = message.text
    # переключаемся на следующее состояние
    await FSMAddIncome.next()
    await message.answer('Введите название проекта')


@dp.message_handler(state=FSMAddIncome.project)
async def add_second_name(message: types.Message, state: FSMContext):
    """ Добавление названия проекта - вводим переключаемся на следующее состояние"""
    async with state.proxy() as data:
        data['project'] = message.text
    # переключаемся на следующее состояние
    await FSMAddIncome.next()
    await message.answer('Введите дату прихода')


@dp.message_handler(state=FSMAddIncome.date_income)
async def add_second_name(message: types.Message, state: FSMContext):
    """ Добавление даты прихода - вводим переключаемся на следующее состояние"""
    async with state.proxy() as data:
        data['date_income'] = message.text
    # переключаемся на следующее состояние
    await FSMAddIncome.next()
    await message.answer('дата записи вводится автоматически')


@dp.message_handler(state=FSMAddIncome.date_write)
async def add_second_name(message: types.Message, state: FSMContext):
    """ Добавление даты записи - берет автоматом и выходит из машины состояний"""
    async with state.proxy() as data:
        data['date_write'] = datetime.datetime.now()
    await message.answer('Готово')
# передать данные куда то
    await state.finish()
    await start_handler(message)
