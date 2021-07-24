from numpy.lib.function_base import diff
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
from datetime import datetime
import Levenshtein


class DetectVideoFaceMasks:
	def loadFaceAndMaskModels(self):
		# load face detector model
		prototxtPath = "models/deploy.prototxt"
		weightsPath = "models/res10_300x300_ssd_iter_140000.caffemodel"
		net = cv2.dnn.readNet(prototxtPath, weightsPath)
		# load model
		model = load_model('models/CNN_FaceMaskDetector1.h5')
		return net, model
	

	def faceMaskDetectionAndPredication(self,frame, net, model):
		# grab the dimensions of the frame and then construct a blob from it
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 177.0, 123.0))
		
		net.setInput(blob)
		detections = net.forward()
		
		faces = []
		locations = []
		predications = []
		
		for i in range(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			
			if confidence > 0.9:
				
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				
				(startX, startY) = (max(0, startX), max(0, startY))
				(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

				face = frame[startY:endY, startX:endX]
				face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
				face = cv2.resize(face, (224, 224))
				face = img_to_array(face)
				face = preprocess_input(face)
				
				faces.append(face)
				locations.append((startX, startY, endX, endY))
				
		# only make a predictions if at least one face was detected
		if len(faces) > 0:
			# for faster inference we'll make batch predictions on *all*
			# faces at the same time rather than one-by-one predictions
			# # in the above `for` loop
			faces = np.array(faces, dtype="float32")
			predications = model.predict(faces, batch_size=32)
		
		return (locations, predications)
	
	
	def run(self):
		vs = VideoStream(src=0).start()
		time.sleep(2.0)
		net, model = self.loadFaceAndMaskModels()
		
		indx = 1
		startTime = datetime.now()
		# loop over the frames from the video stream
		while True:
			flag = 0
			frame = vs.read()
			frame = imutils.resize(frame, width=800)

			(locs, preds) = self.faceMaskDetectionAndPredication(frame, net, model)
			
			# loop over the detected face locations and their corresponding locations
			for (box, pred) in zip(locs, preds):
				(startX, startY, endX, endY) = box
				(mask, withoutMask) = pred

				label = "Mask" if mask > withoutMask else "No Mask"
				if label == "No Mask":
					flag = 1
				
				color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
				label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

				cv2.putText(frame, label, (startX, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
				cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
			
			
			currentTime = datetime.now()
			difference = currentTime - startTime
			diffInMinutes = difference.total_seconds() / 60
			if flag == 1 and diffInMinutes >= 0.5:
				# ct stores current date 
				ct = datetime.date(datetime.now())
				# reset start time
				startTime = datetime.now()
				directory = r'C:/Users/Huseen/Desktop/saved'
				os.chdir(directory) 
				filename = str(ct) + "(" + str(indx) +  ").jpg"
				cv2.imwrite(filename, frame) 
				indx += 1	
				

			cv2.imshow("Live Stream", frame)
			key = cv2.waitKey(1) & 0xFF
			
			if key == ord("q"):
				break
			
		cv2.destroyAllWindows()
		vs.stop()


#detectvideodfacemasks = DetectVideoFaceMasks()
#detectvideodfacemasks.run()
