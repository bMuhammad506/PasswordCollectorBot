from aiogram import types, Router, F
from keyboards.keyboards import build_keyboard, build_dlt_keyboard
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup
from aiogram.filters import Command
from main import InputState
from db.model import Passwords, session
from aiogram.fsm.context import FSMContext
from callbackdata.callbackd import btn, dlt_btn
from aiogram.methods import GetChat

router = Router()
inline_keyboard = build_keyboard()



@router.message(Command("start"))
async def st_funct(message: types.message, state:FSMContext):
    await message.reply(f"Hello! I'm your bot.", reply_markup = inline_keyboard)

@router.message(InputState.waiting_for_name)
async def wait_fr_name(message: types.message, state: FSMContext):
    await state.update_data(site_name = message.text)
    await state.set_state(InputState.waiting_for_pass)
    await message.answer("Please enter the pasword for this:", reply_markup=ReplyKeyboardMarkup(remove_keyboard=True,keyboard=[]))

@router.message(InputState.waiting_for_pass)
async def wait_fr_pass(message: types.message, state: FSMContext):
    await state.update_data(site_pass = message.text)
    data = await state.get_data()
    new_pass = Passwords(site_name = data["site_name"], site_pass = data["site_pass"])
    try:
        session.add(new_pass)
        session.commit()
        await message.reply(text ="Password Saved",reply_markup = inline_keyboard)
    except:
        session.rollback()
        await message.reply(text ="You already have a password for this site delete that first",reply_markup = inline_keyboard)

@router.message(InputState.print_pass_key)
async def show_pass_key(message: types.message, state: FSMContext):
    text_1=""
    try:
        results = session.query(Passwords).all()
        inline_keyboard_dlt = build_dlt_keyboard(results)
        for r in results:
            text_1 += f"Your password for "+ r.site_name +" is : " + r.site_pass + "\n"
        await message.edit_text(text=text_1, reply_markup=inline_keyboard_dlt)
    except:
        text_1="No passwords to show"
        await message.edit_text(text=text_1, reply_markup=inline_keyboard)

@router.callback_query(btn.filter(F.data=="showpass"))
async def show_pass(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(InputState.print_pass_key)
    await show_pass_key(call.message, state)

@router.callback_query(btn.filter(F.data=="savepass"))
async def save_pass(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(InputState.waiting_for_name)
    await call.message.answer("Please enter the site you want to save your pasword for:", reply_markup=ReplyKeyboardMarkup(remove_keyboard=True,keyboard=[]))

@router.callback_query(dlt_btn.filter())
async def dlt_pass(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data_list = call.data.split(":")
    site_name = data_list[1]
    session.query(Passwords).filter(Passwords.site_name == site_name).delete()
    session.commit()
    await state.set_state(InputState.print_pass_key)
    await show_pass_key(call.message, state)