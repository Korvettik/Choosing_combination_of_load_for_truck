# Предположим, что данные прилетают через POST-запрос в JSON-формате.
# В кузов автомашины (длиной L, шириной W, высотой H и погрузочной массой M)
# необходимо равномерно по осям подгрузить N грузов, каждый из которых имеет свою
# длину, ширину, высоту и массу.

# Программа должна запрашивать параметры кузова (L, W, H и М), количество грузов (N),
# а также их длину, высоту и ширину. Если суммарный вес грузов превышает погрузочную массу,
# то необходимо загрузить оптимально (по максимальной массе размещенных грузов).

# Внимание. Грузы размещаются в один ярус(!!!). Допуск примыкания груза 5 см по всем измерениям.
# На выходе программа формирует графическое представление того, как расположены грузы
# (для наглядности на схеме указывать Гр1….ГрN). Если имеются грузы, которые не могут быть
# погружены в силу ограничений кузова, то необходимо вывести список

import json
import copy

items_lst = list()


# ------------- классы -------------------
class Truck:
    def __init__(self, name, L, W, H, M):
        self.name = name
        self.L = int(L)
        self.W = int(W)
        self.H = int(H)
        self.M = int(M)
        self.V = self.L * self.W * self.H

    def __repr__(self):
        return str(self.name)


class Item:
    def __init__(self, name, L, W, H, M):
        self.name = name
        self.L = int(L)
        self.W = int(W)
        self.H = int(H)
        self.M = int(M)
        self.V = self.L * self.W * self.H

    def __repr__(self):
        return str(self.name)


# ----- получение данных и их обработка ----------
tr_name = input('Введите имя грузовика: ')
tr_l = input('Введите L грузовика: ')
tr_W = input('Введите W грузовика: ')
tr_H = input('Введите H грузовика: ')
tr_M = input('Введите M грузовика: ')

if tr_name == tr_l == tr_W == tr_H == tr_M == '':
    print('Вы не ввели никаких параметров. Устанавливаются значения по умолчанию (в мм):\na225df, 2000, 2000, 2000, 50\n')
    truck = Truck('a225df', 2000, 2000, 2000, 11)
else:
    truck = Truck(tr_name, tr_l, tr_W, tr_H, tr_M)

p = input('Введите имя json файла с данными о грузе: ')
if p == '':
    print('Вы не указали имя файла. Устанавливается значение по умолчанию:\nitems.json\n')
    path = 'items.json'
else:
    path = str(p)

with open(path, 'r') as f:
    data = json.loads(f.read())
    for i in data:
        item = Item(i['name'], i['L'], i['W'], i['H'], i['M'])
        items_lst.append(item)



# ----- функции загрузки грузовика ------
def items_by_mass(items_lst: list) -> list:  ##### можно переделать сразу на словарь, где ключи - имена
    '''Формирует список списков, у которых 0 индекс - общая масса, 1 индекс - КОМБИНАЦИя списка грузов'''
    res = list()  # список списков [[1,[a]], [2,[a, b]]]
    box = list()  # список масса, комбинация [2, [a, b]]
    combination = list()  # список комбинации [a, b]

    # проход общий с 1 элементом
    for item in items_lst:
        combination.append(item)
        curent_combination = copy.deepcopy(combination)
        box.append(mass_of_group(curent_combination))  # 0 элемент масса
        box.append(curent_combination)  # 1 элемент комбинация
        res.append(box)
        box = list()

    # собрать одиночки кроме 1
    for item in items_lst[1:]:
        combination = list()
        combination.append(item)
        box.append(mass_of_group(combination))  # 0 элемент масса
        box.append(combination)  # 1 элемент комбинация
        res.append(box)
        box = list()

    # собрать все остальные с выдергиванием по проходу
    for i in range(len(items_lst)):
        current_item_lst = copy.deepcopy(items_lst)
        del current_item_lst[i]
        combination = list()
        box = list()
        for item in current_item_lst:
            combination.append(item)
            curent_combination = copy.deepcopy(combination)
            box.append(mass_of_group(curent_combination))  # 0 элемент масса
            box.append(curent_combination)  # 1 элемент комбинация
            res.append(box)
            box = list()

    # добавляем 1 и последнюю
    box = list()
    combination = list()
    combination.append(items_lst[0])
    combination.append(items_lst[-1])
    box.append(mass_of_group(combination))  # 0 элемент масса
    box.append(combination)  # 1 элемент комбинация
    res.append(box)

    # добавляем предпоследний и последнюю
    box = list()
    combination = list()
    combination.append(items_lst[-2])
    combination.append(items_lst[-1])
    box.append(mass_of_group(combination))  # 0 элемент масса
    box.append(combination)  # 1 элемент комбинация
    res.append(box)

    # удаляем повторные комбинации
    res_dct = dict()
    for comb in res:
        text = ''
        for obj in comb[1]:
            text += obj.name
        res_dct[text] = comb

    my_list = list(res_dct.values())
    # print(f'результат {my_list}')

    return my_list

def items_with_max_mass(res: list) -> list:
    '''Возвращает список грузов с максимальной общей массой'''
    max_mass_box_key = max(map(lambda x: x[0], res))
    for i in res:
        if i[0] == max_mass_box_key:
            return i



def mass_of_group(res: list) -> int:
    '''Считает общую массу грузов в списке'''
    return sum(map(lambda x: x.M, res))


def item_max_h_from_group(group: list) -> int:
    '''Находит максимальную высоту в группе'''
    return max(map(lambda x: x.H, group))

def s_of_group(group: list) -> int:
    '''Находит общую площадь группы в горизонтальной плоскости,
    с учетом допусков (5 см). Считаем, что коробки стоят в одну линию,
    между ними 50мм, а также 50мм до бортов грузовика'''
    s = sum(map(lambda x: x.L * x.W, group)) + truck.W * 50 * (len(group)+1) + truck.L * 50 * 2
    return s


# ----- алгоритм загрузки грузовика ----------------

items_by_mass_lst = items_by_mass(items_lst)  # список списков [масса, [группа]]
print(items_by_mass_lst)

flag = True
while flag:
    group = items_with_max_mass(items_by_mass_lst)
    group_mas = group[0]

    print(group_mas, group)

    # УСЛОВИЕ ЗАДАЧИ - выбрать группу по МАКСИМАЛЬНОЙ возможной массе
    if truck.M >= group_mas:  # Все ОК

        # Фильтруем группу по высоте. СЧИТАЕМ, ЧТО наклонять груз НЕЛЬЗЯ
        max_h_from_group = item_max_h_from_group(group[1])
        if truck.H >= max_h_from_group: #Все ОК

            # Проверяем группу на габариты в горизонтальной плоскости
            tr_s = truck.L * truck.W
            if tr_s >= s_of_group(group[1]):  # есть шанс все уместить

                # ЗДЕСЬ ЛОГИКА ПОВОРОТОВ В ГОРИЗОНТАЛЬНОЙ ПЛОСКОСТИ
                print(f'ты здесь {group_mas, group}')

                flag = False

            else: # нет шанса уместить
                items_by_mass_lst.remove(group)

        else: # убрать группу с максимальной массой и не проходящей по высоте
            items_by_mass_lst.remove(group)

    else:  # убрать группу с максимальной массой
        items_by_mass_lst.remove(group)

    if len(items_by_mass_lst) == 0:
        flag = False
        print('Груз не соответствует ни массе, ни габаритам. Выберите другой груз.')






