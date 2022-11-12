import os
import json
import re
from hunspell import HunSpell


class Analysis:
    def __init__(self):
        self.spellchecker = HunSpell("hunspell/ru_RU.dic", "hunspell/ru_RU.aff")
        self.checkFiles()
        with open('themes.json') as file:
            self.themes = json.load(file)
        self.dataOfText = self.read()

    def checkFiles(self):
        if not os.path.exists("input.txt"):
            os.mknod("input.txt")
        if not os.path.exists("themes.json") or os.stat("themes.json").st_size == 0:
            with open("themes.json", "w") as file:
                file.write("{}")

    def printThemes(self):
        if len(self.themes.keys()) == 0:
            return "Список тем пуст!"
        answer = "Темы:\n"
        for index, keys in enumerate(self.themes.keys()):
            answer += "  " + str(index + 1) + ") " + str(keys).title() + "\n"
        return answer

    def addTheme(self, theme):
        if self.themes.get(theme) != None:
            return "Тема " + theme + " уже существует!"

        if self.spellchecker.spell(theme) is False:
            return "Тема " + theme + " отклонена: некорректное слово!"
        temp = self.spellchecker.suggest(theme)
        if len(temp) < 10:
            return "Тема отклонена: не найдены ключевые слова!"
        
        self.themes[theme] = temp
        return "Тема: " + theme + " успешно добавлена!"
    
    def removeTheme(self, theme):
        if self.themes.get(theme) == None:
            return "Тема " + theme + " не существует!"
        self.themes.pop(theme)
        return "Тема: " + theme + " удалена!"

    def findCoincidences(self):
        counts = []
        for arr in self.themes.values():
            temp = []
            for elem in arr:
                if self.dataOfText.get(elem) is not None:
                    temp.append(self.dataOfText.get(elem))
            counts.append(sum(temp))
        countsAll = sum(counts)
        return dict(zip(list(self.themes.keys()), [str(round(elem * 100 / countsAll)) + "%" for elem in counts]))

    def read(self):
        with open('input.txt', "r", encoding="utf-8") as file:
            r = re.split('[^a-zа-яё]+', file.read(), flags=re.IGNORECASE)
        return {elem: r.count(elem) for elem in r}

    def checkText(self):
        localdata = self.findCoincidences()
        answer = "Тема текста: " + list(localdata.keys())[0].title() + "\n\n"
        answer += "Общая вероятность по всем темам:\n"
        for key, value in localdata.items():
            answer += "  Тема: " + key.title() + " - " + value + "\n"
        return answer

    def __del__(self):
        with open('themes.json', "w") as outfile:
            outfile.write(json.dumps(self.themes))


def main():
    data = Analysis()
    print(data.checkText())

if __name__ == "__main__":
    main()
