import asyncio
import binascii
from bleak import BleakClient

address = "B0:B1:13:71:C8:E9"

BASE_UUID = "0000{}-0000-1000-8000-00805f9b34fb"

MODEL_NBR_UUID = BASE_UUID.format("2a24") #reads model > https://github.com/JorenSix/TgForceSensor
WRITE_WITHOUT_NOTIFY = BASE_UUID.format("fff3")
CHARACTERISTIC_UUID = BASE_UUID.format("fff4")

def ReturnVoltCraftObject( str ):
    #0f11040001006915e8009b3200000000000039
    if len(str) == 38:
        Wattage = int(str[12:-22], 16)/1000
        Voltage = int(str[16:-20], 16)
        Current = int(str[18:-16], 16)/1000
        #Current = str[18:-16]
        Frequency = int(str[22:-14], 16)
        return Wattage, Voltage, Current, Frequency
    else:
        raise Exception("Input length is not 38")

def notification_handler(sender, data):
    Wattage, Voltage, Current, Frequency = ReturnVoltCraftObject(binascii.hexlify(bytearray(data)).decode('ascii'))
    print(f'Watt {Wattage} W, Voltage {Voltage} V, Current {Current} A, Frequency {Frequency} Hz')
    
async def main(address):

    async with BleakClient(address) as client:

        #Some reference code to get some output next to connect
        print(f"Connected: {client.is_connected}")
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

        #Next part just prints all characteristics (For Science)
        #for service in client.services:
            #for char in service.characteristics:
                #print(f"Type {char.properties} - UUID {char.uuid} - Handle {char.handle} ")

        #await client.write_gatt_char(WRITE_WITHOUT_NOTIFY, bytes.fromhex('0f0c170000000000000000000018ffff')) #TODO - The Numbers Mason! What do they Mean?
        await asyncio.sleep(1)
        await client.write_gatt_char(WRITE_WITHOUT_NOTIFY, bytes.fromhex('0f0c0100152716120807e500005affff')) #Instruction Blue Blink light turns solid Green
        await asyncio.sleep(0.5)

        await client.start_notify(CHARACTERISTIC_UUID, notification_handler) #Enables the notify function
        await asyncio.sleep(0.5)
        await client.write_gatt_char(WRITE_WITHOUT_NOTIFY, bytes.fromhex('0f050400000005ffff'))
        await asyncio.sleep(0.5)
        await client.stop_notify(CHARACTERISTIC_UUID) # Disables the responce function
        await client.disconnect()

asyncio.run(main(address))