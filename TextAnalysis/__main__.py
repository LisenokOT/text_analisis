# pylint: disable=invalid-name
"""
TextAnalysis - анализатор темы текстов.
Использование:
    Аргумент -h             Отобразить это сообщение
    Аргумент -i <файл>      Обработать текст из файла
    add <тема>              Добавить темы
    remove <тема>           Удалить тему
    list                    Отобразить сохраненные темы
    text <text>             Обработать введенный текст
    Аргумент -t <файл>      Использовать свой словарь тем

Полное использование:
Usage:
    TextAnalysis (-h|--help|--version)
    TextAnalysis [-i=<path>]    [-t=<path>]
    TextAnalysis add <theme>    [-t=<path>]
    TextAnalysis remove <theme> [-t=<path>]
    TextAnalysis list           [-t=<path>]
    TextAnalysis text [-t=<path>] <text>

Options:
    <theme>                   Название темы
    <text>                    Обычный текст
    -i --input_file=<path>    Путь файла с текстом
    -t --themes_file=<path>   Путь файла с темами

"""
from docopt import docopt

from TextAnalysis.__init__ import __version__
from TextAnalysis.main import main

DEFAULT_ARG = {
    '--themes_file': './demo_data/themes.json',
    '--input_file': './demo_data/input.txt',
}

if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    # Запуск без параметров
    args['use_local_files'] = 0  # Флаг использования файлов по умолчанию
    if not args['--themes_file']:
        args['--themes_file'] = DEFAULT_ARG['--themes_file']
        args['use_local_files'] += 1
    if not args['--input_file']:
        args['--input_file'] = DEFAULT_ARG['--input_file']
        args['use_local_files'] += 2
    # Запуск
    main(args)
