import asyncio
from bleak import BleakClient, cli

address = "B0:B1:13:71:C8:E9"
#MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb" #reads model > https://github.com/JorenSix/TgForceSensor
MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"

#"0000fff0-0000-1000-8000-00805f9b34fb"
#0x002b 0f050400000005ffff

def callback(sender, data):
    print(f"{sender}: {data}")

async def main(address):
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")
        #model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        #bytes(test_string, 'utf-8')
        await client.start_notify('0000fff4-0000-1000-8000-00805f9b34fb', callback)
        await client.write_gatt_char('0000fff3-0000-1000-8000-00805f9b34fb',bytes('0f050400000005ffff', 'utf-8'), response=True) #https://tepette.wordpress.com/2019/04/24/linux-ble-using-hciconfig-hcitool-and-gatttool-to-discover-oximeter-jumper/
        await asyncio.sleep(0.5)  # Sleeping just to make sure the response is not missed...
        await client.stop_notify('0000fff4-0000-1000-8000-00805f9b34fb')
        
        #t = await client.read_gatt_descriptor('0000fff6-0000-1000-8000-00805f9b34fb')
        #print("Model Number: {0}".format("".join(map(chr, model_number))))
        #print("Model Number: {0}".format("".join(map(chr, t))))

asyncio.run(main(address))