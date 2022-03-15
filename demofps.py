from snipped_imutils import WebcamVideoStream
import cv2
import time
from copy import deepcopy

def runccc():
    # stream = cv2.VideoCapture(0)
    prev_frame_time = 0
    new_frame_time = 0
    vs = WebcamVideoStream(src=0)
    vs.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    vs.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    vs.start()
    # Fps = FPS().start()
    close_key = ord('q')
    print(f'press {chr(close_key)} to exit')
    # no_frame_key = ord('f')
    # row = 5
    # col = 70
    while True:
        # (ret, frame) = stream.read()
        frame = vs.read()
        # frame = cv2.flip(frame, 1)
        # frame = imutils.resize(frame, width=400)
        new_frame_time = time.time()
        fps = int(1//(new_frame_time - prev_frame_time))
        prev_frame_time = new_frame_time

        key = cv2.waitKey(1) & 0xFF
        if(key == close_key):
            break
        
        
        # Fps.update()
        isolated_frame = deepcopy(frame) #isolate biar ga numpuk dengan cara di copy
        yield isolated_frame, fps
        # yield frame, fps #text, and any tempering will saling tumpuk


    # Fps.stop()
    # print("[INFO] elasped time: {:.2f}".format(Fps.elapsed()))
    # print("[INFO] approx. FPS: {:.2f}".format(Fps.fps()))
    # stream.release()
    vs.stop()
    cv2.destroyAllWindows()


def main():
    # texu = ("ini 1", "ini 2")
    # id = 0
    row, col = 10, 50
    for locframe, fps in runccc():
        cv2.putText(locframe, f'FPS: {fps}', (row, col), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('Camera', locframe)
        # row, col = row+20, col+20
        # row, col = row%200, col%200
        # id+=1
        # id%=2

if __name__ == "__main__":
    main()