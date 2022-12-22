from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery


class Filter(BoundFilter):
    key = "callback_data"

    def __init__(self, callback_data):
        self.callback_data = callback_data

    async def check(self, call: CallbackQuery):
        print(call.data)
        print(self.callback_data)
        return call.data in self.callback_data
