'''
This code is taken from imutils module, because only need webcamvideostream class
'''
from copy import deepcopy
from threading import Thread
import cv2
import time

#Base Cam Class edited from imutils
class WebCamVideoStream:
	def __init__(self, src=0, name="WebcameVideoStream"):
		# initialze the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		if(self.stream is None or not self.stream.isOpened()):
			raise Exception(f'Unable to open camera by index/path {src}')
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name

		# initialize the variable used to indicate if thread should be
		# stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		return self
	
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
			
			#  otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
	
	def read(self):
		# return the frame most recently read
		return self.frame
	
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		self.stream.release()

#Inherit from WebCamVideoStream and Add FPS counter
class SoeroCam(WebCamVideoStream):
	def __init__(self, src=0, name="WebcameVideoStream"):
		super().__init__(src, name)
		self.fps = 0
		self.isolated_frame = None
		# self.start()
		print("Thread started")
	
	def update(self):
		prev_frame_time = 0 # hold previous frame timestamp
		new_frame_time = 0 #hold new frame timestamp
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
			
			#  otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
			new_frame_time = time.time()
			self.fps = int(1//(new_frame_time - prev_frame_time))
			prev_frame_time = new_frame_time
	
	def read(self):
		self.isolated_frame = deepcopy(self.frame)
		return self.fps, self.isolated_frame
