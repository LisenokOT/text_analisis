"""Основной файл программы."""
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup
from pkg_resources import resource_filename

from hunspell import HunSpell  # pylint: disable=no-name-in-module


def pkgfile(path) -> str:
    """Получить путь к файлу пакета."""
    tpath = resource_filename('TextAnalysis', '')
    return os.path.abspath(tpath + '/../' + path)


class Analysis:
    """Объект приложения."""

    def __init__(self, themeFilePath):
        """Создание объекта."""
        self.wordsOccurences = ''
        # Файл с темами
        self.themesFile = themeFilePath
        # Загрузка словаря
        self.spellchecker = HunSpell(
            pkgfile("hunspell/ru_RU.dic"), pkgfile("hunspell/ru_RU.aff"))
        # Проверка и чтение файла с темами
        self.checkThemesFile()
        with open(self.themesFile, encoding="utf-8") as file:
            self.themes = json.load(file)

    def checkThemesFile(self):
        """Проверяем файл для хранения тем."""
        # Если не существует файла с темами или пустой...
        if not os.path.exists(self.themesFile) or \
                os.stat(self.themesFile).st_size == 0:
            # То записываем {}
            with open(self.themesFile, "w", encoding="utf-8") as file:
                file.write("{}")
        return 0

    def getThemesFormatted(self):
        """Красивый вывод всех тем."""
        if len(self.themes.keys()) == 0:
            return "Список тем пуст!"
        answer = "Темы:\n"
        for index, keys in enumerate(self.themes.keys()):
            # i) Название_темы
            answer += str(index + 1) + ") " + str(keys).title() + "\n"
        return answer

    def parseKeyWords(self, theme):
        """Поиск ключевых слов по теме в интернете."""
        page = BeautifulSoup(
            requests.get(
                "https://www.bukvarix.com/keywords/?q=" + theme,
                timeout=30)
            .text,
            "html.parser"
        )
        info = re.findall(
            r'"([\w ]+)"', str(re.findall(r'"data":([\w \S]+)', str(page))[0]))

        answer = []
        for elem in info:
            for i in elem.split():
                if i != theme and i.isnumeric() is False:
                    answer.append(i)
        return answer

    def addTheme(self, theme):
        """Добавление темы в программу."""
        if self.themes.get(theme) is not None:
            print("Тема " + theme + " уже существует!")
            return 1

        # Нарушена грамматика названия темы
        if self.spellchecker.spell(theme) is False:
            print("Тема " + theme + " отклонена: некорректное слово!")
            return 2
        temp = self.spellchecker.suggest(theme)

        # Недостаточно ключевых слов
        if len(temp) < 5:
            print("Тема отклонена: не найдены ключевые слова!")
            return 2
        # Получить ключевые слова
        temp += self.parseKeyWords(theme)
        # Убрать дубликаты
        self.themes[theme] = list(set(temp))
        self.saveThemes()
        print("Тема " + theme + " успешно добавлена!")
        return 0

    def removeTheme(self, theme):
        """Удаление темы из программы."""
        # Если нет темы
        if self.themes.get(theme) is None:
            print("Тема " + theme + " не существует!")
            return 1
        # Убираем тему
        self.themes.pop(theme)
        self.saveThemes()
        print("Тема " + theme + " удалена!")
        return 0

    def parseStringText(self, text):
        """Разделение текста на слова и сохранение частоты появления."""
        # Разделение слов в тексте
        words = re.split('[^a-zа-яё]+', text, flags=re.IGNORECASE)
        self.wordsOccurences = self.countWordsFromText(words)
        return 0

    def parseTextFile(self, inputFile):
        """Получение текста из файла."""
        with open(inputFile, "r", encoding="utf-8") as file:
            self.parseStringText(file.read())
        return 0

    def countWordsFromText(self, words):
        """Подсчет слов в тексте."""
        # Стемминг (забираем слово и добавляем его основу - стем)
        wordsLen = len(words)
        for i in range(wordsLen):  # pylint: disable=unused-variable
            word = words.pop(0)
            stems = self.spellchecker.stem(word)
            # if stems: words +=  list(map(lambda x: x.decode('utf-8'), stems))
            # Добавляем один стем чтобы не удваивать вероятность
            if isinstance(stems, list) and stems:
                words += [stems[0].decode('utf-8')]
            elif isinstance(stems, str) and stems:
                words += [stems.decode('utf-8')]
        # Подсчет кол-ва слов
        return {elem: words.count(elem) for elem in words}

    def findCoincidences(self):
        """Поиск совпадений текста с ключевыми словами тем."""
        wordsOccurences = self.wordsOccurences
        counts = []  # Счетчик слов для каждой темы

        # Проходим по ключевым словам тем
        for keyWords in self.themes.values():
            themeCount = []  # Счетчик слов темы
            for word in keyWords:
                # Слово из текста есть в ключевых словах
                if wordsOccurences.get(word) is not None:
                    themeCount.append(wordsOccurences.get(word))
            counts.append(sum(themeCount))

        countsAll = sum(counts)  # Всего слов которые нашлись в темах
        # Возврат: тема - процент слов
        return dict(zip(list(self.themes.keys()),
                        [round(themeCount / 100 * countsAll)
                         for themeCount in counts]))

    def checkText(self):
        """
        Проверка текста.

        Запуск алгоритма а затем вывод информации к какой теме относится текст
        и с какой вероятностью.
        """
        # Алгоритм
        localdata = self.findCoincidences()
        # Вывод
        textTheme = max(localdata, key=localdata.get).title()
        answer = "\nТема текста: " + textTheme + "\n\n"
        answer += "Общая вероятность по всем темам:\n"
        for key, value in localdata.items():
            answer += "Тема: " + key.title() + " - " + str(value) + "%" + "\n"
        print(answer)
        return textTheme

    def saveThemes(self):
        """Сохранить данные из оперативной памяти в файл тем в конце работы."""
        with open(self.themesFile, "w", encoding="utf-8") as themeFile:
            text = json.dumps(self.themes, ensure_ascii=False)
            themeFile.write(text)


def main(args):
    """Основа приложения. Определяет режим работы."""
    # Флаг использования файлов по умолчанию
    pkgFilesFlag = args['use_local_files']
    # Если не указан файл с темами то используем встроенный
    if pkgFilesFlag in (1, 3):
        args['--themes_file'] = pkgfile(args['--themes_file'])

    # Объект приложения
    obj = Analysis(args['--themes_file'])

    # Добавление темы
    if args['add']:
        obj.addTheme(args['<theme>'])

    # Удаление темы
    elif args['remove']:
        obj.removeTheme(args['<theme>'])

    # Вывод списка тем
    elif args['list']:
        print(obj.getThemesFormatted())

    # Обработка текста
    elif args['text']:
        obj.parseStringText(args['<text>'])
        return obj.checkText()

    # Обработка файла
    else:
        # Если не указан файл с текстом то используем пример
        if pkgFilesFlag in (2, 3):
            args['--input_file'] = pkgfile(args['--input_file'])
        # Если не существует файла с текстом то выходим
        elif not os.path.exists(args['--input_file']):
            print('Файла с текстом не существует')
            sys.exit()
        obj.parseTextFile(args['--input_file'])
        return obj.checkText()
    return 0


if __name__ == "__main__":
    print("Запуск производится только из __main__")
