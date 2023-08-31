import tkinter as tk
from tkinter import ttk
from main_class import ObjectBolid
import save_load_ini as sl
from bolid_perm import Signal10, C2000_4

# Всплывающее меню при создании или редактировании информации об объекте
class FrameObject(tk.Toplevel):
    def __init__(self, parent, type_object, ver, open_object, object_list, name='', comment='', interface='', id=''):
        super().__init__(parent)
        self.type_object = type_object
        self.ver = ver
        self.set_id = id
        self.open_object = open_object
        self.object_list = object_list
        self.set_interface = interface
        self.comment = comment
        self.name = name
        self.create_frame()
        self.flag_change = False
        self.new_object = None

    def create_frame(self):
        self.label_num = ttk.Label(self, text="Номер:")
        self.label_num.place(x=0, y=0)
        self.entry_num = ttk.Entry(self)
        self.entry_num.place(x=100, y=0)
        self.entry_num.insert(0, self.open_object)

        self.label_name = ttk.Label(self, text="Наименование:")
        self.label_name.place(x=0, y=20)
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=100, y=20)
        self.entry_name.insert(0,self.name)

        self.label_type = ttk.Label(self, text="Тип:")
        self.label_type.place(x=0, y=40)
        self.entry_type = ttk.Entry(self)
        self.entry_type.place(x=100, y=40)
        self.entry_type.insert(0, self.type_object)

        self.interface = tk.IntVar()
        self.interface.set(int(self.set_interface))
        self.chk_interface = ttk.Checkbutton(self, variable=self.interface, text='Touch Memory')
        self.chk_interface.place(x=0, y=60)

        self.label_desc = ttk.Label(self, text="Описание:")
        self.label_desc.place(x=0, y=80)
        self.obj_text = tk.Text(self, width=30, height=5)
        self.obj_text.place(x=10, y=100)
        self.obj_text.insert(1.0, self.comment)

        self.btn_save = ttk.Button(self, text='Сохранить', command=self.click_btn_save)
        self.btn_save.place(x=150, y=200)

    def click_btn_save(self):
        self.flag_change = True
        if self.set_id:
            for _ in self.object_list:
                if _.id == self.set_id:
                    _.num = self.entry_num.get()
                    _.name = self.entry_name.get()
                    _.interface = self.interface.get()
                    # _.ver = self.ver
                    _.comment = self.obj_text.get("1.0", tk.END)
            sl.save_object_ini(self.object_list)

        else:
            index_object = []
            for _ in self.object_list:
                index_object.append(_.id)
            index_list = ['{:03}'.format(_) for _ in range(1, 999)]
            for _ in index_list:
                if _ in index_object:
                    continue
                obj = ObjectBolid()
                obj.id = _
                obj.num = self.entry_num.get()
                obj.name = self.entry_name.get()
                if self.type_object == 'Signal-10':
                    obj.type = '10'
                    obj.interface = self.interface.get()
                if self.type_object == 'S2000-4':
                    obj.type = '4'
                    obj.interface = 0
                obj.ver = self.ver

                obj.comment = self.obj_text.get("1.0", tk.END)
                self.new_object = obj
                self.object_list.append(obj)
                # Добавляем запись в лог
                sl.save_log(id_obj=obj.id,
                            num_obj=obj.num,
                            name_obj=obj.name,
                            mess="Добавление Объекта")
                break
        self.destroy()
