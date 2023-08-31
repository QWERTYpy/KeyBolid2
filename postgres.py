import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import configparser

# Инициализация основных переменных
config = configparser.ConfigParser()
config.read("postgres.ini", encoding="utf-8")
dict_conf = {}  # Создаем словарь для хранения параметров

# Настройка БД
dict_conf['user'] = config["postgres"]["user"]
dict_conf['password'] = config["postgres"]["password"]
dict_conf['host'] = config["postgres"]["host"]
dict_conf['port'] = config["postgres"]["port"]
dict_conf['database'] = config["postgres"]["database"]


class PostgessBase:
    def __init__(self):
        try:
            # Подключение к существующей базе данных
            self.connection = psycopg2.connect(user=dict_conf['user'],
                                               password=dict_conf['password'],
                                               host=dict_conf['host'],
                                               port=dict_conf['port'],
                                               database=dict_conf['database'])
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
            self.flag_BD = True

        except (Exception, Error) as error:
            self.flag_BD = False
            print("Ошибка при работе с PostgreSQL", error)

    def __del__(self):
        try:
            if self.connection:
                self.cursor.close()
                self.connection.close()
                print("Соединение с PostgreSQL закрыто")
        except (Exception, Error) as error:
            print("Ошибка при открытии", error)

    def search_fio(self, name, firstname, secondname):
        # Поиск в базе данных по ФИО
        insert_query = f"SELECT * FROM staff.person WHERE name ilike '{name}%' AND " \
                       f"firstname ilike '{firstname}%' " \
                       f"AND secondname ilike '{secondname}%' "
        self.cursor.execute(insert_query)
        person_list = []  # Список найденных Персон
        for _ in self.cursor.fetchall():
            insert_query = f"SELECT cardid FROM staff.pass WHERE personid = '{_[0]}' and cardstatus = 1"
            self.cursor.execute(insert_query)
            cardid = self.cursor.fetchall()

            if len(cardid) > 0:
                insert_query = f"SELECT fullcardcode FROM staff.card WHERE cardid = '{cardid[0][0]}'"
                self.cursor.execute(insert_query)
                key = self.cursor.fetchall()
                # Отбрасываем лишние байты
                if key[0][0][:6] == '000000':
                    key = key[0][0]
                else:
                    key = '000000'+key[0][0][6:]
                person_list.append([_[2], _[3], _[4], key, _[5]])  # name, firstname, secondname, key, tableno

        return person_list

    def search_key(self, key):
        # Поиск в базе по ключу
        insert_query = f"SELECT cardid, fullcardcode FROM staff.card WHERE fullcardcode ilike '%{key}%'"
        self.cursor.execute(insert_query)
        query = self.cursor.fetchall()
        list_query = []
        for _query in query:
        # if query:
            cardid = _query[0]
            fullcardcode = '000000'+_query[1][-6:]
            insert_query = f"SELECT personid FROM staff.pass WHERE cardid = '{cardid}' and cardstatus = 1"
            self.cursor.execute(insert_query)
            query = self.cursor.fetchall()
            if query:
                personid = query[0][0]
                insert_query = f"SELECT name, firstname, secondname FROM staff.person WHERE personid = '{personid}'"
                self.cursor.execute(insert_query)
                list_fio = (self.cursor.fetchall())
                if len(list_fio):
                    name, firstname, secondname = list_fio[0]
                    list_query.append([name, firstname, secondname, fullcardcode])
            else:
                list_query.append(['','','',''])
        # else:
        #     return '', '', '', ''
        return list_query

    def search_card(self, key):
        # Поиск статуса карты
        key = key[-6:]  # Берём крайние 6 символов
        # Проверяем совпадение этих 6 символов с конца
        insert_query = f"SELECT cardstatus FROM staff.card WHERE fullcardcode ilike '%{key}' "#and cardstatus = '1'"
        self.cursor.execute(insert_query)
        cardstatus = self.cursor.fetchall()
        if len(cardstatus) == 0:
            return 0
        else:
            return cardstatus[0][0]

    def search_block(self, key):
        # Поиск заблокированного пропуска
        key = key[-6:]  # Берём крайние 6 символов
        # Проверяем совпадение этих 6 символов с конца
        insert_query = f"SELECT blocked FROM staff.card WHERE fullcardcode ilike '%{key}' "  # and cardstatus = '1'"
        self.cursor.execute(insert_query)
        cardblock = self.cursor.fetchall()
        if len(cardblock) == 0:
            return 0
        else:
            return cardblock[0][0]


if __name__ == '__main__':
    bd = PostgessBase()
    print(bd.search_block('000000E10992'))
    # a,b,c,d =bd.search_key('00000073D712')
    # a = bd.search_key('5591')
    # print(a)
    # print(bd.select_date())
    # a = bd.search_fio('бур', '', '')
    # # print(a)
    # for _ in a:
    #     print(_)
    # if bd.flag_BD:
    #     print(bd.search_key('000000822823'))
        # print(bd.search_key('000000C3685B'))
    #     print(bd.search_card('0000003DFAD9'))
