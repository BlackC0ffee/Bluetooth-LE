#Based on https://github.com/adafruit/Adafruit_CircuitPython_BLE_Contec_Pulse_Oximeter.git

class TransparentUARTService(Service):
    uuid = VendorUUID("49535343-FE7D-4AE5-8FA9-9FAFD205E455")
    _server_tx = StreamOut(
        uuid=VendorUUID("49535343-1E4D-4BD9-BA61-23C647249616"),
        timeout=1.0,
        buffer_size=64,
    )
    _server_rx = StreamIn(
        uuid=VendorUUID("49535343-8841-43F4-A8D4-ECBE34729BB3"),
        timeout=1.0,
        buffer_size=64,
    )


    0000fff0-0000-1000-8000-00805f9b34fb