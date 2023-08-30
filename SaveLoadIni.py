import configparser
from MainClass import  Person, ObjectBolid
import os
import time


def save_log(edit_data, mess):
    # Файл для сохранения изменений
    path = 'log_bd.txt'
    file = open(path, 'a')
    file.write(f'{time.strftime("%d-%m-%y %H:%M", time.localtime())} | {mess} | {edit_data}\n')
    file.close()


def load_person_ini():
    # Загружаем объекты из файла
    path = 'person.ini'
    list_person = []
    if not os.path.exists(path):
        return list_person
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')
    list_person = []
    for hex_key in config.sections():
        pers = Person()
        pers.name = config[hex_key]['name']
        pers.surname = config[hex_key]['surname']
        pers.patronymic = config[hex_key]['patronymic']
        try:
            pers.bit = config[hex_key]['bit']
        except KeyError:
            pass
        # pers.key = bytes(hex_key, 'ascii')
        pers.key = hex_key
        for _ in config[hex_key]['permission'].split(';'):
            if _:
                id_obj, num_obj, xo_obj, perm_obj = map(str.strip, _.split(','))
                pers.permission[id_obj] = [num_obj, xo_obj, perm_obj.upper()]
        list_person.append(pers)
    return list_person


def save_person_ini(list_person):
    # Сохраняем созданные объекты в файл
    path = 'person.ini'
    config = configparser.ConfigParser()
    for _ in list_person:
        str_permission = ''
        for _perm in _.permission:
            str_permission += f"{_perm}, {_.permission[_perm][0]}, {_.permission[_perm][1]}, {_.permission[_perm][2].upper()};"
        config[f"{_.key.upper()}"] = {'name': _.name.title(),
                                      'surname': _.surname.title(),
                                      'patronymic': _.patronymic.title(),
                                      'permission': str_permission,
                                      'bit': _.bit}

    # shutil.copy('example.ini', 'example_tmp.ini')
    with open(path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def save_object_ini(list_object):
    # Сохраняем созданные объекты в файл
    path = 'object.ini'
    config = configparser.ConfigParser()
    for _ in list_object:
        str_permission = ''
        config[f"{_.id}"] = {'num': _.num,
                             'name': _.name,
                             'type': _.type,
                             'ver': _.ver,
                             'interface': _.interface,
                             'comment': _.comment}

    # shutil.copy('example.ini', 'example_tmp.ini')
    with open(path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def load_object_ini():
    # Загружаем объекты из файла
    path = 'object.ini'
    list_obj = []
    if not os.path.exists(path):
        return list_obj
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')

    for id_obj in config.sections():
        obj = ObjectBolid()
        obj.id = id_obj
        obj.num = config[id_obj]['num']
        obj.name = config[id_obj]['name']
        obj.type = config[id_obj]['type']
        obj.ver = config[id_obj]['ver']
        obj.interface = config[id_obj]['interface']
        obj.comment = config[id_obj]['comment']
        # pers.show()
        list_obj.append(obj)
    return list_obj


if __name__ == '__main__':
    aa = load_object_ini()
    for _ in aa:
        print(_.id, _.num)

