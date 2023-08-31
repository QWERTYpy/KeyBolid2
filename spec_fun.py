# Специальные функции для обработки

def convert_check_10(chk_list):
    """
    Преобразует список флагов полученный из чекбоксов в hex строку
    :param chk_list: Список переменных чекбоксов
    :return: FFFFFF
    """
    list_bin_perm = []  # Список флагов
    for _ in range(len(chk_list)):
        list_bin_perm.append(chk_list[_].get())  # Заполянем список значениями флагов
    # Первые 8 флагов образуют 1 байт
    list_bin_perm_tmp = list_bin_perm[0:8]
    # Берем их в обратном порядке, преобразуем в строку и склеиваем
    str_bin = ''.join(map(str, list_bin_perm_tmp[::-1]))
    # Добавляем префикс, чтобы указать, что это бинарная запись
    str_bin = '0b' + str_bin
    # Преобразуем в hex из бинарной строки и берем только значение
    hex_A = hex(int(str_bin, 2))[2:]
    # Если символов меньше 2 добиваем спереди 0
    if len(hex_A) < 2:
        hex_A = '0' + hex_A

    list_bin_perm_tmp = list_bin_perm[8:16]
    str_bin = ''.join(map(str, list_bin_perm_tmp[::-1]))
    str_bin = '0b' + str_bin
    hex_B = hex(int(str_bin, 2))[2:]
    if len(hex_B) < 2:
        hex_B = '0' + hex_B

    list_bin_perm_tmp = list_bin_perm[16:20]
    str_bin = ''.join(map(str, list_bin_perm_tmp[::-1]))
    str_bin = '0b' + str_bin
    hex_C = hex(int(str_bin, 2))[2:]
    if len(hex_C) < 2:
        hex_C = '0' + hex_C
    return hex_A + hex_B + hex_C

def convert_check_4(chk_list, perm):
    """
    Получение hex для C2000-4
    :param chk_list:
    :param perm:
    :return:
    """
    if perm.get():
        hex_A = '10'
    else:
        hex_A = '00'
    list_bin_perm = []
    for _ in range(len(chk_list)):
        list_bin_perm.append(chk_list[_].get())

    str_bin = ''.join(map(str, list_bin_perm[::-1]))
    str_bin = '0b' + str_bin
    hex_B = hex(int(str_bin, 2))[2:]
    if len(hex_B) < 2:
        hex_B = '0' + hex_B

    if hex_B != '00':
        if hex_A == '10':
            hex_A = '18'
        if hex_A == '00':
            hex_A = '08'
    return hex_A + hex_B + '00'
