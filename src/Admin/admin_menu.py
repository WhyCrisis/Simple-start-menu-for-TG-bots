#----
from os import getenv
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (Message,CallbackQuery)
from dotenv import load_dotenv
from src.Admin.admin_FSM import Delete
#---
load_dotenv()
_admin = getenv("admin")
auid = int(_admin) if _admin and _admin.isdigit() else None
#---
router = Router()
#----
#Databases
from SQL.admin_SQL import get_stats_last_join, \
    get_stats_user_top_language, \
    get_stats_user_count, log_admins_logs, do_admins_logs, see_admins_logs, check_delete, delete_user

from SQL.start_SQL import get_users_log_start


#----
#Keyboards
from src.Admin.admin_keyboard import fast_admin_things, delete_users, back_to_admin

#----
async def show_admin_menu(message: Message):
    await log_admins_logs()
    users = await get_stats_user_count()
    top = await get_stats_user_top_language()
    last = await get_stats_last_join()

    text = (f''
            f' \n'
            f'-------------------------\n\n\n'
            f'Hi, total count:\n'
            f'Users: <b>{users}</b>\n'
            f'Popular language: <b>{top}</b>\n'
            f'Last registration: <b>{last} GMC +3</b>\n')
    parse_mode = 'HTML'
    reply_markup = fast_admin_things()
    await message.answer(text, parse_mode=parse_mode, reply_markup=reply_markup)

@router.message(Command('admin_menu_'))
async def admin_menu_with_things(message: Message):
    if message.from_user.id == auid:
        await show_admin_menu(message)
    else:
        await message.answer('Denied')



@router.callback_query(F.data == 'check_users')
async def check_users(callback:CallbackQuery):
    if callback.from_user.id != auid:
        await callback.answer('Access denied', show_alert=True)
        return

    await callback.answer()
    users = await get_users_log_start()

    if not users:
        await callback.message.answer('Database is empty!')
        await show_admin_menu(callback.message)
        return


    lines = [
        f"Айди: {user_id} | Язык: {lang} | Штамп: {joinAT}"
        for user_id, lang, joinAT in users
    ]
    text = "Current users:\n\n" + "\n".join(lines)

    await callback.message.answer(text,reply_markup=back_to_admin())

@router.callback_query(F.data == 'show_admin_logs')
async def admins_fast_check(callback: CallbackQuery):
        if callback.from_user.id != auid:
            await callback.answer('Access denied', show_alert=True)
            return

        await callback.answer()
        logs = await see_admins_logs()

        if not logs:
            await callback.message.answer('Database is empty!!')
            await show_admin_menu(callback.message)
            return

        lines = [
            f"Id: {admin_id} | Action: {action} | Stamp: {Time}"
            for admin_id, action, Time in logs
        ]
        text = "Admin logs:\n\n" + "\n".join(lines)

        await callback.message.answer(text, reply_markup=back_to_admin())


#----Удаление пользователя

@router.callback_query(F.data == 'delete_user')
async def delete_user_(callback: CallbackQuery,state: FSMContext):
    if callback.from_user.id != auid:
        await callback.answer('Access denied', show_alert=True)
        return

    await callback.message.delete()
    await callback.answer()
    await state.clear()
    await state.set_state(Delete.user_id)
    await callback.message.answer('Enter the uid of user to delete:', reply_markup=back_to_admin())

@router.message(Delete.user_id)
async def true_user(message: Message, state: FSMContext):

    if not message.text or not message.text.isdigit():
        await message.answer('Enter the valid uid to delete!', reply_markup=back_to_admin())
        return

    user_id = int(message.text)
    verification = await check_delete(user_id)

    if verification is None:
        await message.answer('UID is not valid or user does not exist', reply_markup=back_to_admin())
        return

    else:
        text=(f'{user_id} is valid! \nPlease confirm manually to delete the user -> {user_id} data')
        await message.answer(text=text, reply_markup=delete_users())
        await state.update_data(user_id=user_id)

@router.callback_query(F.data == 'drop_user')
async def drop_user(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != auid:
        await callback.answer('Access denied', show_alert=True)
        return

    await callback.answer()
    await callback.message.delete()
    #------
    user_data = await state.get_data()
    user_id = user_data.get('user_id')
    #------
    admin_id = callback.from_user.id
    action = f'User drop! {user_id}'
    #------
    await delete_user(user_id)
    await do_admins_logs(admin_id, action)

    await callback.answer('Deleted! This action is in log now!')
    await show_admin_menu(callback.message)