import cv2
import mediapipe as mp
from soeroCamUtils import SoeroCam
# import pyttsx3 as speech
from mycv2 import calcDistance, createBoxWithText, findMiddlePoint
import numpy as np

def main():
    # mediapipe stuff
    mp_drawing = mp.solutions.drawing_utils # helper to draw
    mp_drawing_styles = mp.solutions.drawing_styles #also a helper, but for style B)
    mp_hands = mp.solutions.hands # all hand utils
    hand_tracker = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands = 2) 
    # open cv cam stuff
    cameraDrone = SoeroCam(width=1080, height=810,isMirrored=False, src=1) # camera for video input
    # print(cameraDrone.getOriginalCamDim())
    cameraWeb = SoeroCam(width=800, height=600, isMirrored=True, src=0)
    close_key = ord('q') # what key to press to exit
    
    #speech stuff
    # engine = speech.init()

    # units
    fontScale = cameraDrone.width/960
    unit_x = cameraDrone.width//32
    mid_x = unit_x*16
    
    # rectangle ui sutff
    RECT_COLOR = (255, 193, 7)
    left_hand_rect =createBoxWithText("THROTLE / YAW", fontScale, 2, cv2.FONT_HERSHEY_SIMPLEX, RECT_COLOR, (255, 255, 255))
    right_hand_rect  =createBoxWithText("PITCH/ ROLL", fontScale, 2, cv2.FONT_HERSHEY_SIMPLEX, RECT_COLOR, (255, 255, 255))

    lrh, lrw,_ = left_hand_rect.shape
    rrh, rrw,_ = right_hand_rect.shape
    left_rect_x = (mid_x - lrw)//2
    right_rect_x = mid_x + (mid_x - rrw)//2

    # joystick ui stuff
    CIRCLE_COLOR = (0,184,244)
    rectSize = 72
    leftStickCenterPos = (mid_x//2,cameraDrone.height//2)
    rightStickCenterPos = (mid_x + mid_x//2, cameraDrone.height//2)
    leftStickTopPos = (leftStickCenterPos[0] - rectSize//2, leftStickCenterPos[1] - rectSize//2)
    rightStickTopPos = (rightStickCenterPos[0] - rectSize//2, rightStickCenterPos[1] - rectSize//2)
    joyStickRect = np.full((rectSize, rectSize, 3), CIRCLE_COLOR, np.uint8)
    colorMsg = ((0, 0, 255), (0, 0, 255), (0, 255, 0))
    readyMsg = ("NOT READY", "NOT READY", "IS READY")

    # loop for each frame captured
    for img in cameraWeb.infiniteCapture():
        # convert img from BGR to RGB because mediapipe takes RGB image
        # and opencv default is BGR
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        img.flags.writeable = False

        # Detect!
        results = hand_tracker.process(img)

        # makes img writable [noneed]
        # img.flags.writeable = True
        # convert back to BGR
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # get fpv frame
        fpvFrame = cameraDrone.singleCapture()

        #add rect
        fpvFrame[0: lrh, left_rect_x: left_rect_x +lrw] = left_hand_rect
        fpvFrame[0:rrh, right_rect_x: right_rect_x + rrw] = right_hand_rect
        # print(cv2.getTextSize("LEFT HAND", cv2.FONT_HERSHEY_SIMPLEX, fontScale, 2))
        
        # add divider ui
        cv2.line(fpvFrame,(mid_x,0),(mid_x,cameraDrone.height),(255,0,0),3)
        # fpvFrame = cv2.resize(fpvFrame, (1440, 1080))
        
        # add center of joystick
        fpvFrame[leftStickTopPos[1]: leftStickTopPos[1] + rectSize, leftStickTopPos[0]: leftStickTopPos[0] + rectSize] = joyStickRect
        fpvFrame[rightStickTopPos[1]: rightStickTopPos[1] + rectSize, rightStickTopPos[0]: rightStickTopPos[0] + rectSize] = joyStickRect
        # cv2.circle(fpvFrame,leftStickPos, 32, CIRCLE_COLOR, -1)
        # cv2.circle(fpvFrame,rightStickPos, 32, CIRCLE_COLOR, -1)
        
        # draw the results!
        total_hand = 0
        thumbTip = []
        indexTip = []
        if (results.multi_hand_landmarks):
            for hand in results.multi_hand_landmarks:#a list of hand landmark
                mp_drawing.draw_landmarks(
                    fpvFrame, 
                    hand, 
                    mp_hands.HAND_CONNECTIONS) 
                    # mp_drawing_styles.get_default_hand_landmarks_style(),
                    # mp_drawing_styles.get_default_hand_connections_style())
                total_hand+=1
                landMark = hand.landmark
                indexTip.append(landMark[mp_hands.HandLandmark.INDEX_FINGER_TIP])
                thumbTip.append(landMark[mp_hands.HandLandmark.THUMB_TIP])
                # print(f'{len(hand.landmark)} and type: {type(hand.landmark)}')
                # print("======1=====")

        # engine.say(f'LOST {2-total_hand} HAND')
        # engine.runAndWait() #need threader
        cv2.putText(fpvFrame, readyMsg[total_hand], (left_rect_x+lrw +20, lrh), cv2.FONT_HERSHEY_SIMPLEX, fontScale, colorMsg[total_hand], 2, cv2.LINE_AA)
        
        midPoints = []
        for i in range(total_hand):
            midPoints.append(findMiddlePoint(thumbTip[i], indexTip[i], cameraDrone.width, cameraDrone.height))
        
        for point, isClose in midPoints:
            if(isClose):
                leftStickDis = calcDistance(leftStickCenterPos[0], leftStickCenterPos[1], point[0], point[1])
                rightStickDis = calcDistance(rightStickCenterPos[0], rightStickCenterPos[1], point[0], point[1])
                if(leftStickDis > rightStickDis):
                    # draw on right
                    cv2.line(fpvFrame, rightStickCenterPos, point, RECT_COLOR, 3)
                else:
                    cv2.line(fpvFrame, leftStickCenterPos, point, RECT_COLOR, 3)
        cv2.imshow('HandTracking', fpvFrame)
        # cv2.imshow('aaa', img)
        key = cv2.waitKey(1) & 0xFF
        if key == close_key:
            cameraDrone.stopCapture()
            cameraWeb.stopCapture()
            break


    

if __name__ == "__main__":
    main()