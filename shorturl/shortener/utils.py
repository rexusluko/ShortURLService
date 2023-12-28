import string


def next_code(code):
    """Генерирует следующий буквенный код"""
    alphabet = string.ascii_lowercase
    length = len(alphabet)

    # Если достигли последнего варианта "zzzzzzzz", начинаем снова с "aaaaaaaa"
    next_code = list(code)
    for i in range(len(next_code) - 1, -1, -1): # Идём справа на лево
        index = alphabet.index(next_code[i]) + 1 # Получаем индекс следующей буквы в алфавите
        if index < length: # Если индекс меньше длины алфавита, увеличиваем символ
            next_code[i] = alphabet[index]
            break
        else: # Если достигли "z", переходим к следующему символу
            next_code[i] = 'a'
    return ''.join(next_code)
