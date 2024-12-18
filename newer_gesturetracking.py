import time
import cvzone
from cvzone.HandTrackingModule import HandDetector
import cv2
from adafruit_motor import servo
import board
import pwmio

# Initialize PWM pins for servos (5 pins for each hand)
# Hand 1 (First hand)
thumb_pin1 = pwmio.PWMOut(board.D17, duty_cycle=2 ** 15,  frequency=50)
index_pin1 = pwmio.PWMOut(board.D27, duty_cycle=2 ** 15,  frequency=50)
middle_pin1 = pwmio.PWMOut(board.D22, duty_cycle=2 ** 15,  frequency=50)
ring_pin1 = pwmio.PWMOut(board.D5, duty_cycle=2 ** 15,  frequency=50)
pinky_pin1 = pwmio.PWMOut(board.D6, duty_cycle=2 ** 15,  frequency=50)

# Hand 2 (Second hand)
thumb_pin2 = pwmio.PWMOut(board.D18, duty_cycle=2 ** 15,  frequency=50)
index_pin2 = pwmio.PWMOut(board.D23, duty_cycle=2 ** 15,  frequency=50)
middle_pin2 = pwmio.PWMOut(board.D24, duty_cycle=2 ** 15,  frequency=50)
ring_pin2 = pwmio.PWMOut(board.D25, duty_cycle=2 ** 15,  frequency=50)
pinky_pin2 = pwmio.PWMOut(board.D4, duty_cycle=2 ** 15,  frequency=50)

# Initialize Servo objects for Hand 1 (First hand)
thumb_servo1 = servo.Servo(thumb_pin1)
index_servo1 = servo.Servo(index_pin1)
middle_servo1 = servo.Servo(middle_pin1)
ring_servo1 = servo.Servo(ring_pin1)
pinky_servo1 = servo.Servo(pinky_pin1)

# Initialize Servo objects for Hand 2 (Second hand)
thumb_servo2 = servo.Servo(thumb_pin2)
index_servo2 = servo.Servo(index_pin2)
middle_servo2 = servo.Servo(middle_pin2)
ring_servo2 = servo.Servo(ring_pin2)
pinky_servo2 = servo.Servo(pinky_pin2)

# Initialize variables
servo_positions1 = [0, 0, 0, 0, 0]  # Store servo positions for Hand 1 (First hand)
servo_positions2 = [0, 0, 0, 0, 0]  # Store servo positions for Hand 2 (Second hand)

def update_servos(fingers1, fingers2=None):
    def smoothMove(servo, target_angle, step=5, delay=0.05):
        if servo.angle is None:
            servo.angle = 15
        current_angle = servo.angle
        step = step if target_angle > current_angle else -step

        for angle in range(int(current_angle), int(target_angle), step):
            servo.angle = angle
            time.sleep(delay)
        servo.angle = target_angle

    smoothMove(thumb_servo1, 165 if fingers1[0] == 1 else 15)
    smoothMove(index_servo1, 165 if fingers1[1] == 1 else 15)
    smoothMove(middle_servo1, 165 if fingers1[2] == 1 else 15)
    smoothMove(ring_servo1, 165 if fingers1[3] == 1 else 15)
    smoothMove(pinky_servo1, 165 if fingers1[4] == 1 else 15)

    if fingers2:
        smoothMove(thumb_servo2, 165 if fingers2[0] == 1 else 15)
        smoothMove(index_servo2, 165 if fingers2[1] == 1 else 15)
        smoothMove(middle_servo2, 165 if fingers2[2] == 1 else 15)
        smoothMove(ring_servo2, 165 if fingers2[3] == 1 else 15)
        smoothMove(pinky_servo2, 165 if fingers2[4] == 1 else 15)


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
