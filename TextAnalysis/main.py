import os
import json
import re
import requests
from hunspell import HunSpell
from bs4 import BeautifulSoup
from pkg_resources import resource_filename


def pkgfile(path) -> str:
    """Получить файл пакета"""
    tpath = resource_filename('TextAnalysis', '../')
    return os.path.abspath(tpath + path)


class Analysis:
    def __init__(self, args):
        # Пользовательские файлы
        self.themes_file = args['--themes_file']
        self.input_file = args['--input_file']
        # Флаг использования файлов по умолчанию
        pkg_files_flag = args['use_local_files']
        # Не указан файл с темами
        if pkg_files_flag == 1 or pkg_files_flag == 3:
            self.themes_file = pkgfile(args['--themes_file'])
        # Не указан файл с текстом
        if pkg_files_flag == 2 or pkg_files_flag == 3:
            self.input_file = pkgfile(args['--input_file'])
        self.spellchecker = HunSpell(
            pkgfile("hunspell/ru_RU.dic"), pkgfile("hunspell/ru_RU.aff"))
        self.checkFiles()
        with open(self.themes_file) as file:
            self.themes = json.load(file)
        self.dataOfText = self.read()

    def checkFiles(self):
        """ Проверяем наличие файлов для ввода текста и для хранения тем """
        if not os.path.exists(self.input_file):
            os.mknod(self.input_file)
        if not os.path.exists(self.themes_file) or os.stat(self.themes_file).st_size == 0:
            with open(self.themes_file, "w", encoding="utf-8") as file:
                file.write("{}")

    def printThemes(self):
        """ Красивый вывод всех тем, что заданы программе """
        if len(self.themes.keys()) == 0:
            return "Список тем пуст!"
        answer = "Темы:\n"
        for index, keys in enumerate(self.themes.keys()):
            answer += "  " + str(index + 1) + ") " + str(keys).title() + "\n"
        return answer

    def parseKeyWords(self, theme):
        """ Поиск ключевых слов по теме в интернете """
        page = BeautifulSoup(requests.get(
            "https://www.bukvarix.com/keywords/?q=" + theme).text, "html.parser")
        info = re.findall(
            '"([\w ]+)"', str(re.findall('"data":([\w \S]+)', str(page))[0]))

        answer = list()
        for elem in info:
            for i in elem.split():
                if i != theme and i.isnumeric() is False:
                    answer.append(i)
        return answer

    def addTheme(self, theme):
        """ Добавление темы в программу """
        if self.themes.get(theme) != None:
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
        """ Удаление темы из программы """
        if self.themes.get(theme) == None:
            return "Тема " + theme + " не существует!"
        self.themes.pop(theme)
        return "Тема: " + theme + " удалена!"

    def findCoincidences(self):
        """ Поиск совпадений текста с темами """
        counts = []
        for arr in self.themes.values():
            temp = []
            for elem in arr:
                if self.dataOfText.get(elem) is not None:
                    temp.append(self.dataOfText.get(elem))
            counts.append(sum(temp))
        countsAll = sum(counts)
        if countsAll == 0:
            countsAll = 1
        return dict(zip(list(self.themes.keys()), [round(elem * 100 / countsAll) for elem in counts]))

    def read(self):
        """ Чтение текста из файла """
        with open(self.input_file, "r", encoding="utf-8") as file:
            r = re.split('[^a-zа-яё]+', file.read(), flags=re.IGNORECASE)
        return {elem: r.count(elem) for elem in r}

    def checkText(self):
        """ Вывод информации к какой теме относится текст и с какой вероятностью """
        localdata = self.findCoincidences()
        answer = "\nТема текста: " + \
            max(localdata, key=lambda k: localdata.get(k)).title() + "\n\n"
        answer += "Общая вероятность по всем темам:\n"
        for key, value in localdata.items():
            answer += "  Тема: " + key.title() + " - " + str(value) + "%" + "\n"
        return answer

    def __del__(self):
        """ В конце работы программы мы осуществляем запись данных из оперативной памяти в файл с темами """
        with open(self.themes_file, "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(self.themes))


def main(args):
    data = Analysis(args)
    # print(data.printThemes())
    print(data.checkText())


if __name__ == "__main__":
    main()
