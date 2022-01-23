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
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))
        
        await client.pair()
        #byte_message = bytes('abc', 'utf-8')
        msg = bytearray()
        msg.extend(map(ord, 'abc'))
        msg = bytes.fromhex('0f0c170000000000000000000018ffff')
        #await client.write_gatt_char('0000fff3-0000-1000-8000-00805f9b34fb', msg)
        #await client.write_gatt_char('0000fff4-0000-1000-8000-00805f9b34fb', byte_message, response=True)

        await client.pair()
        await asyncio.sleep(0.5)
        for service in client.services:
            for char in service.characteristics:
                #if "notify" in char.properties:
                #    print(f"Notification char {char.uuid}")
                    #await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
                #if "write-without-response" in char.properties:
                    #await client.write_gatt_char(char.uuid, msg)
                print(f"Type {char.properties} - UUID {char.uuid} - Handle { char.handle}  ")
        await asyncio.sleep(0.5)
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        await client.write_gatt_char('0000fff3-0000-1000-8000-00805f9b34fb', msg)
        #await client.write_gatt_char(42, msg)
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        await asyncio.sleep(5)
        await client.stop_notify(CHARACTERISTIC_UUID)
        #await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        #await asyncio.sleep(0.5)
        #await client.write_gatt_char('0000fff3-0000-1000-8000-00805f9b34fb',bytes('0f050400000005ffff', 'utf-8'), response=True)
        #await asyncio.sleep(0.5)
        #await client.stop_notify(CHARACTERISTIC_UUID)
        
        #print(f"Connected: {client.is_connected}")
        #model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        #bytes(test_string, 'utf-8')
        #await client.start_notify('0000fff4-0000-1000-8000-00805f9b34fb', callback)
        #await client.write_gatt_char('0000fff3-0000-1000-8000-00805f9b34fb',bytes('0f050400000005ffff', 'utf-8'), response=True) #https://tepette.wordpress.com/2019/04/24/linux-ble-using-hciconfig-hcitool-and-gatttool-to-discover-oximeter-jumper/
        #await asyncio.sleep(0.5)  # Sleeping just to make sure the response is not missed...
        #await client.stop_notify('0000fff4-0000-1000-8000-00805f9b34fb')
        
        #t = await client.read_gatt_descriptor('0000fff6-0000-1000-8000-00805f9b34fb')
        #print("Model Number: {0}".format("".join(map(chr, model_number))))
        #print("Model Number: {0}".format("".join(map(chr, t))))
        await client.disconnect()

asyncio.run(main(address))