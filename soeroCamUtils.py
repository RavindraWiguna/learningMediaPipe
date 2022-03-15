import cv2
'''
Todo: add single capture, add re capture after stopping, add finish all (until release())
'''
class SoeroCam:
    def __init__(self, src=0, width=640, height=480, isMirrored=False) -> None:
        # initialize video camera stream 
        self.src = src
        self.camera = cv2.VideoCapture(self.src)

        # throw exceptions if unable to open camera
        if(self.camera is None or not self.camera.isOpened()):
            raise Exception(f'Unable to open camera by index/path {src}')
        
        # dimension of outputed frame
        self.width = width
        self.height = height
        assert (self.width > 0 and self.height > 0), "Width and Height must be > 0"
        
        # get the first frame
        (self.grabbed, self.frame) = self.camera.read()
        
        # boolean to indicate stop getting frame
        self.isCapturing = True
        # boolean to indicate wether or not a frame is mirrored
        self.isMirrored = isMirrored

    def getOriginalCamDim(self): # return width and height of the camera
        return self.camera.get(cv2.CAP_PROP_FRAME_WIDTH), self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def setOriginalCamDim(self, width: int, height: int):
        # set width and height of the camera
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def startCapture(self):
        # set the boolean indicating start capturing
        self.isCapturing=True
        # reopen the camera if once was released
        self.camera.open(self.src)

    def stopCapture(self):
        # set the boolean indicating stop capturing
        self.isCapturing = False
        # release the device I/O, and free the pointer/memory
        self.camera.release()
        print(f'Stopped Capturing from: {self.src}')
    
    def processFrame(self):
        # process frame according to setup (mirror, width, height)
        if(self.isMirrored):
            self.frame = cv2.flip(self.frame, 1)
        tw, th = self.getOriginalCamDim()
        ratio = max(self.height/th, self.width/tw)
        self.frame = cv2.resize(self.frame, (int(tw*ratio), int(th*ratio)))
        self.frame = self.frame[0:self.height, 0:self.width, :]
    
    def infiniteCapture(self):
        while self.isCapturing:
            # grab frame from camera
            (self.grabbed, self.frame) = self.camera.read()
            # process it
            self.processFrame()
            yield self.frame

    def singleCapture(self):
        # exit if not capturing
        if(not self.isCapturing):
            return None
        
        # grab the frame
        (self.grabbed, self.frame) = self.camera.read()
        # process it
        self.processFrame()
        return self.frame