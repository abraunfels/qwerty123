#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
import errors

Big = 'QWERTYUIOPASDFGHJKLZXCVBNM'
Low = 'qwertyuiopasdfghjklzxcvbnm'
Num = '1234567890'
Spe = '!@#$%^&amp;*()'

BI = False  # Пароль должен содержать символы в верхнем регистре (True - да | False - нет)
LO = True  # Пароль должен содержать символы в нижнем регистре (True - да | False - нет)
NU = True  # Пароль должен содержать цифры (True - да | False - нет)
PS = True  # Пароль должен содержать спец символы (True - да | False - нет)

def gen_pwd(Password_len=15, BI=True, LO=True, NU=True, PS=True):
    if Password_len:
        if Password_len.isdigit() == True:
            Password_len = int(Password_len)
        else:
            raise errors.OrdinaryError('Выход... Значение должно быть цифровое...')
    else:
        raise errors.OrdinaryError('Выход... Не указана Длина пароля...')

    if (BI or  NU or LO or PS) is True:

        Pass_Symbol = []
        if BI == True:
            Pass_Symbol.extend(list(Big))

        if LO == True:
            Pass_Symbol.extend(list(Low))

        if NU == True:
            Pass_Symbol.extend(list(Num))

        if PS == True:
            Pass_Symbol.extend(list(Spe))

        random.shuffle(Pass_Symbol)
        psw = [random.choice(Pass_Symbol) for x in range(Password_len)]
        res = ''.join(str(x) for x in psw)
        return res

    else: raise errors.OrdinaryError('Дурачок?')