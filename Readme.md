"Man to HTML" ("Man2HTML")
Версия: 1.1
Автор: Орлов Илья (ilyaorlov1998@gmail.com)

ОПИСАНИЕ:
Данное приложение предназначено для конвертации файлов с расширением ".man" в файлы с расширением ".html"

ТРЕБОВАНИЯ:
*Python версии не ниже 3.4

СОСТАВ:

КОНСОЛЬНАЯ ВЕРСИЯ:
Справка В Windows консоли(запуск консоли из директории с файлом): python man2html.py -h

ПОДРОБНОСТИ РЕАЛИЗАЦИИ:
Используется модуль argparse для упрощенной работы с аргументами. В файле macroses.py определены основные функции
и классы для определения и конвертирования макросов и прилагающегося текста

ОБНОВЛЕНИЯ:
Ver 1.1: Реализован переход по внешним ссылкам, Добавлено Оглавление каждой страницы,