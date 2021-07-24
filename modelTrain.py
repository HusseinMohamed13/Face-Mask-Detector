# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZllqO5ljtGfCWvCg9xOPuRsS7tTLxRBI
"""

import os
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from sklearn.model_selection import train_test_split
from imutils import paths
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D , Flatten , AveragePooling2D , Dropout
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report


class DataSet:

  def __init__(self):

  def Load(self):
   images=[]
   labels=[]
   print("[INFO] loading images...")
   imagePaths = list(paths.list_images("/content/drive/MyDrive/dataset"))
   for imagePath in imagePaths:
    label = imagePath.split(os.path.sep)[-2]
    image = load_img(imagePath,target_size=(224, 224))
    image = img_to_array(image)
    image = preprocess_input(image)
    images.append(image)
    labels.append(label)

   images = np.array(images)
   labels = np.array(labels)
   lb = LabelBinarizer()
   labels = lb.fit_transform(labels)
   labels = to_categorical(labels)
   return images,labels


class ModelCreation:

  X_train, X_test, y_train, y_test
  def _init_(self):
  
  def prepareDataset(self):
    dataset = DataSet()
    X , Y = dataset.Load()
    ModelCreation.X_train, ModelCreation.X_test, ModelCreation.y_train, ModelCreation.y_test = train_test_split(X, Y, test_size=0.10, random_state=42)

  def trainModel(self):
    # load the MobileNetV2 network, ensuring the head FC layer sets are
    # left off
    baseModel = MobileNetV2(weights="imagenet", include_top=False,input_tensor=Input(shape=(224, 224, 3)))
    # construct the head of the model that will be placed on top of the
    # the base model
    headModel = baseModel.output
    headModel = AveragePooling2D(pool_size=(7, 7))(headModel)
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(128, activation="relu")(headModel)
    headModel = Dropout(0.5)(headModel)
    headModel = Dense(2, activation="softmax")(headModel)
    # place the head FC model on top of the base model (this will become
    # the actual model we will train)
    model = Model(inputs=baseModel.input, outputs=headModel)
    # loop over all layers in the base model and freeze them so they will
    # *not* be updated during the first training process
    for layer in baseModel.layers:
      layer.trainable = False
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()
    model.fit(ModelCreation.X_train, ModelCreation.y_train, epochs=20, batch_size=32)
    model.save("CNN_FaceMaskDetector", save_format="h5")
    ModelCreation.testModel()
  
  def testModel(self,model):
    score = model.evaluate(ModelCreation.X_test, ModelCreation.y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1]) 


model = ModelCreation()
model.prepareDataset()
model.trainModel()