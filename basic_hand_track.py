import cv2
import numpy as np
import mediapipe as mp
from soeroCamUtils import SoeroCam

def main():
    mp_drawing = mp.solutions.drawing_utils # helper to draw
    mp_hand = mp.solutions.hands # all hand utils
    hand_tracker = mp_hand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) 
    
    camera = SoeroCam() # camera for video input
    close_key = ord('q') # what key to press to exit
    
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
        if (results.multi_hand_landmarks):
            for hand in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand, mp_hand.HAND_CONNECTIONS)
        
        
        cv2.imshow('HandTracking', img)
        key = cv2.waitKey(1) & 0xFF
        if key == close_key:
            camera.stopCapture()
            break


    

if __name__ == "__main__":
    main()