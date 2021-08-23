import csv

with open('VoltcraftData\Wireshark Voltcraft Export.csv') as csvFile:
    for index, row in enumerate(csv.reader(csvFile, delimiter=',')):
        if index > 0 and row[2] != 'Master_0xb7d465a0':
            print(f'Row {index}, Source {row[2]}, Value {row[11 ]}')