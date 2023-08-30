# Расчет контрольной суммы для ключа в виде 000000AAAAAA
import binascii
import crcmod.predefined


def crc(byte_str):
    # Устанавливаем тип кодировки. Для Болида это crc-8-maxim
    crc8 = crcmod.predefined.mkPredefinedCrcFun('crc-8-maxim')
    # Меняем порядок записи ключа. Реверсируем
    byte_str_reverse = byte_str
    for _ in range(int(len(byte_str) / 2) - 1):
        byte_str_reverse = byte_str_reverse[0:_ * 2] + byte_str_reverse[-2:] + byte_str_reverse[_ * 2:-2]
    # Добавляем служебный бит
    byte_str_reverse = b'01' + bytes(byte_str_reverse, 'ascii')
    # Высчитываем контрольную сумму
    a = hex(crc8(binascii.unhexlify(byte_str_reverse)))
    if len(a) < 4:
        return bytes('0' + a[2:].upper() + byte_str.upper() + '01', 'ascii')
    return bytes(a[2:].upper() + byte_str.upper() + '01', 'ascii')


def reverse_key(key):
    # Реверсируем ключ
    for _ in range(int(len(key) / 2) - 1):
        key = key[0:_ * 2] + key[-2:] + key[_ * 2:-2]
    return key


if __name__ == '__main__':
    # print(crc('00000072BEA5'))
    # print(crc('0000001811A6'))
    # print(crc('000000945A3B'))
    # print(crc('000000A21DD7'))
    # print(crc('000000423526'))
    # print(crc('0000003D2BAB'))
    # print(crc('0000001D67EC'))
    print(crc('0000007209E6'))
    print(crc('000000AB7094'))
