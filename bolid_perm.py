# Класс описывающий интерфейс Сигнал10
from tkinter import ttk
import tkinter as tk
from main_class import Person



class Signal10:
    def __init__(self, root, person_cur: Person, id_object):
        """
        Отображение интерфейса для управления правами Сигнал-10
        :param root: Ссылка на основное окно
        :param person_cur: Текущая персона
        :param id_object: Текущий Объект
        """
        self.root = root
        ttk.Label(self.root, text="Шлейф").place(x=0, y=130)
        for _ in range(10):
            ttk.Label(self.root, text=f"{_ + 1}", width=4, justify=tk.CENTER).place(x=f"{70 + _ * 30}", y=130)
        ttk.Label(self.root, text="Взятие").place(x=0, y=160)
        ttk.Label(self.root, text="Снятие").place(x=0, y=190)
        self.checkbox_list = person_cur.get_check_10(id_object)
        i = -1
        for _ in range(10):
            i += 1
            ttk.Checkbutton(self.root, variable=self.checkbox_list[i]).place(x=f"{70 + _ * 30}", y=190)
            i += 1
            ttk.Checkbutton(self.root, variable=self.checkbox_list[i]).place(x=f"{70 + _ * 30}", y=160)

    def get_checkbox(self):
        # Получение списка значений чекбокса
        return self.checkbox_list


class C2000_4:
    def __init__(self, root, person_cur: Person, obj):
        """
        Отображение интерейса для С2000-4
        :param root:
        :param person_cur:
        :param obj:
        """
        self.root = root
        ttk.Label(self.root, text="Шлейф").place(x=0, y=130)
        for _ in range(4):
            ttk.Label(self.root, text=f"{_ + 1}", width=4, justify=tk.CENTER).place(x=f"{70 + _ * 30}", y=130)
        ttk.Label(self.root, text="Взятие").place(x=0, y=160)
        ttk.Label(self.root, text="Снятие").place(x=0, y=190)
        self.checkbox_list = person_cur.get_check_4(obj)
        self.perm_2000_4 = person_cur.get_perm(obj)
        i = -1
        for _ in range(8):
            if _ < 4:
                i += 1
                ttk.Checkbutton(self.root, variable=self.checkbox_list[i]).place(x=f"{70 + _ * 30}", y=190)
            else:
                i += 1
                ttk.Checkbutton(self.root, variable=self.checkbox_list[i]).place(x=f"{70 + (_ - 4) * 30}", y=160)

        ttk.Checkbutton(self.root, variable=self.perm_2000_4, text='Доступ').place(x=230, y=130)

    def get_perm(self):
        # Получение значение СКУД С2000-4
        return self.perm_2000_4

    def get_checkbox(self):
        # Получение списка значений чекбокса
        return self.checkbox_list
