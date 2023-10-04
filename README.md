# BLE_Security_Analysis_Toolkit

## Overview

BLE-Toolkit is a comprehensive set of Python scripts designed for Bluetooth Low Energy (BLE) device enumeration and interaction. The toolkit includes a device scanning utility (`BLEScanner`) and a device enumeration utility (`BLEEnumerator`).

### Intention

The primary purpose of this toolkit is to assist researchers, penetration testers, and developers in quickly and efficiently gathering information about nearby BLE devices. It aims to provide an easy-to-use interface for scanning and enumerating BLE devices, offering both batch and interactive modes for maximum flexibility.

### How it Works

#### BLEScanner

- Uses the `bluepy` library for BLE scanning.
- Provides real-time feedback on discovered devices.
- Logs the information about discovered devices to a log file (`ble_scan.log`).

#### BLEEnumerator

- Connects to a specified BLE device using its BSSID.
- Enumerates the services and characteristics available on the device.
- Allows for reading and writing characteristics where applicable.

### Installation

Run the `install.sh` script to install all dependencies.

```bash
chmod +x install.sh
./install.sh
