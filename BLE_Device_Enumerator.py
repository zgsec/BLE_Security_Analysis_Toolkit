#!/usr/bin/env python3
import time
import logging
from bluepy.btle import Peripheral, DefaultDelegate, BTLEException

class EnumDelegate(DefaultDelegate):
    """Delegate class to handle bluepy's events."""
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print(f"Received notification from {cHandle}: {data}")
        logging.info(f"Received notification from {cHandle}: {data}")

def setup_logging():
    """Configure logging settings."""
    logging.basicConfig(filename='ble_enum.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_services_and_characteristics(peripheral):
    """Display available services and characteristics."""
    services = peripheral.getServices()
    service_dict = {}
    for idx, service in enumerate(services):
        print(f"{idx+1}. Service UUID: {service.uuid}")
        service_dict[idx+1] = service

    choice = int(input("Select a service to enumerate its characteristics: "))
    selected_service = service_dict.get(choice)

    if selected_service:
        characteristics = selected_service.getCharacteristics()
        char_dict = {}
        for idx, characteristic in enumerate(characteristics):
            properties = characteristic.propertiesToString().split('|')
            readable = 'Yes' if 'READ' in properties else 'No'
            writable = 'Yes' if 'WRITE' in properties else 'No'
            notifiable = 'Yes' if 'NOTIFY' in properties else 'No'
            print(f"  {idx+1}. Characteristic UUID: {characteristic.uuid} (Readable: {readable}, Writable: {writable}, Notifiable: {notifiable})")
            char_dict[idx+1] = characteristic

        return char_dict
    else:
        print("Invalid service selection.")
        return None

def main():
    """Main function."""
    setup_logging()
    target_bssid = input("Enter the BSSID to connect to: ").strip()

    try:
        peripheral = Peripheral(target_bssid)
        peripheral.withDelegate(EnumDelegate())
        logging.info(f"Connected to {target_bssid}")

        while True:
            print("\nEnumerating services...")
            char_dict = display_services_and_characteristics(peripheral)

            if char_dict:
                action = input("\nOptions:\n  [R]ead from a characteristic\n  [W]rite to a characteristic\n  [E]xit\n  [C]hoose another service\nSelect an option: ").upper()

                if action == 'R':
                    choice = int(input("Select a characteristic to read from: "))
                    selected_char = char_dict.get(choice)
                    if selected_char and "READ" in selected_char.propertiesToString():
                        print(f"Read value: {selected_char.read()}")
                    else:
                        print("Invalid selection or characteristic not readable.")

                elif action == 'W':
                    choice = int(input("Select a characteristic to write to: "))
                    selected_char = char_dict.get(choice)
                    if selected_char and "WRITE" in selected_char.propertiesToString():
                        value_to_write = input("Enter the value to write: ").encode()
                        selected_char.write(value_to_write)
                        print("Write operation completed.")
                    else:
                        print("Invalid selection or characteristic not writable.")

                elif action == 'C':
                    continue

                elif action == 'E':
                    break
                else:
                    print("Invalid option. Try again.")
            else:
                print("No valid services or characteristics to display.")
                break

    except BTLEException as e:
        logging.error(f"BTLEException occurred: {e}")
        print(f"Connection error: {e}")

    except ValueError:
        logging.error("Invalid input. Please enter a number.")
        print("Invalid input. Please enter a number.")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
