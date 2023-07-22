import serial
import firebase
import time
import RPi.GPIO as GPIO
from firebase_admin import firestore

# Initialization
switchStatus = None
doorStatus = None
fanStatus = None

RELAY_PIN = 26


GPIO.setmode(GPIO.BCM)  # Set the GPIO pin numbering mode
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setwarnings(False)

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.reset_input_buffer()

def set_servo_position(switchStatus):
    ser.write(str(switchStatus).encode())
    print(switchStatus)

def controlWindow(stop_event):
    global switchStatus
    switch_status_ref = firebase.firestore_client.collection(
        'home-devices').document('OUTDOOR')
    doc_snapshot = switch_status_ref.on_snapshot(window_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass


def controlDoor(stop_event):
    global doorStatus
    door_status_ref = firebase.firestore_client.collection(
        'home-devices').document('OUTDOOR')
    doc_snapshot = door_status_ref.on_snapshot(door_on_snapshot)


def door_on_snapshot(keys, appliedChanges, read_time):
    global doorStatus
    doc_snapshot = keys[0]
    if doc_snapshot is not None:
        doc = doc_snapshot.to_dict()
        door = doc.get('DOOR')

        if door != doorStatus:
            doorStatus = door
            if door == "DLOW":
                GPIO.output(RELAY_PIN, GPIO.LOW)
            elif door == "DHIGH":
                GPIO.output(RELAY_PIN, GPIO.HIGH)
    else:
        print("Document does not exist.")


def window_on_snapshot(keys, appliedChanges, read_time):
    global switchStatus
    doc_snapshot = keys[0]
    if doc_snapshot is not None:
        doc = doc_snapshot.to_dict()
        switch = doc.get('WINDOW')

        if switch != switchStatus:
            switchStatus = switch
            if switch == "WLOW":
                set_servo_position("WHIGH")
            elif switch == "WHIGH":
                set_servo_position("WLOW")
    else:
        print("Document does not exist.")


def set_fan_position(fanStatus):
    ser.write(str(fanStatus).encode())
    print(fanStatus)


def controlFan(stop_event):
    global fanStatus
    fan_status_ref = firebase.firestore_client.collection(
        'home-devices').document('LIVING-ROOM')
    doc_snapshot = fan_status_ref.on_snapshot(fan_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass


def controlFanBedroom(stop_event):
    global fanStatus
    fan_status_ref = firebase.firestore_client.collection(
        'home-devices').document('BEDROOM')
    doc_snapshot = fan_status_ref.on_snapshot(fan_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass


def controlFanKitchen(stop_event):
    global fanStatus
    fan_status_ref = firebase.firestore_client.collection(
        'home-devices').document('KITCHEN')
    doc_snapshot = fan_status_ref.on_snapshot(fan_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass


def fan_on_snapshot(keys, appliedChanges, read_time):
    global fanStatus
    doc_snapshot = keys[0]
    if doc_snapshot is not None:
        doc = doc_snapshot.to_dict()
        fan = doc.get('FAN')

        if fan != fanStatus:
            fanStatus = fan
            if fan == "FLLOW":
                set_fan_position("FLLOW")
            elif fan == "FLHIGH":
                set_fan_position("FLHIGH")
            elif fan == "FBRHIGH":
                set_fan_position("FBRHIGH")
            elif fan == "FBRLOW":
                set_fan_position("FBRLOW")
            elif fan == "FKHIGH":
                set_fan_position("FKHIGH")
            elif fan == "FKLOW":
                set_fan_position("FKLOW")
    else:
        print("Document does not exist.")

def sensorReading(stop_event):
    sensor_data = {}  # Dictionary to store sensor data and document references
    sensor_count = 0
    # Define the document references for each sensor
    document_refs = {
        u'SOIL': firebase.firestore_client.collection(u'home-sensor').document(u'SOIL-SENSOR'),
        u'GAS': firebase.firestore_client.collection(u'home-sensor').document(u'GAS-SENSOR'),
        u'RAIN': firebase.firestore_client.collection(u'home-sensor').document(u'RAIN-SENSOR'),
        u'FLAME': firebase.firestore_client.collection(u'home-sensor').document(u'FLAME-SENSOR'),
        u'HUMIDITY': firebase.firestore_client.collection('home-sensor').document(u'HUMIDITY-SENSOR'),
        u'TEMPERATURE': firebase.firestore_client.collection('home-sensor').document(u'TEMP-SENSOR'),
        u'HEATINDEX': firebase.firestore_client.collection('home-sensor').document(u'TEMP-SENSOR')
    }
    batch = firebase.firestore_client.batch()
    
    while not stop_event.is_set():
        data = ser.readline().decode().strip()

        if "soil" in data:
            soil_value = int(data.split()[1])
            #print("Soil Value:", soil_value)
            sensor_data['SOIL'] = soil_value

        if "gas" in data:
            gas_value = int(data.split()[1])
            #print("Gas Value:", gas_value)
            sensor_data['LPG'] = gas_value

        if "rain" in data:
            rain_value = int(data.split()[1])
            #print("Rain Value:", rain_value)
            sensor_data['RAIN'] = rain_value

        if "flame" in data:
            flame_value = int(data.split()[1])
            #print("Flame Value:", flame_value)
            sensor_data['FLAME'] = flame_value

        if "humidity" in data:
            humidity_value = float(data.split()[1])
            #print("Humidity Value:", humidity_value)
            sensor_data['HUMIDITY'] = humidity_value

        if "temperature" in data:
            temperature_value = float(data.split()[1])
            #print("Temperature Value:", temperature_value)
            sensor_data['TEMPERATURE'] = temperature_value

        if "heat-index" in data:
            heatindex_value = float(data.split()[1])
            #print("Heat Index Value:", heatindex_value)
            sensor_data['HEATINDEX'] = heatindex_value

        # Update Firebase with the collected sensor data for each document
        for sensor, value in sensor_data.items():
            if sensor in document_refs:
                doc_ref = document_refs[sensor]
                batch.update(doc_ref, {sensor: value})
                sensor_count += 1
        
        if sensor_count >= 7:  # Adjust the count as per your needs
        # Commit the batched updates to Firebase
            batch.commit()
            # Reset the counter and the batch
            sensor_count = 0
            batch = firebase.firestore_client.batch()
