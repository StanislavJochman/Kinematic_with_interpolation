import cv2
import numpy as np
import time
from functions import *


img = createCanvas(width = 720,height = 480)
createUI(img)

while True:
	X_pos = cv2.getTrackbarPos('X_cor','Kinematic')
	Y_pos = cv2.getTrackbarPos('Y_cor','Kinematic')
	img = updateCanvas(img,countFPS(),X_pos,Y_pos)
	cv2.imshow("Kinematic",img)
	handleQuit('Kinematic')

