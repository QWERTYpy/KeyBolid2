# Верхнее меню
import tkinter as tk
import SaveLoadIni as sl
import crc8bolid as crc
import FramePerson as fp
from tkinter import filedialog
from FrameObject import FrameObject
from MainClass import Person
import binascii
import re
from Postgres import PostgessBase
from tkinter import messagebox as mb


class MainMenu:
    def __init__(self, root, table, info_frame, person_list, object_list):
        """
        Инициализируем верхнее меню
        :param root: Указатель на основное окно
        :param table: Указатель на таблицу с даныными
        :param info_frame: Указатель на информационное поле
        :param person_list: Список Персон (Объектов класса Person)
        :param object_list: Список Объектов ( Объектов класса Object)
        """
        self.root = root
        self.table = table
        self.info_frame = info_frame
        self.person_list = person_list
        self.object_list = object_list
        self.flag_change = False  # Флаг для отслеживания изменений
        self.open_object = 0  # Инициируем переменную содержащую номер импортируемого Объекта получаемого из названия файла
        self.main_menu = tk.Menu(self.root)
        self.old_object = None  # При импорте уже существующего Объекта
        # Добавляем пункты меню
        self.main_menu.add_command(label="Сохранить", command=self.main_menu_save_object)
        self.main_menu.add_command(label="Загрузить", command=self.main_menu_load_object)
        self.main_menu.add_command(label="Добавить", command=self.main_menu_load_person)
        self.main_menu.add_command(label="Удалить", command=self.main_menu_delete_person)
        self.main_menu.add_command(label="Удалить возвращенные", command=self.main_menu_delete_return)
        self.main_menu.add_command(label="Удалить заблокированные", command=self.main_menu_delete_block)
        # Если соединение с БД отсутвет, то отключаем
        if not self.table.bd.flag_BD:
            self.main_menu.entryconfig("Удалить возвращенные", state="disabled")
        self.root.config(menu=self.main_menu)

    def main_menu_delete_return(self):
        # Удаление возвращенных пропусков
        if self.table.object_main == '000':
            self.info_frame.title_left_down_text.set("Выберите Объект ...")
        else:
            person_bd = PostgessBase()
            # Пробегаем весь список персон соответсвующих выбранному Объекту
            for _ in self.table.people_table:
                # Если ключ возвращен, то удаляем его
                if person_bd.search_card(_[3]) != 1:
                    # Находим указатель на интересующую персону
                    for __ in self.person_list:
                        if __.key == _[3]:
                            sl.save_log(f"{_[0]} {_[1]} {_[2]} {_[3]}- {self.table.object_main}", f"Удаление Персоны")
                            __.permission.pop(self.table.object_main)

                            if len(__.permission) == 0:
                                self.person_list.remove(__)
                                break
            # Обновляем записи в таблице
            self.table.search_table_action()

    def main_menu_delete_block(self):
        # Удаление заблокированных пропусков
        if self.table.object_main == '000':
            self.info_frame.title_left_down_text.set("Выберите Объект ...")
        else:
            person_bd = PostgessBase()
            # Пробегаем весь список персон соответсвующих выбранному Объекту
            for _ in self.table.people_table:
                # Если ключ возвращен, то удаляем его
                if person_bd.search_block(_[3]) == 1:
                    # Находим указатель на интересующую персону
                    for __ in self.person_list:

                        if __.key == _[3]:
                            for ___ in self.object_list:
                                if ___.id == self.table.object_main:

                                    sl.save_log(f"{_[0]} {_[1]} {_[2]} {_[3]}- {___.num} {___.name}", f"Удаление Заблокированной Персоны")
                                    __.permission.pop(self.table.object_main)

                                    if len(__.permission) == 0:
                                        self.person_list.remove(__)
                                        break
            # Обновляем записи в таблице
            self.table.search_table_action()

    def main_menu_delete_person(self):
        """
        Для удаления выбранной персоны
        :return:
        """
        # Если ничего не выбрано
        if self.table.object_main == '000':
            # Получаем ключ из выбранной строки
            if self.table.main_table.selection():
                select_person = str(self.table.main_table.item(self.table.main_table.selection())['values'][3])
                if len(select_person) < 12:
                    select_person = '000000' + select_person[-6:]
                for _ in self.person_list:
                    # Выбираем Персону соответсвующую ключу
                    if _.key == select_person:
                        # Удаляем из списка прав запись соответсвующую выбранному Объекту
                        answer = mb.askyesno(
                            title="Удаление записи",
                            message="Удалить все записи по выбранному человеку?")
                        if answer:
                            sl.save_log(f"{_.surname} {_.name} {_.key} - {self.table.object_main}", f"Удаление Персоны")
                            self.person_list.remove(_)
                            self.flag_change = True
                            break

                # Обновляем записи в таблице
                self.table.search_table_action()
                # -----
            else:
                self.info_frame.title_left_down_text.set("Выберите Объект ...")
        else:
            # Получаем ключ из выбранной строки
            self.flag_change = True
            if self.table.main_table.selection():
                select_person = str(self.table.main_table.item(self.table.main_table.selection())['values'][3])
                if len(select_person) < 12:
                    select_person = '000000' + select_person[-6:]
                for _ in self.person_list:
                    # Выбираем Персону соответсвующую ключу
                    if _.key == select_person:
                        # Удаляем из списка прав запись соответвующую выбранному Объекту
                        for __ in self.object_list:
                            if __.id == self.table.object_main:
                                sl.save_log(f"{_.surname} {_.name} {_.key} - {__.num} {__.name}", f"Удаление Персоны")
                                _.permission.pop(self.table.object_main)

                        if len(_.permission) == 0:
                            self.person_list.remove(_)
                            break

                # Обновляем записи в таблице
                self.table.search_table_action()
            else:
                self.info_frame.title_left_down_text.set("Выберите Объект ...")

    def main_menu_load_person(self):
        """
        Добавление новой Персоны
        :return:
        """
        # Если ничего не выбрано
        if self.table.object_main == '000':
            self.info_frame.title_left_down_text.set("Выберете Объект ...")
        else:
            # Создаем дочернее окно для добавления новой Персоны и назначения ему прав для выбранного Объекта
            self.frame_person = fp.FramePerson(self.root, self.table, '', self.table.object_main, self.person_list,
                                               self.object_list)
            self.frame_person.geometry("400x400+50+50")
            self.frame_person.title('Редактирование доступа')
            self.frame_person.grab_set()
            self.frame_person.wait_window()
            # Если данные изменены, то обновляем данные
            if self.frame_person.flag_change:
                self.table.search_table_action()
            self.flag_change = self.flag_change or self.frame_person.flag_change

    def main_menu_save_object(self):
        """
        Сохраняем данные в ini файлы
        :return:
        """
        self.flag_change = False
        self.table.flag_change = False
        sl.save_person_ini(self.person_list)
        sl.save_object_ini(self.object_list)
        self.info_frame.title_left_down_text.set("Сохранено ...")

    def main_menu_load_object(self):
        """
        Импорт информации из файла ключей
        :return:
        """
        self.info_frame.title_left_down_text.set("Выберите файл")
        flag_object_add = False  # Флаг существования импортируемого Объекта в базе
        flag_key_add = False  # Флаг существования импортируемого ключа в базе
        # Открываем диалог выбора файла
        filepath = filedialog.askopenfilename(filetypes=[('Файлы ключей', '*.ki')])
        line_cursor = 0  # Указатель на количество обработанных строк
        buffer_str = b''  # Буфер для хранения разбитых строк
        flag_cursor_str = False  # Флаг указателя на строку с ключом и правами доступа
        # Если выбран файл
        if filepath != "":
            # Открываем файл для построчного чтения
            file = open(filepath, 'rb')
            for line in file:
                # Обрабатываем первую строку
                line_cursor += 1
                if line_cursor == 1:
                    # Выбираем из строки тип прибора и версию
                    str_type_ver = re.search(r'Keys.*v.\d.\d\d', line.decode('ansi'))
                    _, type_obj, ver = str_type_ver[0].split(' ')
                    # Выбираем из имени файла номер прибора
                    self.open_object = re.search(r'\d{1,3}.ki', filepath)[0][:-3]
                    # Проверяем существует ли добавляемый Объект в базе
                    for _ in self.object_list:
                        if self.open_object == _.num:
                            self.info_frame.title_left_down_text.set("Объект существует в базе...")
                            self.old_object = _
                            flag_object_add = True  # Включаем флаг, что Объект существует
                            break
                    # Если Объекта нет в базе, то добавляем
                    if not flag_object_add:
                        self.info_frame.title_left_down_text.set("Добавление Объекта...")
                        # Создаем окно добавления описания к Объекту
                        frame_object = FrameObject(self.root, type_obj, ver, self.open_object, self.object_list)
                        frame_object.geometry("260x250+50+50")
                        frame_object.title('Добавление нового Объекта')
                        frame_object.grab_set()
                        frame_object.wait_window()
                # Выводим информацию об обработанных строках
                self.info_frame.title_left_down_text.set(f"Загрузка строк - {line_cursor}.")
                # Строка длиной 48 предшествует строке с ключом и правами
                if len(binascii.hexlify(line)) == 48:
                    # Если такая строка обнаружена включаем флаг и уходим на следующую итерацию
                    flag_cursor_str = True
                    continue
                # Если флаг включен начинаем разборс троки
                if flag_cursor_str:
                    # Добавляем строку в буфер, т.к. есть битые строки
                    # Если из этой строки не будет получен ключ, то строка плюсуется со следующей
                    buffer_str += line
                    # Если строка целая или последняя и тип Объекта Сигнал-10
                    if type_obj == "Signal-10" and len(binascii.hexlify(buffer_str)) == 304 or len(
                            binascii.hexlify(buffer_str)) == 262:
                        # Выключаем флаг, т.к. строка найдена
                        flag_cursor_str = False
                        # Получаем ключ и права доступа
                        self.file_key = crc.reverse_key(binascii.hexlify(buffer_str)[242:254])
                        self.file_perm = binascii.hexlify(buffer_str)[256:262]
                        # Обнуляем буфер
                        buffer_str = b''
                        # Включаем флаг, что получен ключ
                        flag_key_add = True
                    # Если строка целая или последняя и тип Объекта С2000-4
                    if type_obj == 'S2000-4' and len(binascii.hexlify(buffer_str)) == 346 or len(
                            binascii.hexlify(buffer_str)) == 276:
                        # Выключаем флаг т.к. строка найдена
                        flag_cursor_str = False
                        # Получаем ключ и права доступа
                        self.file_key = crc.reverse_key(binascii.hexlify(buffer_str)[214:226])
                        self.file_perm = binascii.hexlify(buffer_str)[228:234]
                        # Обнуляем буфер
                        buffer_str = b''
                        # Включаем флаг, что получен ключ
                        flag_key_add = True
                # Если ключ получен
                if flag_key_add:
                    # Переводим из byte в строку
                    self.file_key = self.file_key.decode('ansi')
                    self.file_perm = self.file_perm.decode('ansi')
                    for _ in self.person_list:
                        # Если такой ключ уже существует в базе
                        if _.key.upper() == self.file_key.upper():
                            self.info_frame.title_left_down_text.set("Такой ключ существует...")
                            # Если добавляется новый Объект
                            if not flag_object_add:  # Двойной импорт
                                if frame_object.new_object:
                                    # В словарь добаляется необходимая запись
                                    if _.permission.get(frame_object.new_object.id):
                                        if _.permission[frame_object.new_object.id][2] == self.file_perm.upper():
                                            print(
                                                f"Полный дубликат для прибора {self.open_object} ключ: {self.file_key.upper()}")
                                        else:
                                            print(
                                                '!!!! Расхождение прав доступа !!!! >>>> {self.open_object} ключ: {self.file_key}')
                                    else:
                                        _.permission[frame_object.new_object.id] = [frame_object.new_object.num,
                                                                                    '000000', self.file_perm.upper()]
                            else:
                                if self.old_object:
                                    # В словарь добаляется необходимая запись
                                    if _.permission.get(self.old_object.id):
                                        if _.permission[self.old_object.id][2] == self.file_perm.upper():
                                            print(
                                                f"Полный дубликат для прибора {self.open_object} ключ: {self.file_key.upper()}")
                                        else:
                                            print(
                                                '!!!! Расхождение прав доступа !!!! >>>> {self.open_object} ключ: {self.file_key}')
                                    else:
                                        _.permission[self.old_object.id] = [self.old_object.num,
                                                                            '000000', self.file_perm.upper()]
                            # Выключаем флаг добавления
                            flag_key_add = False
                            continue
                    # Если ключ еще не добавлен

                    if flag_key_add:
                        self.info_frame.title_left_down_text.set("Добавление ключа...")
                        if self.table.bd.flag_BD:
                            print(self.file_key.upper(),'->', self.table.bd.search_key(self.file_key.upper()))
                            name, firstname, secondname, key = self.table.bd.search_key(self.file_key.upper())[0]
                            if key:
                                new_person = Person(name=firstname, surname=name, patronymic=secondname, key=key)
                            else:
                                new_person = Person(key=self.file_key.upper())
                        else:
                            new_person = Person(key=self.file_key.upper())
                        # Если добавляется новый Объект
                        if not flag_object_add:
                            if frame_object.new_object:
                                new_person.permission[frame_object.new_object.id] = [frame_object.new_object.num,
                                                                                     '000000',
                                                                                     self.file_perm.upper()]
                                sl.save_log(
                                    f"{new_person.surname} {new_person.name} {new_person.key} - {frame_object.new_object.id} {frame_object.new_object.num} {frame_object.new_object.name} ",
                                    f"Импорт Персоны")
                        else:
                            if self.old_object:
                                new_person.permission[self.old_object.id] = [self.old_object.num,
                                                                             '000000',
                                                                             self.file_perm.upper()]
                                sl.save_log(
                                    f"{new_person.surname} {new_person.name} {new_person.key} - {self.old_object.id} {self.old_object.num} {self.old_object.name}",
                                    f"Импорт Персоны")

                        # В список добавляется новая Персона
                        self.person_list.append(new_person)

                        # Флаг добавления нового ключа выключается
                        flag_key_add = False
            # Обновляются данные в таблице
            self.table.reboot_table()
            # Закрывается файл ключей
            file.close()
