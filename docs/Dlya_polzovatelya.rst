Руководство пользователя
==================================

Как установить программу
--------------------------------------------
| **Установка для Windows:**
| 1) Скачать архив по ссылке и разархивировать его в папку, затем добавить папку bin в PATH
| Ссылка на HunSpell: Ссылка_
.. _Ссылка: https://sourceforge.net/projects/ezwinports/files/hunspell-1.3.2-3-w32-bin.zip/download
| В Windows 10 можно добраться до настройки PATH так: Этот компьютер → Свойства → Дополнительные параметры системы → Дополнительно → Переменные среды. Или вызовом «Изменение переменных среды текущего пользователя» в результатах поиска.
| В окошке «Переменные среды» в блоке «Переменные среды пользователя %USERNAME%» находим строку PATH, выделяем кликом, жмем кнопку «Изменить…» и в появившемся окошке нажимаем «Создать» для добавления ещё одного элемента. В самом элементе нужно вписать путь к папке bin
| 2) Затем выполнить команду в папке с архивом TextAnalysis: ``pip install TextAnalysis-1.0.0.zip``
|
| **Установка для Linux:**
| 1) Скачать архив по ссылке и разархивировать его в папку, затем добавить папку bin в PATH
| 2) Установить библиотеку libhunspell-dev. Для Ubuntu и других похожих дистрибутивов команда ``sudo apt-get install libhunspell-dev``
| 3) Затем выполнить команду в папке с архивом TextAnalysis: ``pip install TextAnalysis-1.0.0.zip``
|
| **Установка из исходника:**
| 1) Скачать исходный код и разархивировать его
| 2) Затем установка из исходника повторяет инструкцию для конкретной ОС, но последнем шаге команда заменяется на ``pip install ./``

Как использовать программу
--------------------------------------------
| Вызов помощи по использованию программы ``python -m TextAnalysis --help``
| Вывести список тем можно с помощью ``python -m TextAnalysis list``
| Можно ввести свою тему с помощью ``python -m TextAnalysis add <тема>``, удалить тему ``python -m TextAnalysis remove <тема>``
| Можно отправить на обработку введенный текст ``python -m TextAnalysis text <ввести текст>``
| Можно отправить на обработку текст из файла ``python -m TextAnalysis -i <путь к файлу>``

Что нужно для работы программы
--------------------------------------------
| Для программы нужен интернет, а именно сайт, с которого парсятся данные "Букварикс".