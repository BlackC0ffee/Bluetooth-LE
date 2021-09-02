# Bluetooth Low Energy Shizzle

This document provides some documentation related to some prototyping I did around Bluetooth Low Energy

## Analyzing BLE device

This document describes the basic steps for connecting with a BLE device and how to read/manipulate information from it.

### Prerequisites

1. A BLE device
2. A Linux Machine with a bluetooth adapter (e.g. Rpi)

### Connecting and reading the data

Assuming you already have setup a Linux device and have a BLE device in your reach. The first step is to find you Bluetooth device on your linux machine. This can be done with the `hciconfig` command:

![hciconfig output](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/hciconfig.png?raw=true)

As you can see the **hci0** is our bluetooth adapter on our machine. Using the hcitool we can scan for BLE devices using the command `sudo hcitool -i hci0 lescan`:

![hcitool -i hci0 lescan: output](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/hcitool-lescan.png?raw=true)

The device we want to connect to is B0:B1:13:71:C8:E9 which is a "smart power socket". This can be performed using the gatttool and the command `sudo gatttool -i hci0 -b B0:B1:13:71:C8:E9 -I`

Next you need to connect to the device using the command `connect`

![gatttool -i hci0 -b B0:B1:13:71:C8:E9 -I](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/gatttool-connect.png?raw=true)

Once connected you can read the primary profiles using the command `primary`

![Primary output](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/primary.png?raw=true)

#### UUID Numbers [^1]

The four last numbers of the first block are referring to the services specified by Bluetooth

- 1800 = Generic Access
- 1801 = Generic Attribute
- 180a = Device Information
- fff0 = Not a standard UUID Number

## Sniffing BLE

In our previous example we noticed that the Voltcraft power socket was using their own standard to communicate over Bluetooth. In this step we will capture (sniff) the traffic and try to reverse engineer the data.

### Prerequisites

1. A windows (or Linux) machine
1. A [nRF52840 Dongle](https://www.nordicsemi.com/Products/Development-hardware/nRF52840-Dongle)
1. [Uploaded and configured sniffer environment](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fug_sniffer_ble%2FUG%2Fsniffer_ble%2Fintro.html)

### Connect and sniff the data

Start Wireshark and listen to the traffic using the nRF52840 Dongle. Select the device you want to sniff **before** you connect to the device using the android app.

![Selecting the BLE Device](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/wireshark-selectble.png?raw=true)

Capture the data and use a filter `btatt.value` to filter the package that contain data. In the picture you can see the Service ID fff0 that we had discovered in the previous part. As we want to export the data, we configure it as a column.

![Filtered BLE data](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/wireshark-setcolumn.png?raw=true)

Select the packets that are needed and export them in a csv format.

![Export to CSV](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/wireshark-exporttocsv.png?raw=true)

Opening the CSV, you can notice a pattern

![Excel pattern](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/Excel-csvpattern.png?raw=true)

The master sends `0x0f050400000005ffff` and receives data back that isn't completely random.

During the capture a picture was taken from the mobile app and the csv data is filtered so only the slave data is kept. The numbers in the picture are also converted to hexadecimal values and checking the data we are able to find the line that contains the data.

![Decoding the Hex Data](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/decode-hex-data.png?raw=true)

The first part is probably a key to identify the device and the last part is probably some sort of value to calculate the power factor.

### Test one - convert raw csv data to human readable format

Running `ConvertRawWiresharkCsv.py`, converts the csv values to human readable format

![ConvertRawWiresharkCsv.py output](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/ConvertRawWiresharkCsv_py-to-text.png?raw=true)

### Test two - send command to device

Start scan using Wireshark and connect to the device using a `sudo gatttool -i hci0 -b B0:B1:13:71:C8:E9 -I` and connect using the command `connect`

Sending character write request `char-write-req 0x002b 0f050400000005ffff` results in a succesfull reply and can be confirmed in Wireshark

![Test two output](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/gatttool-char-write-req.png?raw=true)

![Test two output - wireshark](https://github.com/BlackC0ffee/Bluetooth-LE/blob/master/Media/wireshark-char-write-req.png?raw=true)

### Test tree - Connect using python script

On the Rpi Add user to the correct groups

```bash
sudo usermod -a -G bluetooth $USER
sudo reboot
```

Install the required libraries with `pip3 install --upgrade adafruit-blinka-bleio adafruit-circuitpython-ble`

Connect using `VoltcraftConnect.py`

## Resources

- [Adafruit - Introduction to Bluetooth Low Energy](https://learn.adafruit.com/introduction-to-bluetooth-low-energy)
- [Adafruit - Reverse Engineering a Bluetooth Low Energy Light Bulb](https://learn.adafruit.com/reverse-engineering-a-bluetooth-low-energy-light-bulb)
- <https://www.jaredwolff.com/get-started-with-bluetooth-low-energy/>

[^1]: https://btprodspecificationrefs.blob.core.windows.net/assigned-numbers/Assigned%20Number%20Types/Generic%20Access%20Profile.pdf