#!/usr/bin/env python3
import csv
import time
import logging
import argparse
from collections import OrderedDict
from bluepy.btle import Scanner, DefaultDelegate, BTLEException

# Delegate class to handle bluepy's discovery events
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            logging.info(f"Discovered device {dev.addr}")

# Utility class for logging BLE device data
class BLELogger:
    @staticmethod
    def log_device(dev, device_name, device_count):
        log_entry = f"Discovered {device_count} devices. Latest: {dev.addr} ({dev.addrType}), RSSI={dev.rssi} dB, Name={device_name}"
        print(log_entry)  # Real-time feedback
        logging.info(log_entry)

# Class to handle BLE device scanning
class BLEScanner:
    def __init__(self, scan_duration):
        self.scan_duration = scan_duration
        self.scanner = Scanner().withDelegate(ScanDelegate())
        self.device_data = OrderedDict()  # Data deduplication

    def scan_devices(self):
        stop_time = time.time() + self.scan_duration
        device_count = 0  # Real-time feedback
        print("Scanning for devices...")  # Real-time feedback

        while time.time() < stop_time:
            try:
                devices = self.scanner.scan(0.1)
                for dev in devices:
                    device_name = next((value for adtype, desc, value in dev.getScanData() if desc == "Complete Local Name"), None)
                    
                    # Data deduplication
                    if dev.addr not in self.device_data:
                        self.device_data[dev.addr] = {
                            "addrType": dev.addrType,
                            "rssi": dev.rssi,
                            "device_name": device_name,
                            "scan_data": dev.getScanData()
                        }
                        device_count += 1  # Real-time feedback
                        BLELogger.log_device(dev, device_name, device_count)
            except BTLEException as e:
                logging.error(f"BTLEException occurred during scan: {e}")
            except Exception as e:
                logging.error(f"Unexpected exception occurred: {e}")

        return list(self.device_data.values())

# Write the scanned device data to a CSV file
def write_to_csv(devices, filename):
    headers = ["Device Address", "Address Type", "RSSI", "Device Name", "Description", "Value"]
    rows = [headers]

    for dev in devices:
        device_name = dev['device_name']
        for adtype, desc, value in dev['scan_data']:
            rows.append([dev['addr'], dev['addrType'], dev['rssi'], device_name, desc, value])

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# Configure logging settings
def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Main function to handle argument parsing and initiate scanning
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BLE Device Scanner')
    parser.add_argument('--duration', type=int, default=30, help='Duration of the scan in seconds')
    parser.add_argument('--log_file', type=str, default='ble_scan.log', help='Log file name')
    parser.add_argument('--csv_file', type=str, default='ble_devices.csv', help='CSV file to store device data')
    args = parser.parse_args()

    setup_logging(args.log_file)
    scanner = BLEScanner(scan_duration=args.duration)
    scanned_devices = scanner.scan_devices()
    write_to_csv(scanned_devices, args.csv_file)

