import asyncio
from bleak import BleakClient, cli

address = "B0:B1:13:71:C8:E9"
#MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb" #reads model > https://github.com/JorenSix/TgForceSensor
MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"

#"0000fff0-0000-1000-8000-00805f9b34fb"
#0x002b 0f050400000005ffff
BASE_UUID = "0000{}-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"
SENDCHAR = '0000fff3-0000-1000-8000-00805f9b34fb'

def callback(sender, data):
    print(f"{sender}: {data}")

def notification_handler(sender, data, debug=False):
    """Simple notification handler which prints the data received."""
    #print("{0}: {1}".format(sender, data))
    print("Handling...")
    print("Data is " + str(type(data)))
    array = bytearray(data)
    
async def main(address):

    async with BleakClient(address) as client:
        x = await client.is_connected()
        print(f"Connected: {x}")

        MODEL_NBR_UUID = BASE_UUID.format("2a24")
        WRITE_WITHOUT_NOTIFY = BASE_UUID.format("fff3")

        #Some reference code to get some output next to connect
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

        #Next part just prints all characteristics (For Science)
        #for service in client.services:
            #for char in service.characteristics:
                #print(f"Type {char.properties} - UUID {char.uuid} - Handle { char.handle}  ")

        await asyncio.sleep(0.5)
        #await client.start_notify(CHARACTERISTIC_UUID, notification_handler) #Enables the responce function
        await client.write_gatt_char(WRITE_WITHOUT_NOTIFY, bytes.fromhex('0f0c170000000000000000000018ffff'))
        await asyncio.sleep(5)
        #await client.stop_notify(CHARACTERISTIC_UUID) # Disables the responce function
        
        await client.disconnect()

asyncio.run(main(address))