#----
import os
import aiosqlite
import sqlite3
#----

#-----Использование базы log_admin------------
#
#
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # <- src/
DB_name_2 = os.path.join(BASE_DIR, "log_admin.db") # <--- Использованная база для записи логов действий администрации через меню администрации
DB_name = os.path.join(BASE_DIR, "users.db") # <--- Использованная база для просмотра юзеров и админского функционала
#
#

#------------------------------------------------------------------------------------------#
#Запись действия администратора через инициализацию базы данных "admin_logs" и последующая запись
#------------------------------------------------------------------------------------------#
#Работа с базой "admin_logs"
#------------------------------------------------------------------------------------------#
async def log_admins_logs():
    async with aiosqlite.connect(DB_name_2) as db:
        query = (
            "CREATE TABLE IF NOT EXISTS admins_logs ("
            "admin_id INT, "
            "action TEXT,"
            "Time timestamp DEFAULT CURRENT_TIMESTAMP )"
        )
        await db.execute(query)
        await db.commit()

async def see_admins_logs():
    async with aiosqlite.connect(DB_name_2) as db:
        async with db.execute("SELECT * FROM admins_logs;") as cursor:
            result = await cursor.fetchall()
            if not result:
                return None
            return result

async def do_admins_logs(admin_id: int, action: str):
    async with aiosqlite.connect(DB_name_2) as db:
        await db.execute(
            "INSERT INTO admins_logs (admin_id, action) VALUES (?, ?)",
            (admin_id, action)
        )
        await db.commit()

# ------------------------------------------------------------------------------------------#
# Статистика админского окна после команды /get_menu_with_things
# ------------------------------------------------------------------------------------------#
async def get_stats_last_join():
    async with aiosqlite.connect(DB_name) as db:
        async with db.execute("SELECT joinAT FROM users ORDER BY joinAT DESC LIMIT 1;") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None
# Время последней регистрации

async def get_stats_user_count():
    async with aiosqlite.connect(DB_name) as db:
        async with db.execute("SELECT COUNT(user_id) FROM users;") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None
# Количество пользователей (всех) из базы данных

async def get_stats_user_top_language():
    async with aiosqlite.connect(DB_name) as db:
        async with db.execute(
                "SELECT language, COUNT(*) as total FROM users GROUP BY language ORDER BY total DESC LIMIT 1;") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None
# Получение ТОП популярного языка в БД

#------------------------------------------------------------------------------------------#
#Удаление пользователя из базы данных + проверки
#------------------------------------------------------------------------------------------#
async def check_delete(user_id: int):
    async with aiosqlite.connect(DB_name) as db:
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            if not result:
                return None
            return result

async def delete_user(user_id: int):
    async with aiosqlite.connect(DB_name) as db:
        await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        await db.commit()
#------------------------------------------------------------------------------------------#
#
#------------------------------------------------------------------------------------------#
