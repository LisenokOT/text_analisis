# pylint: disable=invalid-name
# pylint: disable=redefined-outer-name
"""Файл тестов приложения."""
import pytest

from TextAnalysis.main import main

# Сброс файла тем для тестов
with open('./demo_data/default_themes.json', "r", encoding="utf-8") as file:
    text = file.read()
with open('./demo_data/test_themes.json', "w", encoding="utf-8") as file:
    file.write(text)


@pytest.fixture
def userdata():
    """Фикстура: Входные параметры пользователя."""
    return {
        '--themes_file': './demo_data/test_themes.json',
        '--input_file': './demo_data/input.txt',
        '<text>': '',
        '<theme>': '',
        'add': False,
        'remove': False,
        'list': False,
        'text': False,
        'use_local_files': 3  # Использовать файлы по умолчанию
    }


def testRunDefault(userdata):
    """Запуск без параметров."""
    result = main(userdata)
    assert result
    print("Тема: ", result)


def testRunWithString(userdata):
    """Проверка темы своего текста."""
    userdata['text'] = True
    userdata['<text>'] = 'Математика — мой любимый школьный предмет с первого класса. Мне нравится решать примеры и задачи, находить ответы на логические вопросы.'  # pylint: disable=line-too-long
    result = main(userdata)
    assert result
    print("Тема: ", result)


def testAddTheme(userdata):
    """Добавление своей темы."""
    userdata['add'] = True
    userdata['<theme>'] = 'Зима'
    assert main(userdata) == 0


def testDeleteTheme(userdata):
    """Удаление своей темы."""
    userdata['remove'] = True
    userdata['<theme>'] = 'Зима'
    assert main(userdata) == 0


def testListThemes(userdata):
    """Вывод списка тем. Для отображения запускать в дебаге."""
    userdata['list'] = True
    assert main(userdata) == 0
