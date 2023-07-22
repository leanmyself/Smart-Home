import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def add_data():
    # Write to RFID
    new_text = input("Enter the data to write on RFID: ")
    reader.write(new_text)
    print("Successfully written to RFID:", new_text)
    print("\n")

def read_data():
    # Read from RFID
    id, text = reader.read()
    print("RFID ID:", id)
    print("RFID Text:", text)
    print("\n")

try:
    while True:
        print("Enroll an RFID\n")
        print("1. Add Data")
        print("2. Read Data")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            print("Tap the RFID to display the ID...")
            id, _ = reader.read()
            print("RFID ID:", id)
            add_data()
        elif choice == "2":
            read_data()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

finally:
    GPIO.cleanup()
