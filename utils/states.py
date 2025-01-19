from aiogram.fsm.state import StatesGroup, State


class AdminHandler(StatesGroup):
    start = State()


class AddMovie(StatesGroup):
    name = State()
    code = State()
    language = State()
    quality = State()
    movie = State()


class AddSponsor(StatesGroup):
    name = State()
    link = State()
    member = State()


class DelMovie(StatesGroup):
    name = State()
    

class DelSponsor(StatesGroup):
    name = State()


class SendAd(StatesGroup):
    ad = State()
    check = State()