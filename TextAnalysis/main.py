"""Основной файл программы."""
import json
import os
import sys
import re

import requests
from bs4 import BeautifulSoup
from pkg_resources import resource_filename

from hunspell import HunSpell  # pylint: disable=no-name-in-module


def pkgfile(path) -> str:
    """Получить файл пакета."""
    tpath = resource_filename('TextAnalysis', '../')
    return os.path.abspath(tpath + path)


class Analysis:
    """Объект приложения."""

    def __init__(self, args):
        """Создание объекта."""
        # Пользовательские файлы
        self.themesFile = args['--themes_file']
        self.inputFile = args['--input_file']
        # Флаг использования файлов по умолчанию
        pkgFilesFlag = args['use_local_files']
        # Не указан файл с темами
        if pkgFilesFlag == 1 or pkgFilesFlag == 3:
            self.themesFile = pkgfile(args['--themes_file'])
        # Не указан файл с текстом
        if pkgFilesFlag == 2 or pkgFilesFlag == 3:
            self.inputFile = pkgfile(args['--input_file'])
        # Загрузка словарей
        self.spellchecker = HunSpell(
            pkgfile("hunspell/ru_RU.dic"), pkgfile("hunspell/ru_RU.aff"))
        # Проверка и чтение входных файлов
        self.checkFiles()
        with open(self.themesFile, encoding="utf-8") as file:
            self.themes = json.load(file)

    def checkFiles(self):
        """Проверяем наличие файлов для ввода текста и для хранения тем."""
        # Если не существует файла с текстом
        if not os.path.exists(self.inputFile):
            # То выходим
            print('Файла с текстом не существует')
            sys.exit()
        # Если не существует файла с темами...
        if not os.path.exists(self.themesFile) or \
                os.stat(self.themesFile).st_size == 0:
            # То создаем пустой
            with open(self.themesFile, "w", encoding="utf-8") as file:
                file.write("{}")

    def getThemesFormatted(self):
        """Красивый вывод всех тем, что заданы программе."""
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

        answer = list()
        for elem in info:
            for i in elem.split():
                if i != theme and i.isnumeric() is False:
                    answer.append(i)
        return answer

    def addTheme(self, theme):
        """Добавление темы в программу."""
        if self.themes.get(theme) is not None:
            return "Тема " + theme + " уже существует!"

        if self.spellchecker.spell(theme) is False:
            return "Тема " + theme + " отклонена: некорректное слово!"
        temp = self.spellchecker.suggest(theme)
        if len(temp) < 5:
            return "Тема отклонена: не найдены ключевые слова!"
        temp += self.parseKeyWords(theme)
        self.themes[theme] = list(set(temp))
        return "Тема: " + theme + " успешно добавлена!"

    def removeTheme(self, theme):
        """Удаление темы из программы."""
        if self.themes.get(theme) is None:
            return "Тема " + theme + " не существует!"
        self.themes.pop(theme)
        return "Тема: " + theme + " удалена!"

    def findCoincidences(self):
        """Поиск совпадений текста с темами."""
        # Подсчет слов
        wordsOccurences = self.countWordsFromText()
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

    def countWordsFromText(self):
        """Чтение текста из файла и подсчет слов в нем."""
        with open(self.inputFile, "r", encoding="utf-8") as file:
            # Разделение слов в тексте
            words = re.split('[^a-zа-яё]+', file.read(), flags=re.IGNORECASE)
        # Стемминг (забираем слово и добавляем его основы)
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

    def checkText(self):
        """
        Проверка текста.

        Запуск алгоритма а затем вывод информации к какой теме относится текст
        и с какой вероятностью.
        """
        # Алгоритм
        localdata = self.findCoincidences()
        # Вывод
        answer = "\nТема текста: " + \
            max(localdata, key=localdata.get).title() + "\n\n"
        answer += "Общая вероятность по всем темам:\n"
        for key, value in localdata.items():
            answer += "Тема: " + key.title() + " - " + str(value) + "%" + "\n"
        return answer

    def __del__(self):
        """Сохранить данные из оперативной памяти в файл тем в конце работы."""
        with open(self.themesFile, "w", encoding="utf-8") as themeFile:
            text = json.dumps(self.themes, ensure_ascii=False)
            themeFile.write(text)


def main(args):
    """Основа приложения."""
    obj = Analysis(args)
    # print(object.getThemesFormatted())
    print(obj.checkText())


if __name__ == "__main__":
    print("Запуск производится только из __main__")
