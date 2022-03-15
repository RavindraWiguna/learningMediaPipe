import cv2

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

    def infiniteCapture(self):
        tw, th = 0, 0
        while self.isCapturing:
            # grab frame from camera
            (self.grabbed, self.frame) = self.camera.read()
            # mirrored if needed
            if(self.isMirrored):
                self.frame = cv2.flip(self.frame, 1)
            # get camera dimension
            tw, th = self.getOriginalCamDim()
            # resize frame according to dezired ratio
            ratio = max(self.height/th, self.width/tw) 
            self.frame = cv2.resize(self.frame, (int(tw*ratio), int(th*ratio)))
            yield self.frame[0:self.height, 0:self.width, :]

    def stopCapture(self):
        self.isCapturing = False
        self.camera.release()
        print(f'Stopped Capturing from: {self.src}')
    
