import cv2
import numpy as np
import time
from functions import *



img = createCanvas(width = 720,height = 480)
createUI(img)

while True:
	do_walking, captured_pos = getValues()
	sizeX,sizeY = getCanvas_size(img)
	if (do_walking==True):
		for x in range(len(captured_pos)):
			img = updateCanvas(img,countFPS(),captured_pos[x][0],captured_pos[x][1],[sizeX//2,sizeY//3])
			cv2.imshow("Kinematic",img)
			cv2.waitKey(330)
	else:
		X_pos = cv2.getTrackbarPos('X_cor','Kinematic')-150
		Y_pos = cv2.getTrackbarPos('Y_cor','Kinematic')
		img = updateCanvas(img,countFPS(),X_pos,Y_pos,[sizeX//2,sizeY//3])
		cv2.imshow("Kinematic",img)
		
	handleQuit('Kinematic')

