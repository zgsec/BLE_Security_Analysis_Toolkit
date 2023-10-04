#!/usr/bin/env python3

import time
import logging
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
    def __init__(self, scan_duration=30):
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

# Configure logging settings
def setup_logging():
    logging.basicConfig(filename='ble_scan.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Main function to initiate scanning
if __name__ == "__main__":
    setup_logging()
    scanner = BLEScanner()
    scanner.scan_devices()
