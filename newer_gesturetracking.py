import time
import cvzone
from cvzone.HandTrackingModule import HandDetector
import cv2
import RPi.GPIO as GPIO
from adafruit_motor import servo

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize PWM pins for servos (5 pins for each hand)
# Hand 1 (First hand)
thumb_pin1 = 17
index_pin1 = 27
middle_pin1 = 22
ring_pin1 = 5
pinky_pin1 = 6

# Hand 2 (Second hand)
thumb_pin2 = 18
index_pin2 = 23
middle_pin2 = 24
ring_pin2 = 25
pinky_pin2 = 4

# Set up PWM for each pin
GPIO.setup(thumb_pin1, GPIO.OUT)
GPIO.setup(index_pin1, GPIO.OUT)
GPIO.setup(middle_pin1, GPIO.OUT)
GPIO.setup(ring_pin1, GPIO.OUT)
GPIO.setup(pinky_pin1, GPIO.OUT)

GPIO.setup(thumb_pin2, GPIO.OUT)
GPIO.setup(index_pin2, GPIO.OUT)
GPIO.setup(middle_pin2, GPIO.OUT)
GPIO.setup(ring_pin2, GPIO.OUT)
GPIO.setup(pinky_pin2, GPIO.OUT)

thumb_pwm1 = GPIO.PWM(thumb_pin1, 50)
index_pwm1 = GPIO.PWM(index_pin1, 50)
middle_pwm1 = GPIO.PWM(middle_pin1, 50)
ring_pwm1 = GPIO.PWM(ring_pin1, 50)
pinky_pwm1 = GPIO.PWM(pinky_pin1, 50)

thumb_pwm2 = GPIO.PWM(thumb_pin2, 50)
index_pwm2 = GPIO.PWM(index_pin2, 50)
middle_pwm2 = GPIO.PWM(middle_pin2, 50)
ring_pwm2 = GPIO.PWM(ring_pin2, 50)
pinky_pwm2 = GPIO.PWM(pinky_pin2, 50)

# Start PWM with initial duty cycle
thumb_pwm1.start(0)
index_pwm1.start(0)
middle_pwm1.start(0)
ring_pwm1.start(0)
pinky_pwm1.start(0)

thumb_pwm2.start(0)
index_pwm2.start(0)
middle_pwm2.start(0)
ring_pwm2.start(0)
pinky_pwm2.start(0)

# Initialize variables
servo_positions1 = [0, 0, 0, 0, 0]  # Store servo positions for Hand 1 (First hand)
servo_positions2 = [0, 0, 0, 0, 0]  # Store servo positions for Hand 2 (Second hand)

# Function to update servos for both hands
def update_servos(fingers1, fingers2=None):
    # Update servos for Hand 1 (First hand)
    thumb_pwm1.ChangeDutyCycle(10 if fingers1[0] == 1 else 2)
    index_pwm1.ChangeDutyCycle(10 if fingers1[1] == 1 else 2)
    middle_pwm1.ChangeDutyCycle(10 if fingers1[2] == 1 else 2)
    ring_pwm1.ChangeDutyCycle(10 if fingers1[3] == 1 else 2)
    pinky_pwm1.ChangeDutyCycle(10 if fingers1[4] == 1 else 2)

    # If fingers2 (second hand) is provided, update servos for Hand 2 (Second hand)
    if fingers2:
        thumb_pwm2.ChangeDutyCycle(10 if fingers2[0] == 1 else 2)
        index_pwm2.ChangeDutyCycle(10 if fingers2[1] == 1 else 2)
        middle_pwm2.ChangeDutyCycle(10 if fingers2[2] == 1 else 2)
        ring_pwm2.ChangeDutyCycle(10 if fingers2[3] == 1 else 2)
        pinky_pwm2.ChangeDutyCycle(10 if fingers2[4] == 1 else 2)

# Open camera
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)

# Initialize hand detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Gesture classification function
def handPositionStrings(fingers):
    if fingers == [0, 0, 0, 0, 0]:
        return "Fist"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Peace"
    elif fingers == [0, 0, 1, 1, 1]:
        return "Okay"
    elif fingers == [0, 1, 1, 1, 1]:
        return "Four"
    elif fingers == [1, 1, 1, 1, 1]:
        return "Five"
    elif fingers == [1, 0, 0, 0, 0]:
        return "Thumbs up"
    elif fingers == [0, 1, 1, 1, 0]:
        return "Three"
    elif fingers == [0, 0, 1, 0, 0]:
        return "The Bird"
    elif fingers == [0, 1, 0, 0, 0]:
        return "Index up"
    elif fingers == [0, 0, 0, 0, 1]:
        return "Pinky up"
    elif fingers == [0, 0, 0, 1, 0]:
        return "Ring up"
    elif fingers == [1, 1, 0, 0, 1]:
        return "Spider-Man"
    elif fingers == [1, 1, 1, 0, 0]:
        return "Ninja Turtle"
    elif fingers == [1, 1, 0, 0, 0]:
        return "L"
    else:
        return "No Gesture"

# Main loop
while True:
    # Reads image from camera
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centerPoint1 = hand1["center"]
        handType1 = hand1["type"]

        fingers1 = detector.fingersUp(hand1)
        update_servos(fingers1)  # Update servos for hand 1

        # Calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # Display FPS and gesture information on the image
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, str("Gesture 1"), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, handPositionStrings(fingers1), (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            centerPoint2 = hand2["center"]
            handType2 = hand2["type"]

            fingers2 = detector.fingersUp(hand2)
            update_servos(fingers1, fingers2)  # Update servos for hand 2

            cv2.putText(img, str(int(fps)), (150, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, str("Gesture 2"), (150, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, handPositionStrings(fingers2), (150, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display image
    cv2.imshow("Image", img)
    cv2.waitKey(1)
