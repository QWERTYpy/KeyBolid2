import tkinter as tk
from tkinter import ttk
from MainClass import Person, ObjectBolid
from BolidPerm import Signal10, C2000_4
import re
import SaveLoadIni as sl
from FrameGetBd import Get_BD


# Всплывающее меню при создании или редактировании информации о объекте
class FramePerson(tk.Toplevel):
    def __init__(self, parent, table, key, object, person_list, object_list):
        super().__init__(parent)
        self.key = key
        self.table = table
        # print(key)
        self.object = object
        self.person_list = person_list
        self.object_list = object_list
        # self.checkbox_list = []
        self.object_cur = ''
        for __ in self.object_list:
            if __.id == self.object:
                self.object_cur = __
        for _ in self.person_list:
            # print(type(_.key), type(self.key))
            if _.key[6:] == self.key[6:]:
                self.flag_add_new = False
                self.person_cur = _
        if not self.key:
            self.person_cur = Person()
            self.flag_add_new = True
            # self.person_list.append(Person())
            # self.person_cur = self.person_list[-1]
            self.person_cur.permission[self.object_cur.id] = [self.object_cur.num, '000000', '000000']

        self.create_frame()
        if self.key:
            self.filling_person()
        if self.object_cur.type == '4':
            self.bolid_4(self.object_cur)
        if self.object_cur.type == '10':
            self.bolid_10(self.object_cur)
        self.flag_change = False
        self.btn_save = ttk.Button(self, text='Сохранить', command=self.click_btn_save)
        self.btn_save.place(x=300, y=340)

    def filling_person(self):
        self.entry_name.insert(0, self.person_cur.name)
        self.entry_surname.insert(0, self.person_cur.surname)
        self.entry_patr.insert(0, self.person_cur.patronymic)
        #self.entry_hex.insert(0, self.person_cur.key)
        self.entry_hex.insert(0, self.person_cur.key)
        if int(self.object_cur.interface):
            self.entry_bit.insert(0, self.person_cur.bit)

    def bolid_4(self, obj: ObjectBolid):
        ttk.Label(self, text="Настройка:").place(x=0, y=110)
        if obj.type == '4':
            obj_type = 'C2000-4'
        ttk.Label(self, text=obj_type).place(x=100, y=110)
        ttk.Label(self, text=obj.name).place(x=200, y=110)

        self.object_c2000_4 = C2000_4(self, self.person_cur, obj.id)
        self.obj_text = tk.Text(self, width=44, height=4)
        self.obj_text.place(x=10, y=230)
        self.obj_text.insert(1.0, obj.comment)
        self.obj_text.configure(state=tk.DISABLED)

    def bolid_10(self, obj: ObjectBolid):
        ttk.Label(self, text="Настройка:").place(x=0, y=110)
        if obj.type == '10':
            obj_type = 'Сигнал10'
        ttk.Label(self, text=obj_type).place(x=100, y=110)
        ttk.Label(self, text=obj.name).place(x=200, y=110)
        self.object_signl10 = Signal10(self, self.person_cur, obj.id)
        self.obj_text = tk.Text(self, width=44, height=4)
        self.obj_text.place(x=10, y=230)
        self.obj_text.insert(1.0, obj.comment)
        self.obj_text.configure(state=tk.DISABLED)

    def create_frame(self):
        self.label_surname = ttk.Label(self, text="Фамилия:")
        self.label_surname.place(x=0, y=0)
        self.entry_surname = ttk.Entry(self)
        self.entry_surname.place(x=100, y=0)

        self.search_btn = ttk.Button(self, text='Взять из БД', command=self.get_bd)
        self.search_btn.place(x=250, y=0)
        if not self.table.bd.flag_BD:
            self.search_btn['state'] = 'disabled'

        self.label_name = ttk.Label(self, text="Имя:")
        self.label_name.place(x=0, y=20)
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=100, y=20)

        self.label_patr = ttk.Label(self, text="Отчество:")
        self.label_patr.place(x=0, y=40)
        self.entry_patr = ttk.Entry(self)
        self.entry_patr.place(x=100, y=40)
        #
        self.label_hex = ttk.Label(self, text="Ключ:")
        self.label_hex.place(x=0, y=60)
        check = (self.register(self.is_valid), "%P")
        self.entry_hex = ttk.Entry(self, validate="key", validatecommand=check)
        self.entry_hex.place(x=100, y=60)

        self.search_btn = ttk.Button(self, text='Искать', command=self.click_btn_search)
        self.search_btn.place(x=250, y=60)

        self.label_bit = ttk.Label(self, text="Доп. ключ:")
        self.label_bit.place(x=0, y=80)
        self.entry_bit = ttk.Entry(self)
        self.entry_bit.place(x=100, y=80)

    def get_bd(self):
        self.frame_get_bd = Get_BD(self, self.entry_hex.get())

        self.frame_get_bd.geometry("790x400+50+50")
        self.frame_get_bd.title('Поиск в базе данных')
        self.frame_get_bd.grab_set()
        self.frame_get_bd.wait_window()

    def is_valid(self,newval):
        return re.match("^[0-9ABCDEFabcdef]{0,12}$", newval) is not None


    def click_btn_search(self):

        for _ in self.person_list:
            if _.key.upper() == self.entry_hex.get().upper():
                self.entry_name.delete(0,tk.END)
                self.entry_name.insert(0, _.name)
                self.entry_surname.delete(0,tk.END)
                self.entry_surname.insert(0, _.surname)
                self.entry_patr.delete(0,tk.END)
                self.entry_patr.insert(0, _.patronymic)

    def click_btn_save(self):
        flag_dubl_key = False
        # # edit_cur = False
        for _ in self.person_list:
            if _.key.upper() == self.entry_hex.get().upper():
                print(f'Обнаружен дубликат ключа: {_.key.upper()}')
                flag_dubl_key = True
                self.person_cur = _
                self.person_cur.permission[self.object_cur.id] = [self.object_cur.num, '000000', '000000']
        # for _ in self.object_list:
        #     if _.id == self.object_cur.id:
        #         print(f'Изменения в текущем Объекте: {_.id} - {_.num}')
        #         edit_cur = True
        #         flag_dubl = False

        # if not self.flag_add_new:
        self.flag_change = True
        # Считываем новые данные
        self.person_cur.name = self.entry_name.get()
        self.person_cur.surname = self.entry_surname.get()
        self.person_cur.patronymic = self.entry_patr.get()
        self.person_cur.key = self.entry_hex.get().upper()
        self.person_cur.bit = self.entry_bit.get().upper()
        if self.object_cur.type == '10':
            self.person_cur.permission[self.object_cur.id][2] = self.person_cur.convert_check_10(
                self.object_signl10.get_checkbox())
        if self.object_cur.type == '4':
            self.person_cur.permission[self.object_cur.id][2] = self.person_cur.convert_check_4(
                self.object_c2000_4.get_checkbox(), self.object_c2000_4.get_perm())
        if self.flag_add_new and not flag_dubl_key:
            self.person_list.append(self.person_cur)
        # Добавляем запись в лог
        sl.save_log(f"{self.person_cur.surname} {self.person_cur.name} {self.person_cur.patronymic} {self.person_cur.key} - {self.object}", f"Изменнение данных")
        self.destroy()
