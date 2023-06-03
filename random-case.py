def random_case(string: str) -> str:
    from random import choice
    funcs = [str.upper, str.lower]
    result = [choice(funcs)(letter) for letter in string]
    return ''.join(result)


while True:
    a = input('Введи слово: ')
    print(random_case(a))

