def read():
    themes = {"футбол": ["тут","футбол", "матч", "спорт", "мяч", "поле", "лига", "чемпионат", "аргентина", "счет", "гол", "футболист"],
    "физика": ["прямо", "физика", "ученые", "наука", "законы", "квантовая", "тело", "механика"]}
    with open('file.txt', "r", encoding="utf-8") as file:
        r = file.read().replace(',', '').replace('.', '').split(" ")
    data = {elem: r.count(elem) for elem in r}
    # temp_1 = sum([value for key, value in data.items() if key in themes["футбол"]])
    # temp_2 = sum([value for key, value in data.items() if key in themes["физика"]])
    # print(temp_1, temp_2)
    # tem = [keys for keys in themes.keys()]
    # count = [sum([value for key, value in data.items() if key in themes.get(keyses) for keyses in tem])]
    counts = []
    for arr in themes.values():
        temp = []
        for elem in arr:
            if data.get(elem) is not None:
                temp.append(data.get(elem))
        counts.append(sum(temp))
    #print(count)
    print(counts)

# def distan():
#     t = {"one": [1, 2, 3], "two": [2, 3, 4], "tree": [3, 4, 5]}
#     r = t.values()
#     print(r)

def main():
    read()


if __name__ == "__main__":
    main()
