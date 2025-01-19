import aiosqlite


class Database:
    def __init__(self, db_name: str = "./data/database.db"):
        self.db_name = db_name
    
    async def initialize(self):
    
        async with aiosqlite.connect(self.db_name) as db:
            # Таблица пользователей
            await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID
                user_id INTEGER NOT NULL UNIQUE, -- ID пользователя
                language TEXT DEFAULT 'uz' -- Предпочитаемый язык пользователя, по умолчанию 'ru'
            )
            """)

            # Таблица фильмов
            await db.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный ID фильма
                name TEXT NOT NULL, -- Название фильма
                code TEXT NOT NULL, -- Код для доступа к фильму
                language TEXT, -- Языки фильма 
                quality TEXT, -- Качество фильма
                message_id INTEGER UNIQUE NOT NULL  -- ID сообщения фильма
            )
            """)

            # Таблица каналов
            await db.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный ID канала
                name TEXT NOT NULL, -- Название канала
                link TEXT NOT NULL, -- Ссылка на канал
                member INTEGER -- id Канала -100351353
            )
            """)

            # Сохранение изменений
            await db.commit()

    # User
    # check user
    async def user_exists(self, user_id):
        async with aiosqlite.connect(self.db_name) as conn:
            async with conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)) as cursor:
                result = await cursor.fetchone()
                return bool(result)
            
    # add user    
    async def add_user(self, user_id, lang ="uz"):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('INSERT INTO users (user_id, language) VALUES (?, ?)', (user_id, lang))
            await conn.commit()
            
    # get lang user
    async def get_lang(self, user_id):
        async with aiosqlite.connect(self.db_name) as conn:
            async with conn.execute('SELECT language FROM users WHERE user_id = ?', (user_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else None
            
    async def set_lang(self, user_id, lang):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('UPDATE users SET language = ? WHERE user_id = ?', (lang, user_id))
            await conn.commit()
            
    async def send_movie(self, code, lang):
        async with aiosqlite.connect(self.db_name) as conn:
            async with conn.execute('SELECT name, quality, message_id FROM movies WHERE code = ? AND language = ?', (code, lang)) as cursor:
                result = await cursor.fetchall()
                return result
            
    async def get_sponsors(self):
        async with aiosqlite.connect(self.db_name) as conn:
            async with conn.execute('SELECT name, link, member FROM channels') as cursor:
                result = await cursor.fetchall()
                return result
            
    async def get_users(self):
        async with aiosqlite.connect(self.db_name) as conn:
            async with conn.execute('SELECT user_id FROM users') as cursor:
                result = await cursor.fetchall()
                return result

    # Admin
    # movie data
    async def get_movie_data(self, code):
        async with aiosqlite.connect(self.db_name) as conn:
            async with conn.execute("""SELECT name,
                                    code,
                                    language,
                                    quality
                                    FROM movies WHERE code = ?""", 
                                    (code,)) as cursor:
                result = await cursor.fetchall()
                return result 

    async def get_movies(self):
        async with aiosqlite.connect(self.db_name) as conn:
            async with conn.execute("SELECT name, code FROM movies") as cursor:
                result = await cursor.fetchall()
                return result

    # add movie            
    async def add_movie(self, name, code, lang, qual, mess_id):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute("""INSERT INTO movies (name, 
                               code, 
                               language, 
                               quality, 
                               message_id
                               ) VALUES (?, ?, ?, ?, ?)""", 
                               (name, code, lang, qual, mess_id))
            await conn.commit()

    async def add_sponsor(self, name, link, member):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute("INSERT INTO channels (name, link, member) VALUES (?, ?, ?)", (name, link, member))
            await conn.commit()

    async def del_movie(self, code):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute("DELETE FROM movies WHERE code = ?", (code,))
            await conn.commit()
            
    async def del_sponsor(self, name):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute("DELETE FROM channels WHERE name = ?", (name,))
            await conn.commit()
