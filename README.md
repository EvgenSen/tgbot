# tgbot
Пример использования библиотеки telebot для взаимодействия с API telegram

## main.py

Синхронный телебот

Список команд:

* image - получить изображение с камер. Инфо о камерах задается в конфиге.
* save - сохранить заметку. Текст заметки может быть в сообщении с командой или в следующем сообщении.
* read - прочитать заметку.
* worktime - прочитать инфо об отработанном времени (TODO).

## main_async.py

Асинхронный телебот

Список команд:

* image - получить изображение с камер. Инфо о камерах задается в конфиге.
* save - сохранить заметку. Текст заметки должен быть в сообщении с командой.
* read - прочитать заметку.
