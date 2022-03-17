import cv2
import mediapipe as mp
from soeroCamUtils import SoeroCam
import pyttsx3 as speech
from mycv2 import createBoxWithText
import numpy as np

def main():
    # mediapipe stuff
    mp_drawing = mp.solutions.drawing_utils # helper to draw
    mp_hand = mp.solutions.hands # all hand utils
    hand_tracker = mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands = 2) 
    # open cv cam stuff
    camera = SoeroCam(width=640, height=480,isMirrored=True) # camera for video input
    close_key = ord('q') # what key to press to exit
    
    #speech stuff
    engine = speech.init()

    # units
    fontScale = camera.width/960
    unit_x = camera.width//32
    mid_x = unit_x*16
    
    # rectangle ui sutff
    RECT_COLOR = (255, 193, 7)
    left_hand_rect =createBoxWithText("THROTLE / YAW", fontScale, 2, cv2.FONT_HERSHEY_SIMPLEX, RECT_COLOR, (255, 255, 255))
    right_hand_rect  =createBoxWithText("PITCH/ ROLL", fontScale, 2, cv2.FONT_HERSHEY_SIMPLEX, RECT_COLOR, (255, 255, 255))

    lrh, lrw,_ = left_hand_rect.shape
    rrh, rrw,_ = right_hand_rect.shape
    left_rect_x = (mid_x - lrw)//2
    right_rect_x = mid_x + (mid_x - rrw)//2

    black_screen = np.zeros((camera.height, camera.width, 3), np.uint8)

    # loop for each frame captured
    for img in camera.infiniteCapture():
        # convert img from BGR to RGB because mediapipe takes RGB image
        # and opencv default is BGR
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        img.flags.writeable = False

        # Detect!
        results = hand_tracker.process(img)

        # makes img writable
        img.flags.writeable = True

        # convert back to BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # draw the results!
        total_hand = 0
        if (results.multi_hand_landmarks):
            for hand in results.multi_hand_landmarks:#a list of hand landmark
                mp_drawing.draw_landmarks(black_screen, hand, mp_hand.HAND_CONNECTIONS)
                total_hand+=1
                # print(f'{len(hand.landmark)} and type: {type(hand.landmark)}')
                # print("======1=====")
         
        # if(total_hand<2):
            # engine.say(f'LOST {2-total_hand} HAND')
            # engine.runAndWait() #need threader
            
        #add rect
        img[0: lrh, left_rect_x: left_rect_x +lrw] = left_hand_rect
        img[0:rrh, right_rect_x: right_rect_x + rrw] = right_hand_rect
        # print(cv2.getTextSize("LEFT HAND", cv2.FONT_HERSHEY_SIMPLEX, fontScale, 2))
        cv2.line(img,(mid_x,0),(mid_x,camera.height),(255,0,0),3)
        cv2.imshow('HandTracking', img)
        cv2.imshow('AR ceritanya', black_screen)
        black_screen = np.zeros((camera.height, camera.width, 3), np.uint8)
        key = cv2.waitKey(1) & 0xFF
        if key == close_key:
            camera.stopCapture()
            break


    

if __name__ == "__main__":
    main()