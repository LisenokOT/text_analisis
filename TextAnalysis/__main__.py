"""
TextAnalysis

Usage:
    TextAnalysis [-i=<path>] [-t=<path>]
    TextAnalysis (-h|--help|--version)

Options:
    -i --input_file=<path>        Файл с текстом
    -t --themes_file=<path>        Файл с темами
"""
from docopt import docopt

from TextAnalysis.__init__ import __version__
from TextAnalysis.main import main

DEFAULT_ARG = {'--themes_file': 'demo_data/themes.json',
               '--input_file': 'demo_data/input.txt'}

if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    # Запуск без параметров
    args['use_local_files'] = 0 # Флаг использования файлов по умолчанию
    if not (args['--themes_file']):
        args['--themes_file'] = DEFAULT_ARG['--themes_file']
        args['use_local_files'] += 1
    if not (args['--input_file']):
        args['--input_file'] = DEFAULT_ARG['--input_file']
        args['use_local_files'] += 2
    # Запуск
    main(args)
