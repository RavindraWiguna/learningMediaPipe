import cv2
import mediapipe as mp
from soeroCamUtils import SoeroCam
import pyttsx3 as speech
from mycv2 import createBoxWithText
import numpy as np

def findMiddlePoint(point1, point2, width, height):
    return (int((point1.x+point2.x)/2*width), int((point1.y+point2.y)/2*height),)


def main():
    # mediapipe stuff
    mp_drawing = mp.solutions.drawing_utils # helper to draw
    mp_drawing_styles = mp.solutions.drawing_styles #also a helper, but for style B)
    mp_hands = mp.solutions.hands # all hand utils
    hand_tracker = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands = 2) 
    # open cv cam stuff
    cameraDrone = SoeroCam(width=1440, height=1080,isMirrored=False, src="/dev/video2") # camera for video input
    # print(cameraDrone.getOriginalCamDim())
    cameraWeb = SoeroCam(width=800, height=600, isMirrored=True, src=0)
    close_key = ord('q') # what key to press to exit
    
    #speech stuff
    engine = speech.init()

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
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # get fpv frame
        fpvFrame = cameraDrone.singleCapture()

        #add rect
        fpvFrame[0: lrh, left_rect_x: left_rect_x +lrw] = left_hand_rect
        fpvFrame[0:rrh, right_rect_x: right_rect_x + rrw] = right_hand_rect
        # print(cv2.getTextSize("LEFT HAND", cv2.FONT_HERSHEY_SIMPLEX, fontScale, 2))
        cv2.line(fpvFrame,(mid_x,0),(mid_x,cameraDrone.height),(255,0,0),3)
        # fpvFrame = cv2.resize(fpvFrame, (1440, 1080))
        cv2.circle(fpvFrame,(mid_x//2,cameraDrone.height//2), 32, (0,0,255), -1)
        
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
         
        # if(total_hand<2):
            # engine.say(f'LOST {2-total_hand} HAND')
            # engine.runAndWait() #need threader
            
        
        midPoints = []
        for i in range(total_hand):
            midPoints.append(findMiddlePoint(thumbTip[i], indexTip[i], cameraDrone.width, cameraDrone.height))
        
        for point in midPoints:
            # print(type(point[0]))
            print(point)
            cv2.line(fpvFrame, (mid_x//2,cameraDrone.height//2), point, (255, 128, 56), 3)
        cv2.imshow('HandTracking', fpvFrame)
        # cv2.imshow('aaa', img)
        key = cv2.waitKey(1) & 0xFF
        if key == close_key:
            cameraDrone.stopCapture()
            cameraWeb.stopCapture()
            break


    

if __name__ == "__main__":
    main()