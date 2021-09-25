import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from VoltCraftService import VoltCraftSeM6000

ble = adafruit_ble.BLERadio()
found = set()

for entry in ble.start_scan(ProvideServicesAdvertisement, timeout=60, minimum_rssi=-80):
    name = entry.complete_name
    if not name:
        continue
    if name == "Voltcraft":
        print(f'{name} found')
        if VoltCraftSeM6000 in entry.services:
            print(f'VoltCraftSeM6000 Service found')
        Voltcraft = ble.connect(entry, timeout=10)
        print(f'Connected')
        ble.stop_scan()
        break
    
voltcraft_service = Voltcraft[VoltCraftSeM6000]
voltcraft_service.data

if Voltcraft.connected:
    Voltcraft.disconnect()
    print(f'Disconnected')