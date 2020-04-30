import cv2
import numpy as np
import time
import math

reset_button = None
def nothing(x):
	pass

class Button:
	def __init__(self, x, y, text):
		self.text = text
		self.size_x = [x-75,x+75]
		self.size_y = [y-25,y+25]

start_time = time.time()
def handleQuit(windowname):
	if cv2.waitKey(25) & 0xFF == 27 or cv2.getWindowProperty(windowname, cv2.WND_PROP_VISIBLE) ==0:
		cv2.destroyAllWindows()
		exit()

def createCanvas(width,height):
	global reset_button,walk_button
	img = 255 * np.ones(shape=[height, width, 3], dtype=np.uint8)
	cv2.namedWindow('Kinematic')
	cv2.rectangle(img, (0, height-30), (width, height), (0, 0, 0), -1)
	cv2.putText(img,'www.stanislavjochman.sk',(10, height-10), cv2.FONT_HERSHEY_PLAIN, 1.5,(255, 255, 255),1,cv2.LINE_AA)
	reset_button = createButton(img,width-75,25,"Reset         ")
	walk_button = createButton(img,width-75,77,"Walk            ")
	return img

def createButton(img,x,y,text):
	button = Button(x,y,text)
	cv2.rectangle(img, (button.size_x[0],button.size_y[0]), (button.size_x[1],button.size_y[1]), (0, 0, 0), -1)
	text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 1.5, 1)[0][0]
	cv2.putText(img,text,(button.size_x[0]+text_size//4, button.size_y[0]+32), cv2.FONT_HERSHEY_PLAIN, 1.5,(255, 255, 255),1,cv2.LINE_AA)
	return button

def walk():
	print("walking")

def mouseClick(event, x, y, flags, param):
	if(x in range(reset_button.size_x[0],reset_button.size_x[1]) and y in range(reset_button.size_y[0],reset_button.size_y[1]) and event == cv2.EVENT_LBUTTONDOWN):
		resetTrackbar()
	elif(x in range(walk_button.size_x[0],walk_button.size_x[1]) and y in range(walk_button.size_y[0],walk_button.size_y[1]) and event == cv2.EVENT_LBUTTONDOWN):
		walk()
def resetTrackbar():
	cv2.setTrackbarPos('X_cor','Kinematic',100)
	cv2.setTrackbarPos('Y_cor','Kinematic',100)

def createUI(img):
	width ,height = len(img[0]),len(img)
	cv2.createTrackbar('X_cor','Kinematic',0,200,nothing)
	cv2.createTrackbar('Y_cor','Kinematic',0,200,nothing)
	resetTrackbar()
	cv2.setMouseCallback("Kinematic", mouseClick)
	


def updateCanvas(img,fps,X_pos,Y_pos):
	width ,height = len(img[0]),len(img)
	img = createCanvas(width = width, height = height)
	cv2.putText(img,"FPS: "+str(fps),(width-100, height-10), cv2.FONT_HERSHEY_PLAIN, 1.5,(255, 255, 255),1,cv2.LINE_AA)
	cv2.line(img,(width//2,0),(width//2+X_pos,0+Y_pos),(100,100,100),5)
	return img

def countFPS():
	global start_time
	fps = int(1/(time.time()-start_time))
	start_time = time.time()
	return fps