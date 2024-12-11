import cvzone
from cvzone.HandTrackingModule import HandDetector
import cv2
import time


pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.8, maxHands=2)

#fix this so it isnt a bunch of if statements
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



while True:
    # reads image from camera
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centerPoint1 = hand1["center"]
        handType1 = hand1["type"]

        fingers1 = detector.fingersUp(hand1)
        handPositionStrings(fingers1)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, str("Gesture 1"), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, handPositionStrings(fingers1), (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        #print(fingers1)

        if len(hands)==2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            centerPoint2 = hand2["center"]
            handType2 = hand2["type"]

            fingers2 = detector.fingersUp(hand2)

            cv2.putText(img, str(int(fps)), (150, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, str("Gesture 2"), (150, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, handPositionStrings(fingers2), (150, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),2)

            print(fingers1, fingers2)


    cv2.imshow("Image", img)
    cv2.waitKey(1)