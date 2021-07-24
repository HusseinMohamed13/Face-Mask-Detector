from keras.applications.mobilenet_v2 import preprocess_input
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np

class DetectMaskImage:

	# set image path
	def __init__(self,image):
		self.image = image
		
	# prepare the face image
	def prepareFace(self,startX, startY, endX, endY):
		face = self.image[startY:endY, startX:endX]
		face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
		face = cv2.resize(face, (224, 224))
		face = img_to_array(face)
		face = preprocess_input(face)
		face = np.expand_dims(face, axis=0)
		return face

	# load model and predict the class of image "Mask" or "Without_Mask"
	def predictClass(self,face):
		model = load_model('models/CNN_FaceMaskDetector1.h5')
		result = model.predict(face)
		if(result[0][0]>result[0][1]):
			return "Mask",result[0][0]*100
		else:
			return "no Mask",result[0][1]*100
	
	# load face detector model and image , detect faces in image
	def getDetectionFaces(self):
		# load face detector model
		prototxtPath = "models/deploy.prototxt"
		weightsPath = "models/res10_300x300_ssd_iter_140000.caffemodel"
		net = cv2.dnn.readNet(prototxtPath, weightsPath)
	    
		# construct a blob from the image
		blob = cv2.dnn.blobFromImage(self.image, 1.0, (300, 300),(104.0, 177.0, 123.0))
		
		# pass the blob through the network and obtain the face detections
		net.setInput(blob)
		detections = net.forward()
		return detections

	def run(self):
		detections = self.getDetectionFaces()
		(h, w) = self.image.shape[:2]
       
		# loop over the detections
		for i in range(0, detections.shape[2]):
			#get probability associated with the detection
			probability = detections[0, 0, i, 2]
			# filter out weak detections
			if probability > 0.4:
				# compute the (x, y)-coordinates of the bounding box for the object
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				(startX, startY) = (max(0, startX), max(0, startY))
				(endX, endY) = (min(w - 1, endX), min(h - 1, endY))
			
				face = self.prepareFace(startX, startY, endX, endY)
				
				# detect if face has mask or not
				label,percentage = self.predictClass(face)				
				
				color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
				
				# include the probability in the label
				label = "{}: {:.2f}%".format(label, percentage)

				# display the label and bounding box rectangle on the output frame
				cv2.putText(self.image, label, (startX, startY - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
				cv2.rectangle(self.image, (startX, startY), (endX, endY), color, 2)

		cv2.imshow("Output", self.image)
		cv2.waitKey(0)
