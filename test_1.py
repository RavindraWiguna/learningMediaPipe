from soeroCam_old import SoeroCam
import cv2

def main():
    camera = SoeroCam(0)
    isRunning = True
    close_key = ord('q')
    row, col = 10, 50
    camera.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera.start()
    while isRunning:
        fps, frame = camera.read()
        cv2.putText(frame, f'FPS: {fps}', (row,col), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('Camera', frame)
        key = cv2.waitKey(1) & 0xFF
        if(key == close_key):
            isRunning = False
    
    #clean up
    camera.stop()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()