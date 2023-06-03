import psycopg2
from collections import namedtuple
from datetime import datetime


class DataBase:
    __DB_TUPLE = namedtuple('DB_Selector', ['id', 'nickname', 'age', 'email', 'password', 'avatar'])

    def __init__(self, **adress):
        self.__database = adress['database']
        self.__user = adress['user']
        self.__password = adress['password']
        self.__host = adress['host']
        self.__port = adress['port']
        self.__info = {
            'database': self.__database,
            'user': self.__user,
            'password': self.__password,
            'host': self.__host,
            'port': self.__port
        }
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(**self.__info)

    def close_connection(self):
        self.connection.close()

    def insert_data(self, nickname: str, age: int, email: str, password: str):
        cursor = self.connection.cursor()
        try:
            with cursor as cur:
                cur.execute(
                    '''INSERT INTO users (nickname, age, email, "password") 
                       VALUES (%s, %s, %s, %s)''',
                    (nickname, age, email, password)
                )
                print('Data successfully uploaded')
                self.connection.commit()
                return True
        except Exception:
            raise

    def get_user_by_id(self, user_id: int) -> namedtuple:
        cursor = self.connection.cursor()
        with cursor as cur:
            cur.execute(
                '''SELECT * FROM users WHERE id = %s''', (user_id,)
            )
            res = cur.fetchone()
            if not res:
                print('There is no such user...')
                return False
            return self.__DB_TUPLE(*res)

    def get_user_by_email(self, email: str):
        cursor = self.connection.cursor()
        with cursor as cur:
            cur.execute(
                '''select * from users where email = %s ''', (email,)
            )
            res = cur.fetchone()
            if not res:
                print('There is no such user...', end='\n\n')
                return None
            return self.__DB_TUPLE(*res)

    def get_user_posts(self, user_id: int):
        cursor = self.connection.cursor()
        with cursor as cur:
            cur.execute(
                '''select * from posts where creator_id = %s order by date_and_time desc''', (user_id,)
            )
            res = cur.fetchall()
            if not res:
                return False
            return res

    def upload_post(self, user_id: int, post: str):
        cursor = self.connection.cursor()
        try:
            with cursor as cur:
                cur.execute(
                    '''insert into posts (post_text, creator_id, date_and_time) values (%s, %s, %s)''',
                    (post, user_id, datetime.strftime(datetime.today(), '%d/%m/%Y, %H:%M:%S'))
                )
                self.connection.commit()
                print('Post uploaded')
                return True
        except Exception:
            raise

    def delete_post(self, post_id):
        cursor = self.connection.cursor()
        try:
            with cursor as cur:
                cur.execute(
                    '''delete from posts where post_id = %s''', (post_id,)
                )
            self.connection.commit()
            print(f'Post with id = {post_id} deleted successfully')
            return 'Post deleted'
        except Exception:
            raise

    def get_all_posts(self):
        cursor = self.connection.cursor()
        with cursor as cur:
            cur.execute(
                '''select * from posts order by date_and_time desc'''
            )
            res = list(map(list, cur.fetchall()))
            for post in res:
                user = self.get_user_by_id(int(post[2]))
                formatted_time = datetime.strftime(post[3], '%d/%m/%Y %H:%M:%S')
                post[2] = user.nickname if user else None
                post[3] = formatted_time
        return res

    def update_avatar(self, user_id: int, avatar: bytes):
        cursor = self.connection.cursor()
        try:
            with cursor as cur:
                cur.execute(
                    '''update users set avatar = %s where id=%s''', (avatar, user_id)
                )
                self.connection.commit()
            return 'Uploaded'
        except Exception:
            raise

    def update_nick(self, user_id: int, new_data:  str) -> str:
        cursor = self.connection.cursor()
        with cursor as cur:
            try:
                cur.execute(
                    f'''update users set nickname = %(data)s where id = %(id)s''',
                    {'data': new_data, 'id': user_id}
                )
                self.connection.commit()
                print('Data has been successfully uploaded')
                return 'Uploaded'
            except psycopg2.Error:
                print('Error occured')
                return 'Something went wrong'

#  Функция для обновления данных о пользователе: ава, ник, пароль.
