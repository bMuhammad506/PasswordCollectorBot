from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from callbackdata.callbackd import btn, dlt_btn


def build_keyboard():
    keyboard_inline= InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Save Password", callback_data=btn(data = "savepass").pack()),
    InlineKeyboardButton(text = "Show Password", callback_data=btn(data = "showpass").pack())
    ]
    ],)
    return keyboard_inline

def build_dlt_keyboard(result):
    keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[])
    for r in result:
        button = InlineKeyboardButton(text = f"Delete password {r.site_name}" , callback_data= dlt_btn(data = r.site_name).pack())
        keyboard_inline.inline_keyboard.append([button])
    return keyboard_inline
