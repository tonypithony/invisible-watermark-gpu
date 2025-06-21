def chair2binary(aichar):
    return bin(ord(aichar))[2:]  # Убираем '0b'

def binary2chair(binary_str):
    return chr(int(binary_str, 2))  # Переводим двоичное число в символ

def string2binary(aistring):
    return ''.join(map(chair2binary, aistring))  # объединяем все 7-битные строки

def binary2string(binary_str):
    # Проверяем, что длина кратна 7
    remainder = len(binary_str) % 7
    if remainder != 0:
        pad = 7 - remainder
        binary_str += '0' * pad
        print(f"[Предупреждение] Строка дополнена {pad} нулями для корректной обработки.")

    # Разбиваем по 7 символов
    chunks = [binary_str[i:i+7] for i in range(0, len(binary_str), 7)]

    # Восстанавливаем строку
    return ''.join(map(binary2chair, chunks))


source = 'hello'
binary = string2binary(source)
result = binary2string(binary)

print("Исходная строка:", source)
print("Бинарный вид:", binary)
print("Восстановленная:", result)


# Такая строка имеет длину 20 → не кратно 7 → будет дополнена до 21
test_binary = '11010001100101110110011'
restored = binary2string(test_binary)
print("Восстановленная из некорректной:", restored)


'''
Исходная строка: hello
Бинарный вид: 11010001100101110110011011001101111
Восстановленная: hello
[Предупреждение] Строка дополнена 5 нулями для корректной обработки.
Восстановленная из некорректной: hel`
'''


def string2binary(s):
    """Преобразует строку в бинарную строку (по 8 бит на символ)"""
    return ''.join(f"{byte:08b}" for byte in s.encode('utf-8'))

def binary2string(binary_str):
    """Восстанавливает строку из бинарного представления"""
    remainder = len(binary_str) % 8
    if remainder != 0:
        pad_bits = 8 - remainder
        binary_str += '0' * pad_bits
        print(f"[Предупреждение] Строка дополнена {pad_bits} нулями.")
    
    byte_data = bytes(int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8))
    return byte_data.decode('utf-8', errors='replace')

if __name__ == "__main__":
    original_text = "Привет, мир! Hello, world! 😊"
    print("Исходная строка:", original_text)

    # Кодируем в бинарную строку
    binary_str = string2binary(original_text)
    print("\nБинарное представление (первые 100 символов):\n", binary_str[:100] + "...")

    # Восстанавливаем обратно
    restored_text = binary2string(binary_str)
    print("\nВосстановленная строка:")
    print(restored_text)

    # Проверяем совпадение
    print("\nСовпадают ли оригинальная и финальная строки?",
          "✅" if original_text == restored_text else "❌")


    # print(string2binary('Hello')) # 0100100001100101011011000110110001101111

'''
Исходная строка: Привет, мир! Hello, world! 😊

Бинарное представление (первые 100 символов):
 1101000010011111110100011000000011010000101110001101000010110010110100001011010111010001100000100010...

Восстановленная строка:
Привет, мир! Hello, world! 😊

Совпадают ли оригинальная и финальная строки? ✅
'''