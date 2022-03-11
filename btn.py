from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


urlChanel = InlineKeyboardButton('ПОДПИСАТЬСЯ', url='t.me/glamourmusictv')
done = InlineKeyboardButton('ПОДПИСАЛСЯ', callback_data='done')
done_menu = InlineKeyboardMarkup(row_width=1).add(done)
url = InlineKeyboardMarkup(row_width=1).add(urlChanel)


