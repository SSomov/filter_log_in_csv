import csv
import re

__version__ = "0.2.1"
FD: str = 'data/'
SEARCH_COL: int = 8
PATTERN_FILE: str = 'list.txt'
PATTERN_FILE_IN: str = 'csv1.csv'
PATTERN_FILE_OUT: str ='csv2.csv'
PATTERN1: re.Pattern = re.compile(r'Processing IDoc document with number\s(\d{16})')
PATTERN2: re.Pattern = re.compile(r'Calling server: POST http://BO-(\w{4})')

print(__version__)

with open(FD+'list.txt', 'r', encoding='utf-8') as f:
    list_filter = [line.strip() for line in f]

print("list search:", list_filter)

with open(FD+PATTERN_FILE_IN, "r", newline='', encoding='utf-8') as File:
    reader = csv.reader((line.replace('\0', '')
                        for line in File),  delimiter=';')
    #reader = csv.reader(File, delimiter=';')
    data = list(reader)
    for row in data:
        tempstr: list = []
        for word in list_filter:
            if word in row[SEARCH_COL]:
                tempstr.append(word)
        # ищем соотвествие PATTERN1, в частности номер в 16 символов
        match = re.search(PATTERN1, row[SEARCH_COL])
        if match is not None:
            # если соотвествие есть получаем номер, удаляем лидирующие нули
            # добавляем в 9 столбец строки
            row.append(match[1].lstrip('0'))
        else:
            row.append('')
        # ищем соотвествие PATTERN2, в частности номер в 4 символа
        match = re.search(PATTERN2, row[SEARCH_COL])
        if match is not None:
            row.append(match[1].lstrip('0'))
            # print(row[10])
        # перезаписываем строку с данными паттернами
        row[SEARCH_COL] = " ".join(tempstr)
    with open(FD+PATTERN_FILE_OUT, "w", encoding='utf-8') as output:
        writer = csv.writer(output, delimiter=';', lineterminator='\n')
        for row in data:
            writer.writerow(row)
