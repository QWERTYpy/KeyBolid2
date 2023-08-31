import binascii
import crc8bolid
import time


def write_key(number, permition_list): # [[key, perm]] 000000AABBCC, AABB00
    """
    Функция для записи файла ключей для С2000-4
    AA: 10 - Доступ
        08 - Ключ ХО
    BB: 1   2   3   4
    вз  10  20  40  80
    сн  01  02  04  08
    """
    # Заголовок файла
    b_head_start = b'134b6579732053323030302d3420762e332e303000'
    b_head_end = b'00000000005d4f80775cf819002000000018f91900904e807780f81900101d9501000000000a'
    # Промежуточное заполнение
    b_body = b'0400000000000030f91900d10e2501c0818177000000007c102d77ba701677d80415000a0400000000000030f9190000000000b1020000010000000a04000004888c030c8c8c03000000005100000000000000d8041500c015000000000000b8db900334f91900b7d5560000000000d10e250100000000880300000000000000f91900f93e1577101d95011876bb0090d88c03f4d190031800000034f9190090d88c03f4d190'
    # Концовка
    b_pre_end = b'ff0fffff0fff000000000000000000000000000101'
    b_end = b'00005d4f80775cf819002000000018f91900904e807780f81900101d9501000000000a'
    # Открывает файл для сохранения ключей
    file_new = open(f'exp_key/{number}_{time.strftime("%d%m%y_%H_%M", time.localtime())}.ki', 'wb')
    len_pass = len(permition_list)
    # Если ключей меньше 16, то берем последний символ и дибиваем его 0
    if len_pass < 16:
        b_count = bytes('0'+hex(len_pass)[2], 'ascii')
    else:
        # В противном сучае берем два символа
        b_count = bytes(hex(len_pass)[2:], 'ascii')
    # Заполняем файл
    file_new.write(binascii.unhexlify(b_head_start))
    file_new.write(binascii.unhexlify(b_count))
    file_new.write(binascii.unhexlify(b_head_end))
    for _perm_ind in range(len(permition_list)):
        file_new.write(binascii.unhexlify(b_body))
        b_key_perm = crc8bolid.reverse_key(crc8bolid.crc(permition_list[_perm_ind][0]))+bytes(permition_list[_perm_ind][1],'ascii')
        # print(b_key_perm)
        file_new.write(binascii.unhexlify(b_key_perm))
        file_new.write(binascii.unhexlify(b_pre_end))
        # Если ключ не последний, то добиваем строку концовкой
        if _perm_ind < len(permition_list)-1:
            file_new.write(binascii.unhexlify(b_end))
    # Закрываем файл
    file_new.close()

if __name__ == '__main__':
    permition_list = [['00550073d712', '330000']]
    write_key('10', permition_list)