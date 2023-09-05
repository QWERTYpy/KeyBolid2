import tkinter as tk
import save_load_ini as sl
import main_menu as mm
import table as tbl
from main_class import InfoFrame, InfoFrame2
from tkinter import messagebox as mb


# 4.1.6.12290 UProg


def on_closing():
    flag_change = False  # Инициализируем флаг для проверки на изменение данных
    flag_change = table.flag_change or main_menu.flag_change  # Проверяем смежные флаги
    # Если были произведены изменения, спрашиваем нужно ли их сохранять
    if flag_change:
        answer = mb.askyesno(
            title="Обнаружены изменения",
            message="Сохранить данные?")
    # Если ответ утвердительный, то сохраняем
    if flag_change and answer:
        sl.save_person_ini(person_list)
    root.destroy()  # Закрыть окно


# Основные переменные
object_list = sl.load_object_ini()  # Список объектов
person_list = sl.load_person_ini()  # Список персон
object_flag = {_.num: 0 for _ in object_list}
# Создаем приложение
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.title("KeyBolid - v.2.3.0")
root.geometry("840x600+10+10")  # Создаем окно
root.resizable(False, False)  # Запрещаем изменять размер окна
root.configure(background='#ffffff')  # Устанавливаем цвет фона
# Создаем инфополе
infoframe = InfoFrame(root)
infoframe2 = InfoFrame2(root)
# Создаем основную таблицу
table = tbl.Table(root, infoframe, infoframe2, object_list, person_list,  object_flag)
# Создаем главное меню
main_menu = mm.MainMenu(root, table, infoframe, infoframe2, person_list, object_list, object_flag)
# Запускаем отображение
root.mainloop()
