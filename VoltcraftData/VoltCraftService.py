from typing import ClassVar
import _bleio
from adafruit_ble import uuid
from adafruit_ble.services import Service
from adafruit_ble.uuid import StandardUUID
from adafruit_ble.characteristics import Characteristic, ComplexCharacteristic
from adafruit_ble.characteristics.int import Uint8Characteristic

#https://github.com/adafruit/Adafruit_CircuitPython_BLE_Heart_Rate/blob/main/adafruit_ble_heart_rate.py
#https://github.com/adafruit/Adafruit_CircuitPython_BLE/tree/main/adafruit_ble
#https://github.com/adafruit/Adafruit_CircuitPython_BLE_BerryMed_Pulse_Oximeter/

#https://github.com/adafruit/Adafruit_CircuitPython_BLE_Adafruit/tree/main/adafruit_ble_adafruit

class VoltCraftSeM6000(Service):
    uuid = StandardUUID(0xFFF0)

    device_data = Uint8Characteristic(uuid=(StandardUUID(0X002B)), properties = Characteristic.WRITE)

    #device_data.

    def __init__(self, service=None):
        super().__init__(service=service)
        
    @property
    def data(self):
        try:
            return self.device_data
        except IndexError:
            return "InvalidLocation"