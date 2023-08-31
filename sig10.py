import binascii
import crc8bolid
import time


def write_key(number, permition_list): # [[key, perm]] 000000AABBCC AABBCC
    """
    Функция для записи файла ключей для Сигнала - 10
    AA  1   2   3   4
    BB                  5   6   7   8
    CC                                  9   10
    вз  02  08  20  80  02  08  20  80  02  08
    сн  01  04  10  40  01  04  10  40  01  04
    """
    # Заголовок файла
    b_head_start = b'4b657973205369676e616c2d313020762e312e3030'
    b_head_end = b'00000000f91900904e047780f81900602e9001000000000a'
    # Промежуточное заполнение
    b_body = b'0400000000000030f91900d10ece02c0810577000000007c102376ba702575fa0302000a0400000000000030f9190000000000b1020000010000000a040000fc199103401d9103000000005100000000000000fa030200382800000000000058eb950334f91900b7d5560000000000d10ece0200000000880300000000000000f91900f93e2475602e9001000000001cd7910364d295031800000034f919001cd7910364d295031800000034f91900af244000cc'
    # Концовка
    b_end = b'00f91900904e047780f81900403f9901000000000a'
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
        file_new.write(binascii.unhexlify(b_key_perm))
        # Если ключ не последний, то добиваем строку концовкой
        if _perm_ind < len(permition_list)-1:
            file_new.write(binascii.unhexlify(b_end))
    # Закрываем файл
    file_new.close()

if __name__ == '__main__':
    permition_list = [['00550073d712', '330000']]
    write_key('10', permition_list)





