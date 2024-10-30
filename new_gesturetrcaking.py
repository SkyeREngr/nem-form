import cvzone
from cvzone.HandTrackingModule import HandDetector
import cv2
import time
import serial

try:
    ser = serial.Serial('COM8', 9600, timeout=1)
    time.sleep(2)
    print("Serial connection established on COM8")
except Exception as e:
    print(f"Error opening serial connection on COM8: {e}")
    ser = None

def sendData(fingers):
    if ser is not None and ser.is_open:
        #thumb value needs to be inverted for some reason
        fingers[0] = 1 if fingers[0] == 0 else 0
        #use CSV format for better parsing
        string = ",".join([str(finger) for finger in fingers]) + "\n"
        try:
            ser.write(string.encode())  #send encoded string
            print(f"Sent: {string.strip()}")  #remove newline
        except Exception as e:
            print(f"Error while sending data: {e}")
    else:
        print("Serial connection not open")


cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    img = cv2.flip(img, 1)

    if hands:
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        sendData(fingers1)  #send finger data out

    cv2.imshow("Image", img)
    cv2.waitKey(1)
