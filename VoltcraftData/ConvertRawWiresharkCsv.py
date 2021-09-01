import csv

def ReturnVoltCraftObject( str ):
    #0f11040001006915e8009b3200000000000039
    if len(str) == 38:
        Wattage = int(str[12:-22], 16)/1000
        Voltage = int(str[16:-20], 16)
        Current = int(str[18:-16], 16)/100
        Frequency = int(str[22:-14], 16)
        return Wattage, Voltage, Current, Frequency
    else:
        raise Exception("Input length is not 38")


with open('VoltcraftData\Wireshark Voltcraft Export.csv') as csvFile:
    for index, row in enumerate(csv.reader(csvFile, delimiter=',')):
        if index > 0 and row[2] != 'Master_0xb7d465a0' and len(row[11]) == 38:
            print(f'Row {index}, Source {row[2]}')
            Wattage, Voltage, Current, Frequency = ReturnVoltCraftObject(row[11])
            print(f'Watt {Wattage} W, Voltage {Voltage} V, Current {Current} A, Frequency {Frequency} Hz')