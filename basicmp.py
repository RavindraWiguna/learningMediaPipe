#!/usr/bin/python3
import mediapipe as mp
import cv2
import time

def run_camera(source):
    cap = cv2.VideoCapture(source)
    #check if camera/device valid
    if( cap is None or not cap.isOpened()):
        raise Exception(f'Unable to open camera by index: {source}')
    
    close_key = ord('q')
    print(f'press: {chr(close_key)} to exit')
    prev_frame_time = 0
    new_frame_time = 0
    fps = None
    while(cap.isOpened()):
        ret, img = cap.read()

        new_frame_time = time.time()
        fps = str(1//(new_frame_time - prev_frame_time))
        prev_frame_time = new_frame_time
        # yield frame, fps
        # fps = str(cap.get(5))
        cv2.putText(img, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('Camera', img)
        if(cv2.waitKey(1) & 0xFF == close_key):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    run_camera(0)
    # for img, fps in run_camera(0):
        # cv2.putText(img, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
        # cv2.imshow('Camera', img)


if __name__=="__main__":
    main()