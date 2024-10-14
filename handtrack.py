import cv2
import mediapipe as mp
import numpy as np
import time

# hand identification program, detects if a hand is displayed

#checking opencv and mediapipe version
#print("Your OpenCV version is: " + cv2.__version__)
#print("Your mediapipe version is: " + mp.__version__)

# assigning camera to variable
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(False,1, 1, 0.5, 0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

"""We need to find a way to track the three main joints for each finger and abstract that information into our servo motors"""
"""https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker"""

index_y_coords = []
max_index_node_diffs = [87, 62, 50]

def finger_node_diff(finger_nodes):
    node_distances = []
    node_distances.append(finger_nodes[0] - finger_nodes[1])
    node_distances.append(finger_nodes[1] - finger_nodes[2])
    node_distances.append(finger_nodes[2] - finger_nodes[3])
    return node_distances

def finger_angle_calc(node_diffs):
    #print("this will calculate the angle of an individual's index finger")
    node_angles = []
    for i in range(len(max_index_node_diffs)):
        new_node_angle = (1 - (node_diffs[i] / max_index_node_diffs[i])) * 90
        node_angles.append(new_node_angle)
    return node_angles

while True:
    # reads image from camera
    success, img = cap.read()
    # converts BGR to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # processes results from camera
    results = hands.process(imgRGB)
    print("______________________________________________________________")
    # results.multi_hand_landmarks is the hand data
    # if the camera is receiving hand data,
    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                
                # hand location height, width, channel
                h, w, c = img.shape
                # gives position of center
                cx, cy = int(lm.x*w), int(lm.y*h)
                match id:
                    case 4:
                        cv2.circle(img, (int(cx), int(cy)), 10, (255, 0, 255), cv2.FILLED) #thumb
                        #print("Thumb Coordinates: ", cx, cy)
                    # index finger coordinates
                    case 5:
                        cv2.circle(img, (int(cx), int(cy)), 10, (0, 255, 255), cv2.FILLED) #base index knuckle
                        index_y_coords.append(cy)
                        #print("Index 5 Coordinates: ", cy)
                    case 6:
                        cv2.circle(img, (int(cx), int(cy)), 10, (0, 255, 255), cv2.FILLED) #first index knuckle
                        index_y_coords.append(cy)
                        #print("Index 6 Coordinates: ", cy)
                    case 7:
                        cv2.circle(img, (int(cx), int(cy)), 10, (0, 255, 255), cv2.FILLED) #second index knuckle
                        index_y_coords.append(cy)
                        #print("Index 7 Coordinates: ", cy)
                    case 8:
                        cv2.circle(img, (int(cx), int(cy)), 10, (0, 255, 255), cv2.FILLED) #tip of index finger
                        index_y_coords.append(cy)
                        #print("Index 8 Coordinates: ", cy)
                    case 12:
                        cv2.circle(img, (int(cx), int(cy)), 10, (255, 0, 255), cv2.FILLED) #middle
                        ##print("Middle Coordinates: ", cx, cy)
                    case 16:
                        cv2.circle(img, (int(cx), int(cy)), 10, (255, 0, 255), cv2.FILLED) #ring
                        #print("Ring Coordinates: ", cx, cy)
                    case 20:
                        cv2.circle(img, (int(cx), int(cy)), 10, (255, 0, 255), cv2.FILLED) #pinky
                        #print("Pinky Coordinates: ", cx, cy)
            # draw skeleton mesh onto hand
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        
        #calculate finger angles
        #index finger is id 5-8
        print("index finger coords: ", index_y_coords)
        finger_node_diffs = finger_node_diff(index_y_coords)
        print("index finger node differences: ", finger_node_diffs)
        print("index finger node angles: ", finger_angle_calc(finger_node_diffs))


        index_y_coords = []


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    time.sleep(0.5)