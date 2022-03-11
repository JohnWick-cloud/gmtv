import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from database import Sqlite
import cfg
from states import Media, List, Video
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from btn import done_menu, url
import requests
from aiogram.utils.markdown import hlink

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
auidio_id = {}
list_count = 1
db = Sqlite('id.db')

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, для доступа подпишитесь на канал', reply_markup=url)
    await message.answer('Затем нажмите на кнопку', reply_markup=done_menu)
    global msg_arg
    msg_arg = message.get_args()
    global us_id
    us_id = message.from_user.id




@dp.callback_query_handler(lambda c: c.data ==  'done')
async def done(call: types.CallbackQuery):
    user_channel_status = await bot.get_chat_member(chat_id='@glamourmusictv', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        
        if db.get_all_id(msg_arg):
            for v in db.get_id(msg_arg):
                requests.post(
            url=f'https://api.telegram.org/bot{cfg.TOKEN}/forwardMessage',
            data={f'chat_id': {call.from_user.id}, 'from_chat_id': {cfg.CHANELID}, 'message_id': {v[0]}}
            ).json()
        
        elif msg_arg == '':
            chanel_ = InlineKeyboardButton("САЙТ", url='https://gmtv.fun')
            chanel_menu = InlineKeyboardMarkup(row_width=1).add(chanel_)
            await bot.send_message(chat_id=us_id, text='Перейдите на сайт для выбора', reply_markup=chanel_menu)

        else:
            requests.post(
        url=f'https://api.telegram.org/bot{cfg.TOKEN}/forwardMessage',
        data={f'chat_id': {call.from_user.id}, 'from_chat_id': {cfg.CHANELID}, 'message_id': {msg_arg}}
            ).json()
        
    else:
        await bot.answer_callback_query(callback_query_id=call.id,text='Для доступа подпишитесь на канал',show_alert=True)

@dp.message_handler(commands='addmusic')
async def add(message: types.Message):
    if message.from_user.id in cfg.ADMIN:
        await message.answer('Отправьте музыку.')
        await Media.file_id.set()

@dp.message_handler(content_types= 'audio', state = Media.file_id)
async def get_ad(message: types.Message, state: FSMContext):
    response = requests.post(
        url=f'https://api.telegram.org/bot{cfg.TOKEN}/forwardMessage',
        data={f'chat_id': {cfg.CHANELID}, 'from_chat_id': {message.from_user.id}, 'message_id': {message.message_id}}
    ).json()
    await message.answer(f"https://t.me/glamourmusictv_bot?start={response['result']['message_id']}")
    await state.finish()

@dp.message_handler(commands='listmusic')
async def add(message: types.Message):
   
    if message.from_user.id in cfg.ADMIN:
        await message.answer('Отправьте название плэйлиста(Без пробелов).')
        await List.list_name.set()

@dp.message_handler(content_types= 'text', state = List.list_name)
async def get_list_name(message: types.Message, state: FSMContext):
    await state.update_data(list_name=message.text)
    await message.answer('Отправьте музыку для плэйлиста')
    await List.file_id.set()

@dp.message_handler(content_types= 'audio', state = List.file_id)
async def get_list(message: types.Message, state: FSMContext):
    response = requests.post(
        url=f'https://api.telegram.org/bot{cfg.TOKEN}/forwardMessage',
        data={f'chat_id': {cfg.CHANELID}, 'from_chat_id': {message.from_user.id}, 'message_id': {message.message_id}}
    ).json()
    answ = await state.get_data()
    db.add_id(answ['list_name'],response['result']['message_id'])
    await message.answer(f"https://t.me/glamourmusictv_bot?start={answ['list_name']}")
    await state.finish()
  

@dp.message_handler(commands='addvideo')
async def add(message: types.Message):
    if message.from_user.id in cfg.ADMIN:
        await message.answer('Отправьте видео.')
        await Video.file_id.set()

@dp.message_handler(content_types= 'video', state = Video.file_id)
async def get_list(message: types.Message, state: FSMContext):
    response = requests.post(
        url=f'https://api.telegram.org/bot{cfg.TOKEN}/forwardMessage',
        data={f'chat_id': {cfg.CHANELID}, 'from_chat_id': {message.from_user.id}, 'message_id': {message.message_id}}
    ).json()
    await message.answer(f"https://t.me/glamourmusictv_bot?start={response['result']['message_id']}")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

    


    
