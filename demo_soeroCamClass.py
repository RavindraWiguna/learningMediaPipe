from soeroCamUtils import SoeroCam
import cv2
import time

def main():
    camera = SoeroCam(src=0, width=640, height=480, isMirrored=True)
    close_key = ord('q')
    prev_frame_time = 0
    new_frame_time = 0
    for img in camera.infiniteCapture():
        # print(f'm:{c}')
        new_frame_time = time.time()
        fps = int(1//(new_frame_time - prev_frame_time))
        prev_frame_time = new_frame_time
        cv2.putText(img, f'FPS: {fps}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('Camera', img)
        key = cv2.waitKey(1) & 0xFF
        if(key == close_key):
            camera.stopCapture()
            cv2.destroyAllWindows()
            break
        # time.sleep(1) ceritanya simulate ngelag di main(), ternyata print printan {c}: counter nya sama
    
    # camera.startCapture()
    # newFrame = camera.singleCapture()
    # cv2.imshow('New Frame', newFrame)
    # key = cv2.waitKey(0) & 0xFF
    # if(key):
    #     print("this")
    #     camera.stopCapture()
    #     cv2.destroyAllWindows()
    print("End of program")


if __name__=="__main__":
    main()