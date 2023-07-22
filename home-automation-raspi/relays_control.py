import serial
import firebase
from firebase_admin import firestore

# Initialization
lightStatus = None
outletStatus = None

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.reset_input_buffer()

def set_light_position(lightStatus):
    ser.write(str(lightStatus).encode())
    print(lightStatus)
    
def set_outlet_position(outletStatus):
    ser.write(str(outletStatus).encode())
    print(outletStatus)

def controlLightLR(stop_event):
    global lightStatus
    light_status_ref = firebase.firestore_client.collection('home-devices').document('LIVING-ROOM')
    light_doc_snapshot = light_status_ref.on_snapshot(light_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass
    
def controlOutletLR(stop_event):
    global outletStatus
    outlet_status_ref = firebase.firestore_client.collection('home-devices').document('LIVING-ROOM')
    outlet_doc_snapshot = outlet_status_ref.on_snapshot(outlet_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass

def controlLightBR(stop_event):
    global lightStatus
    light_status_ref = firebase.firestore_client.collection('home-devices').document('BEDROOM')
    light_doc_snapshot = light_status_ref.on_snapshot(light_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass
    
def controlOutletBR(stop_event):
    global outletStatus
    outlet_status_ref = firebase.firestore_client.collection('home-devices').document('BEDROOM')
    outlet_doc_snapshot = outlet_status_ref.on_snapshot(outlet_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass

def controlLightB(stop_event):
    global lightStatus
    light_status_ref = firebase.firestore_client.collection('home-devices').document('BATHROOM')
    light_doc_snapshot = light_status_ref.on_snapshot(light_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass
    
def controlOutletB(stop_event):
    global outletStatus
    outlet_status_ref = firebase.firestore_client.collection('home-devices').document('BATHROOM')
    outlet_doc_snapshot = outlet_status_ref.on_snapshot(outlet_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass

def controlLightK(stop_event):
    global lightStatus
    light_status_ref = firebase.firestore_client.collection('home-devices').document('KITCHEN')
    light_doc_snapshot = light_status_ref.on_snapshot(light_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass

def controlOutletK(stop_event):
    global outletStatus
    outlet_status_ref = firebase.firestore_client.collection('home-devices').document('KITCHEN')
    outlet_doc_snapshot = outlet_status_ref.on_snapshot(outlet_on_snapshot)

    # Keep running until the stop_event is set
    while not stop_event.is_set():
        pass

def light_on_snapshot(keys, appliedChanges, read_time):
    global lightStatus
    for key in keys:
        light_snapshot = key
        if light_snapshot is not None:
            doc1 = light_snapshot.to_dict()
            light = doc1.get('LIGHTS')

            if light != lightStatus:
                lightStatus = light
                if light == "LLLOW":
                    set_light_position("LLLOW")
                elif light == "LLHIGH":
                    set_light_position("LLHIGH")
                elif light == "LBHIGH":
                    set_light_position("LBHIGH")
                elif light == "LBLOW": 
                    set_light_position("LBLOW")
                elif light == "LKHIGH":
                    set_light_position("LKHIGH")
                elif light == "LKLOW": 
                    set_light_position("LKLOW")
                elif light == "LBRHIGH":
                    set_light_position("LBRHIGH")
                elif light == "LBRLOW": 
                    set_light_position("LBRLOW")
        else:
            print("Document does not exist.")

        
def outlet_on_snapshot(keys, appliedChanges, read_time):
    global outletStatus
    for key in keys:
        outlet_snapshot = key
        if outlet_snapshot is not None:
            doc2 = outlet_snapshot.to_dict()
            outlet = doc2.get('OUTLET')

            if outlet!= outletStatus:
                outletStatus = outlet
                if outlet == "OLLOW":
                    set_outlet_position("OLLOW")
                elif outlet == "OLHIGH":
                    set_outlet_position("OLHIGH")
                elif outlet == "OBHIGH":
                    set_outlet_position("OBHIGH")
                elif outlet == "OBLOW": 
                    set_outlet_position("OBLOW")
                elif outlet == "OKHIGH":
                    set_outlet_position("OKHIGH")
                elif outlet == "OKLOW": 
                    set_outlet_position("OKLOW")
                elif outlet == "OBRHIGH":
                    set_outlet_position("OBRHIGH")
                elif outlet == "OBRLOW": 
                    set_outlet_position("OBRLOW")
        else:
            print("Document does not exist.")

def currentReading(stop_event):

    while not stop_event.is_set():
        data = ser.readline().decode().strip()

        if "current" in data:
            current_value = float(data.split()[1])
            # print("Current Value:", current_value)
            
            firebase.firestore_client.collection(u'home-sensor').document(u'CURRENT-SENSOR').update({
            u'CURRENT': current_value
            })
  
        if "power" in data:
            power_value = float(data.split()[1])
            # print("Power Value:", power_value)
            
            firebase.firestore_client.collection(u'home-sensor').document(u'CURRENT-SENSOR').update({
            u'POWER': power_value
            })
            
        if "energy" in data:
            energy_value = float(data.split()[1])
            # print("Energy Value:", energy_value)
            
            firebase.firestore_client.collection(u'home-sensor').document(u'CURRENT-SENSOR').update({
            u'ENERGY': energy_value
            })
            