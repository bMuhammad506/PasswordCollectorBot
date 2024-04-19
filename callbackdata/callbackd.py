from aiogram.filters.callback_data import CallbackData

class btn(CallbackData , prefix="mine"):
    data : str

class dlt_btn(CallbackData, prefix="dlt"):
    data : str