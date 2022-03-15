import cv2
import numpy as np
import mediapipe as mp
from soeroCamUtils import SoeroCam

def main():
    mp_drawing = mp.solutions.drawing_utils # helper to draw
    mp_drawing_styles = mp.solutions.drawing_styles #also a helper, but for style B)
    mp_hands = mp.solutions.hands # all hand utils
    hand_tracker = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands = 2) 
    
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
            for hand in results.multi_hand_landmarks: #a list of hand landmark
                print(
                    f'Index finger tip coordinates: (',
                    f'{hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * camera.width}, '
                    f'{hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * camera.height})'
                )
                mp_drawing.draw_landmarks(
                    img, 
                    hand, 
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        
        
        cv2.imshow('HandTracking', img)
        key = cv2.waitKey(1) & 0xFF
        if key == close_key:
            camera.stopCapture()
            break


    

if __name__ == "__main__":
    main()