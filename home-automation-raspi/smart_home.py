from firebase_admin import firestore
from sensors_control import controlWindow, controlDoor, controlFan, controlFanBedroom, controlFanKitchen, sensorReading
from relays_control import controlLightBR, controlLightLR, controlLightB, controlLightK, controlOutletB, controlOutletBR, controlOutletK, controlOutletLR, currentReading

import time
import threading


if __name__ == '__main__':
    stop_event = threading.Event()

    t1 = threading.Thread(target=sensorReading, args=(stop_event,))
    t2 = threading.Thread(target=controlWindow, args=(stop_event,))
    t3 = threading.Thread(target=controlFan, args=(stop_event,))
    t4 = threading.Thread(target=controlFanBedroom, args=(stop_event,))
    t5 = threading.Thread(target=controlFanKitchen, args=(stop_event,))

    t6 = threading.Thread(target=controlLightBR, args=(stop_event,))
    t7 = threading.Thread(target=controlLightLR, args=(stop_event,))
    t8 = threading.Thread(target=controlLightB, args=(stop_event,))
    t9 = threading.Thread(target=controlLightK, args=(stop_event,))

    t10 = threading.Thread(target=controlOutletBR, args=(stop_event,))
    t11 = threading.Thread(target=controlOutletLR, args=(stop_event,))
    t12 = threading.Thread(target=controlOutletB, args=(stop_event,))
    t13 = threading.Thread(target=controlOutletK, args=(stop_event,))
    t14 = threading.Thread(target=controlOutletBR, args=(stop_event,))

    t15 = threading.Thread(target=currentReading, args=(stop_event,))
    t16 = threading.Thread(target=controlDoor, args=(stop_event,))
    # Start all the threads
    threads = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16]
    for thread in threads:
        thread.start()

    # Wait for the stop event to be set
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Set the stop event to stop the threads
        stop_event.set()

    # Wait for all the threads to finish
    for thread in threads:
        thread.join()
