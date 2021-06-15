# qwerty123
## Кроссплатформенное приложение для управления паролями.

###### Хранение паролей.
1. Шифрование паролей на криптосистеме AES.
2. Ключ шифрования AES также хранится в зашифрованном виде с помощью  RSA.
3. Закрытый ключ RSA хранится по стандарту PKCS#8.
4. Паролем для закрытого ключа RSA является хеш-сумма (PBKDF2-HMAC-SHA256, 100000) от мастер-ключа пользователя. 

###### Вход в систему.
<img width="501" alt="auth" src="https://user-images.githubusercontent.com/22542567/121979373-baedd480-cd92-11eb-9c84-877b1096cd88.png">

###### Интерфейс пользователя.
<img width="502" alt="main" src="https://user-images.githubusercontent.com/22542567/121979596-2637a680-cd93-11eb-881a-39248e6d413a.png">

###### Генерирование псевдослучайных паролей.
<img width="565" alt="gen" src="https://user-images.githubusercontent.com/22542567/121979463-ea044600-cd92-11eb-9dec-22e70b44d5de.png">

