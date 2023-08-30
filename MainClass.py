# Описание основных классов
import tkinter as tk

# Класс отвечающий за вывод Информационного поля
class InfoFrame:
    def __init__(self, root):
        self.root = root
        self.title_left_down_text = tk.StringVar()
        self.title_left_down_text.set("Добро пожаловать ...")
        self.title_left_down = tk.Label(self.root, anchor="nw", height=1, width=20,
                                        textvariable=self.title_left_down_text, background='white')
        self.title_left_down.place(x=10, y=570)

class InfoFrame2:
    def __init__(self, root):
        self.root = root
        self.title_left_down_text = tk.StringVar()
        self.title_left_down_text.set("Изменений нет.")
        self.title_left_down = tk.Label(self.root, anchor="nw", height=1, width=50,
                                        textvariable=self.title_left_down_text, background='white')
        self.title_left_down.place(x=300, y=570)



# Класс описывающий прибор
class ObjectBolid:
    def __init__(self):
        self.num = 0  # Номер прибора
        self.id = 0  # Возможно потребуется для дублированный адресов
        self.name = ''  # Название
        self.type = 0  # Тип прибора 4/10
        self.ver = ''  # Версия
        self.interface = 0  # 0 Если не нужен паразитный бит, 1 Если нужен
        self.comment = ''  # Комментарий

    def show(self):
        print(self.num, self.id, self.name, self.type, self.ver, self.comment)

# Класс описывающий доступ предоставленный определенному человеку
class Person:
    def __init__(self, name='', surname='', patronymic='', key='', bit=''):
        self.name = name  # Имя
        self.surname = surname  # Фамилия
        self.patronymic = patronymic  # Отчество
        self.key = key  # Ключ
        self.permission = {}  # Права доступа # id_object: [Номер прибора, ХО, Доступ]
        self.bit = bit  # Паразитный бит

    def get_perm_obj(self):  # Получение списка приборов к которым есть доступ у человека
        _list_obj = []
        for _ in self.permission.keys():
            _list_obj.append(self.permission[_][0])
        return (',').join(_list_obj)

    def get_obj(self):
        return [_[0] for _ in self.permission.values()]

    def show(self):
        print(self.name, self.surname, self.patronymic, self.key, self.permission)

    def get_check_10(self, id_object):
        """
        Получение списка флагов для чекбоксов из hex
        :param id_object:
        :return:
        """
        # Получаем hex для данного Объекта
        permission = self.permission[id_object][2]
        # Инициализируем будущий список
        self.chk_list = []
        # Получаем первый байт и преобразуем в двоичный
        bin_perm = bin(int(permission[0:2], 16))
        # Получаем список битов в обратном порядке
        list_bin_perm_A = list(bin_perm[:1:-1])
        # Если длина меньше 8, то добиваем 0
        if len(list_bin_perm_A) < 8:
            for _ in range(8 - len(list_bin_perm_A)):
                list_bin_perm_A.append('0')

        bin_perm = bin(int(permission[2:4], 16))
        list_bin_perm_B = list(bin_perm[:1:-1])
        if len(list_bin_perm_B) < 8:
            for _ in range(8 - len(list_bin_perm_B)):
                list_bin_perm_B.append('0')

        bin_perm = bin(int(permission[4:6], 16))
        list_bin_perm_C = list(bin_perm[:1:-1])
        if len(list_bin_perm_C) < 4:
            for _ in range(4 - len(list_bin_perm_C)):
                list_bin_perm_C.append('0')
        # Составляем итоговый список с флагами
        list_bin_perm = list_bin_perm_A + list_bin_perm_B + list_bin_perm_C
        # Создаем список для чекбокса
        for _ in range(20):
            self.chk_list.append(tk.IntVar(value=list_bin_perm[_]))

        return self.chk_list

    def get_check_4(self, id_object):
        """
        С2000-4
        Получение списка флагов для чекбоксов из hex
        :param id_object:
        :return:
        """
        permission = self.permission[id_object][2]
        self.chk_list = []
        # Сами права находятся во 2 байте
        bin_perm = bin(int(permission[2:4], 16))
        list_bin_perm = list(bin_perm[:1:-1])

        if len(list_bin_perm) < 8:
            for _ in range(8 - len(list_bin_perm)):
                list_bin_perm.append('0')

        for _ in range(8):
            self.chk_list.append(tk.IntVar(value=list_bin_perm[_]))

        return self.chk_list

    def get_perm(self, id):
        """
        С2000-4
        Получение значения ключа ХО или прав доступа
        :param id:
        :return:
        """
        perm = self.permission[id][2][0:2]
        if perm == '10' or perm == '18':
            return tk.IntVar(value=1)
        else:
            return tk.IntVar(value=0)




if __name__ == '__main__':
    per = Person("Иван", "Иванович", "Иванович", "555555555555")
    per.permission = {"021": ["7", "000000", "100000"], "022": ["79", "000000", "100000"], "023": ["80", "000000", "FF0300"], "025": ["5", "000000", "081100"]}
    per.show()
    print(per.get_obj())