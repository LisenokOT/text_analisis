## MAKEFILE #############################################
# Полезные команды:
# make dev 						- Установка DEV версии
# make run p="аргументы" 		- Запуск
# make doc 						- Генерация документации
# make remove 					- Удаление
#########################################################
ifeq ($(OS),Windows_NT)
    OPEN := powershell
else
    UNAME := $(shell uname -s)
    ifeq ($(UNAME),Linux)
        OPEN := xdg-open
    endif
endif
# Сообщение по умолчанию
default:
	@echo Invalid Make Command

# Сборка пакета
build: pep8
	@python setup.py sdist --formats=zip

# Генерация документации
doc: pep8
	@rm -f ./docs/TextAnalysis.rst
	@sphinx-apidoc -o ./docs/ ./TextAnalysis/
	@sphinx-build -b html docs docs/_build/html
	@$(OPEN) ./docs/_build/html/index.html

# Установка
install: build
	@pip install dist/TextAnalysis-1.0.0.zip

# Установка в режиме разработчика
dev:
	@pip install -e .[dev]

# Удаление
remove:
	@pip uninstall TextAnalysis

# Форматирование кода (устарело)
pep8:
	@pip install autopep8
	@python -m autopep8 --in-place --recursive ./TextAnalysis
	@python -m autopep8 --in-place setup.py

# Запуск (p=Параметры)
run:
	@python -m TextAnalysis $(p)

# Тестирование
test:
	@python -m pytest -s ./TextAnalysis/tests/test_main.py::test$(f)

# Пре-коммит
# pre-commit install
pre:
	@pre-commit run --all-files
