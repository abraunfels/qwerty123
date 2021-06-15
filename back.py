import os
import hashlib
import keyring
import base64
import os
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import errors
import db_work

class ClientOpenData:
    def setattr(self, username, priv_key_RSA):
        self.username = username
        self.private_key_RSA = priv_key_RSA

client = ClientOpenData()

#################################################################################

def generate_key_HMAC(password):
    salt = os.urandom(32)
    passwordBytes = password.encode('utf-8')
    key = hashlib.pbkdf2_hmac(
        'sha256',  # Используемый алгоритм хеширования
        passwordBytes,  # Конвертируется пароль в байты
        salt,  # Предоставляется соль
        100000  # Рекомендуется использовать хотя бы 100000 итераций SHA-256
    )

    return salt, key

def generate_key_RSA(key_HMAC):
    key_RSA = RSA.generate(2048)

    encrypted_key_RSA = key_RSA.export_key(passphrase=key_HMAC, pkcs=8,
                                        protection="scryptAndAES128-CBC")
    return key_RSA.publickey(), encrypted_key_RSA

def generate_key_AES(public_key_RSA):
    key_AES = get_random_bytes(32)  # Это и должен быть наш ключ, который мы храним???Э

    encryptor = PKCS1_OAEP.new(public_key_RSA)
    encrypted_key_AES = encryptor.encrypt(key_AES)

    return encrypted_key_AES

def register(username, password):
    if db_work.check_user_exist(username) is False:
        salt, key_HMAC = generate_key_HMAC(password)
        public_key_RSA, encrypted_key_RSA = generate_key_RSA(key_HMAC)
        encrypted_key_AES = generate_key_AES(public_key_RSA)
        db_work.create_user(username, salt, key_HMAC, public_key_RSA.export_key(), encrypted_key_RSA, encrypted_key_AES)

    else: raise errors.RegisterError('Пользователь с таким именем уже существует!')

def encrypt_AES(key_RSA, encrypted_key_AES):
    decryptor = PKCS1_OAEP.new(key_RSA)
    decrypted_key_AES = decryptor.decrypt(encrypted_key_AES)
    return decrypted_key_AES

def check_master_key(salt, public_key_RSA, encrypted_key_RSA, password):

    # Используется та же настройка для генерации ключа, только на этот раз вставляется для проверки настоящий пароль
    new_key_HMAC = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),  # Конвертирование пароля в байты
        salt,
        100000
    )
    try:
        new_key_RSA = RSA.import_key(encrypted_key_RSA, passphrase=new_key_HMAC)
        return new_key_RSA

    except ValueError: raise errors.AccessError('Неверный мастер-ключ!', errors.AccessErrorType.PASSWORD_FASLE)



def check_entrance(username, password):
    if db_work.check_user_exist(username) is True:
        salt, public_key_RSA, encrypted_key_RSA  = db_work.get_key(username)
        new_key_RSA = check_master_key(salt, public_key_RSA, encrypted_key_RSA, password)
        client.setattr(username, new_key_RSA)

    else: raise errors.AccessError('Пользователь не найден!', errors.AccessErrorType.LOGIN_NOT_EXIST)

def check_attempts(username):
    if db_work.check_user_exist(username) is True:
        attempts = db_work.get_attempts(username)[0]
        return attempts

    else: raise errors.AccessError('Пользователь не найден!', errors.AccessErrorType.LOGIN_NOT_EXIST)

def new_attempts(username, val):
    if db_work.check_user_exist(username) is True: db_work.set_attempts(username, val)
    else: raise errors.AccessError('Пользователь не найден!', errors.AccessErrorType.LOGIN_NOT_EXIST)


################################################################################################

def decrypt_key_AES(encrypted_key_AES):
    decryptor = PKCS1_OAEP.new(client.private_key_RSA)
    key_AES = decryptor.decrypt(encrypted_key_AES)
    return key_AES



def new_element(username, address, login, password, comment=''):
    password = password.encode('utf-8')
    header = json.dumps({'address': address, 'login': login})
    header = header.encode('utf-8')

    encrypted_key_AES = db_work.get_AES(username)
    key_AES = decrypt_key_AES(encrypted_key_AES)

    cipher = AES.new(key_AES, AES.MODE_GCM)

    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(password)  # это то что будет хранится вместо наших данных

    json_k = ['nonce', 'header', 'ciphertext', 'tag']
    json_v = [b64encode(x).decode('utf-8') for x in (cipher.nonce, header, ciphertext, tag)]
    result = json.dumps(dict(zip(json_k, json_v)))
    id = db_work.add_element(username, address, login, result, comment)
    return id


def decrypt_passord(username, password):
    try:
        b64 = json.loads(password)
        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        jv = {k: b64decode(b64[k]) for k in json_k}

        encrypted_key_AES = db_work.get_AES(username)
        key_AES = decrypt_key_AES(encrypted_key_AES)

        cipher = AES.new(key_AES, AES.MODE_GCM, nonce=jv['nonce'])
        cipher.update(jv['header'])
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        dict = json.loads(jv['header'])
        return str(plaintext), str(dict['address']), str(dict['login'])

    except ValueError:
        raise errors.OrdinaryError("Неверное расшифрование")


def get_elements(username):
    data = db_work.get_elements(username)
    dict_data = {}
    for el in data:
        dict_data[el[0]]={'address': el[1],
            'login': el[2],
            'comment' : el[3]
        }
    return dict_data

##################################################################################################

def del_element(username, id):
    db_work.delete_element(username, id)

def get_element(username, id):
    id, address, login, pwd, comment = db_work.get_element(username, id)
    password, address, login = decrypt_passord(username,pwd)

    dict_data = {'address': address,
            'login': login,
            'password' : password,
            'comment' : comment
        }
    return dict_data

#####################################################################################################
def edit_element(username, id, address, login, password, comment=''):
    password = password.encode('utf-8')

    encrypted_key_AES = db_work.get_AES(username)
    key_AES = decrypt_key_AES(encrypted_key_AES)

    cipher = AES.new(key_AES, AES.MODE_GCM)

    ciphertext, tag = cipher.encrypt_and_digest(password)  # это то что будет хранится вместо наших данных

    json_k = ['nonce','ciphertext', 'tag']
    json_v = [b64encode(x).decode('utf-8') for x in (cipher.nonce, ciphertext, tag)]
    result = json.dumps(dict(zip(json_k, json_v)))
    db_work.edit_element(username, id, address, login, result, comment)



