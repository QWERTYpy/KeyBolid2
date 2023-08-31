import tkinter as tk
from tkinter import ttk
from postgres import PostgessBase


# Всплывающее меню при создании или редактировании информации о объекте
class Get_BD(tk.Toplevel):
    def __init__(self, parent, hex_key, _name, _surname, _patr):
        super().__init__(parent)
        self.root = parent
        self.search_table(hex_key, _name, _surname, _patr)
        self.main_table_create()

    def search_table(self, hex_key, _name, _surname, _patr):
        """
        Составляем интерфейс для поиска
        :return:
        """
        ttk.Label(self, text="Фамилия").place(x=10, y=10)
        self.entry_surname = ttk.Entry(self)
        self.entry_surname.config(width=23)
        self.entry_surname.place(x=10, y=30)
        self.entry_surname.insert(0,_surname)

        ttk.Label(self, text="Имя").place(x=160, y=10)
        self.entry_name = ttk.Entry(self)
        self.entry_name.config(width=23)
        self.entry_name.place(x=160, y=30)
        self.entry_name.insert(0,_name)

        ttk.Label(self, text="Отчество").place(x=310, y=10)
        self.entry_patronymic = ttk.Entry(self)
        self.entry_patronymic.config(width=23)
        self.entry_patronymic.place(x=310, y=30)
        self.entry_patronymic.insert(0,_patr)

        ttk.Label(self, text="Ключ").place(x=460, y=10)
        self.entry_hex = ttk.Entry(self)
        self.entry_hex.config(width=23)
        self.entry_hex.place(x=460, y=30)
        self.entry_hex.insert(0, hex_key)

        self.btn_entry = ttk.Button(self, text='Искать ...', command=self.search_table_action, width=10)
        self.btn_entry.place(x=610, y=28)

    def search_table_action(self):
        """
        Поиск по таблице
        :return:
        """
        pb = PostgessBase()
        # Очищаем таблицу
        self.main_table.delete(*self.main_table.get_children())
        # Заполняем данными удовлетворяющими критериям поиска
        # Если заполнено одно из полей
        if self.entry_surname.get() or self.entry_name.get() or self.entry_patronymic.get():
            # print('Search fio')
            person_list = pb.search_fio(self.entry_surname.get().title(), self.entry_name.get().title(),
                                        self.entry_patronymic.get().title())
            # Очищаем таблицу
            self.main_table.delete(*self.main_table.get_children())
            # Выводим данные в таблицу
            for person in person_list:
                self.main_table.insert("", tk.END, values=person)

        elif self.entry_hex.get():
            # print('Seach hex')
            for _ in pb.search_key(self.entry_hex.get()):
                name, firstname, secondname, key = _
                if name or firstname or secondname:
                    self.main_table.insert("", tk.END, values=[name, firstname, secondname, key, ''])
        else:
            pass

    def main_table_create(self):
        # Составляем колонки
        table_column = ('surname', 'name', 'patronymic', 'hex_key', 'tab_name')
        # Создаем таблицу
        self.main_table = ttk.Treeview(self, columns=table_column, show='headings')
        self.main_table.place(x=10, y=70)
        # Определяем заголовки
        self.main_table.heading('name', text='Имя', anchor=tk.W)
        self.main_table.heading('surname', text='Фамилия', anchor=tk.W)
        self.main_table.heading('patronymic', text='Отчество', anchor=tk.W)
        self.main_table.heading('hex_key', text='Ключ', anchor=tk.W)
        self.main_table.heading('tab_name', text='Табельный номер', anchor=tk.W)
        # Определяем ширину столбцов
        self.main_table.column("#1", stretch=tk.NO, width=150)
        self.main_table.column("#2", stretch=tk.NO, width=150)
        self.main_table.column("#3", stretch=tk.NO, width=150)
        self.main_table.column("#4", stretch=tk.NO, width=150)
        self.main_table.column("#5", stretch=tk.NO, width=150)
        # Добавляем прокрутку
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.main_table.yview)
        self.main_table.configure(yscroll=self.scrollbar.set, height=12)
        self.scrollbar.place(relx=1.0, relheight=1.0, in_=self.main_table, bordermode='outside')

        self.btn_entry = ttk.Button(self, text='Добавить', command=self.add_button, width=10)
        self.btn_entry.place(x=610, y=340)

    def add_button(self):
        # Передаем данные в поля формы
        if self.main_table.selection():
            name, firstname, secondname, key, _ = self.main_table.item(self.main_table.selection())['values']
            if len(str(key)) < 12:
                key = '000000'+str(key)[-6:]
            if name or firstname or secondname or key:
                self.root.entry_name.delete(0, tk.END)
                self.root.entry_name.insert(0, firstname)
                self.root.entry_surname.delete(0, tk.END)
                self.root.entry_surname.insert(0, name)
                self.root.entry_patr.delete(0, tk.END)
                self.root.entry_patr.insert(0, secondname)
                self.root.entry_hex.delete(0, tk.END)
                self.root.entry_hex.insert(0, key)
                self.destroy()
