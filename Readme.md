# Задача:
Предположим, что данные прилетают в JSON-формате.
В кузов автомашины (длиной L, шириной W, высотой H и погрузочной массой M)
необходимо равномерно по осям подгрузить N грузов, каждый из которых имеет свою
длину, ширину, высоту и массу.

Программа должна запрашивать параметры кузова (L, W, H и М), количество грузов (N),
а также их длину, высоту и ширину. Если суммарный вес грузов превышает погрузочную массу,
то необходимо загрузить оптимально (по максимальной массе размещенных грузов).

Внимание. Грузы размещаются в один ярус(!!!). Допуск примыкания груза 5 см по всем измерениям.
На выходе программа формирует описание, что оптимально загрузить в кузов в первую очередь.

# Принятые решения
1. Сначала выбирается группа грузов с максимальной общей массой, но не превосходящая
   грузоподъемность кузова грузовика.
2. Проверяем группу по высоте всех грузов, чтобы максимальная высота груза была не более 
   высоты кузова. Считаем, что наклонять груз нельзя.
3. Проверяем общую занимаемую площадь груза - она не должна превышать площадь кузова
4. Если длина или ширина груза больше его ширины или длины и при этом ширина кузова больше
   этой длины или ширины, то мы поворачиваем груз в горизонтальной плоскости на 90'.
5. Проверка, что общая длина грузов (с допусками), а также максимальная ширина одного из грузов
   (с допусками) входят в длину и ширину кузова.

# Как запустить
1. Скачиваем все файлы репозитория
2. Запускаем main.py

# Что делать
1. При запуске программы вам будет предложено ввести параметры грузовика:
   имя грузовика --- любой текст
   L,W,H грузовика (длина, ширина, высота (мм)) --- число
   М грузовика (масса (кг))--- число
2. Если ничего не будет введено (вообще), то будут присвоены значения по умолчанию
   'a225df', 3000, 2000, 2000, 11
3. Вам будет предложено ввести имя файла json, откуда считывать данные о грузах
   Если ничего не будет введено, то будет использован файл по умолчанию
   items.json
4. Программа отработает по принятым фильтрам и выведет на экран первую подходящую комбинацию грузов.