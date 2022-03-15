import cv2
import numpy as np
import mediapipe as mp
from soeroCamUtils import SoeroCam
import pyttsx3 as speech


def main():
    # mediapipe stuff
    mp_drawing = mp.solutions.drawing_utils # helper to draw
    mp_hand = mp.solutions.hands # all hand utils
    hand_tracker = mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands = 2) 
    # open cv cam stuff
    camera = SoeroCam(width=960, height=720,isMirrored=True) # camera for video input
    close_key = ord('q') # what key to press to exit
    
    #speech stuff
    engine = speech.init()

    # units
    fontScale = camera.width/960
    unit_x = camera.width//32
    mid_x = unit_x*16
    font_pix = fontScale*17

    # x pos of text
    x_left = int(mid_x - font_pix*10 - font_pix*7)
    x_right = int(mid_x+7*font_pix)
    # y pos of text
    y_text = camera.height//24
    
    # rectangle ui sutff
    RECT_COLOR = (255, 193, 7)
    rect_h, rect_w = int(39*fontScale), int(font_pix*12)
    left_rect = np.full((rect_h, rect_w,3), RECT_COLOR, np.uint8)
    right_rect = np.full((rect_h, int(rect_w+font_pix),3), RECT_COLOR, np.uint8)
    left_rect_x = int(x_left-font_pix)
    right_rect_x = int(x_right-font_pix)    
    lrh, lrw,_ = left_rect.shape
    rrh, rrw,_ = right_rect.shape

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
                mp_drawing.draw_landmarks(img, hand, mp_hand.HAND_CONNECTIONS)
                total_hand+=1
         
        # if(total_hand<2):
            # engine.say(f'LOST {2-total_hand} HAND')
            # engine.runAndWait() #need threader
            
        #add rect
        img[0: lrh, left_rect_x: left_rect_x +lrw] = left_rect
        img[0:rrh, right_rect_x: right_rect_x + rrw] = right_rect
        cv2.putText(img, f'LEFT HAND', (x_left, y_text), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, f'RIGHT HAND', (x_right, y_text), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.line(img,(mid_x,0),(mid_x,camera.height),(255,0,0),3)
        cv2.imshow('HandTracking', img)
        key = cv2.waitKey(1) & 0xFF
        if key == close_key:
            camera.stopCapture()
            break


    

if __name__ == "__main__":
    main()