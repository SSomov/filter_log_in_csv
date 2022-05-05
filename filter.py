import csv
import re

__version__ = "0.1.0"

FD = 'data/'
PATTERN1 = r'Processing IDoc document with number\s(\d{16})'
PATTERN2 = r'Calling server: POST http://BO-(\w{4})'

print("convert csv 1.1")

with open(FD+'list.txt', 'r') as f:
    list_filter = [line.strip() for line in f]

print("list search:", list_filter)
with open(FD+'csv1.csv', "r", newline='', encoding='utf-8') as File:
    reader = csv.reader((line.replace('\0','') for line in File),  delimiter=';')
    #reader = csv.reader(File, delimiter=';')
    data = list(reader)
    for row in data:
        tempstr = []
        for word in list_filter:
            if word in row[7]:
                tempstr.append(word)
        row[7] = " ".join(tempstr)
         # ищем соотвествие PATTERN1, в частности номер в 16 символов
        match = re.search(PATTERN1, row[8])
        if match is not None:
            # если соотвествие есть получаем номер, удаляем лидирующие нули
            # добавляем в 9 столбец строки
            row.append(match[1].lstrip('0'))
            match = re.search(PATTERN2, row[8])
            # ищем соотвествие PATTERN2, в частности номер в 4 символов
            if match is not None:
                row.append(match[1].lstrip('0'))
                # print(row[10])
    with open(FD+'csv2.csv', "w", encoding='utf-8') as output:
        writer = csv.writer(output, delimiter=';', lineterminator='\n')
        for row in data:
            writer.writerow(row)
