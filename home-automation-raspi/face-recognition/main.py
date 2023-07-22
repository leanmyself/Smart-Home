import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from face_recognition import face_recognition
import time
from twilio.rest import Client
from RPLCD.i2c import CharLCD

# Define the LCD I2C address and dimensions
LCD_ADDRESS = 0x27  # Replace with the actual I2C address of your LCD display
LCD_WIDTH = 16     # Replace with the actual width of your LCD display
LCD_LINES = 2      # Replace with the actual number of lines of your LCD display

RELAY_PIN = 26  # Replace with the appropriate GPIO pin number
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

# Create an instance of the LCD display
lcd = CharLCD(i2c_expander='PCF8574', address=LCD_ADDRESS,
              port=1, cols=LCD_WIDTH, rows=LCD_LINES)

def send_sms_notification(phone_number, message):
    try:
        client.messages.create(
            body=message,
            from_='+',
            to=phone_number
        )
        print("SMS notification sent.")
    except Exception as e:
        print("Error sending SMS notification:", str(e))


def write_to_lcd(line, text):
    spaces = (LCD_WIDTH - len(text)) // 2

    centered_text = " " * spaces + text

    lcd.cursor_pos = (line, 0)
    lcd.write_string(centered_text)


def initialize_lcd():
    # Initialize the LCD display
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    write_to_lcd(0, "Welcome to")
    write_to_lcd(1, "Smart Space")


def turn_relay_on():
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    print("Door is opened.")


def turn_relay_off():
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print("Door is closed.")


def read_rfid():
    reader = SimpleMFRC522()
    try:
        print("Hold an RFID card near the reader.")
        id, text = reader.read()
        print("RFID Card ID:", id)
        print("RFID Card Text:", text)
        return str(id), text
    except Exception as e:
        print("Error reading RFID card:", str(e))
        return None, None


if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)  # Set the GPIO pin numbering mode
        GPIO.setup(RELAY_PIN, GPIO.OUT)

        initialize_lcd()  # Initialize the LCD display

        while True:
            recognized_user = face_recognition()  # Perform face recognition

            if recognized_user:
                print("Face detected. Please tap the RFID card.")
                write_to_lcd(0, "Face detected")
                write_to_lcd(1, "Tap RFID card")
                rfid_success = False

                id, text = read_rfid()

                rfid_attempts = 1  # Initialize the attempts to 1

                while rfid_attempts <= 3:
                    if id and text:
                        print("RFID card belongs to:", text)

                        if recognized_user == text.strip() or text.strip() == 'Master':
                            print(
                                "RFID card and face recognition match. Access granted.")
                            # Perform authorized actions here
                            send_sms_notification('+63', 'SMART SPACE. The door is opened. Access Granted to ' + recognized_user)
                            print("Access granted to:", recognized_user)
                            write_to_lcd(0, "Access granted")
                            write_to_lcd(1, "Welcome Home.")
                    
                            turn_relay_on()
                            rfid_success = True
                            time.sleep(10)
                            turn_relay_off()
                            initialize_lcd()
                            break
                        else:
                            print(
                                "RFID card and face recognition do not match. Please try again.")
                            write_to_lcd(0, "Access denied")
                            write_to_lcd(1, "Tap RFID again")

                    rfid_attempts += 1
                    # Add a delay of 2 seconds between tap attempts
                    time.sleep(2)
                    id, text = read_rfid()

                if not rfid_success:
                    send_sms_notification('+63', 'SMART SPACE. Someone tried to acccess your door.')
                    print("Maximum attempts reached. Access denied.")
                    write_to_lcd(0, "Maximum attempts")
                    write_to_lcd(1, "reached. Sorry")
                    turn_relay_off()
                    time.sleep(3)
                    initialize_lcd()

            else:
                print("No face detected.")
                write_to_lcd(0, "No face detected")


    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        GPIO.cleanup(RELAY_PIN)  # Cleanup the specific GPIO pin used
