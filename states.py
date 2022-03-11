from aiogram.dispatcher.filters.state import StatesGroup, State

class Media(StatesGroup):
    file_id = State()
    post = State()
    caption = State()
    id = State()

class List(StatesGroup):
    file_id = State()
    list_name = State()


class Video(StatesGroup):
    file_id = State()
   