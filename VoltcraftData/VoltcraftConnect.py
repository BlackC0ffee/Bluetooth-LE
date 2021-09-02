import adafruit_ble

ble = adafruit_ble.BLERadio()
found = set()

for entry in ble.start_scan(timeout=60, minimum_rssi=-80):
    name = entry.complete_name
    if not name:
        continue
    if name == "Voltcraft":
        print(f'{name} found')
        Voltcraft = ble.connect(entry, timeout=10)
        print(f'Connected')
        break

if Voltcraft.connected:
    Voltcraft.disconnect()
    print(f'Disconnected')
