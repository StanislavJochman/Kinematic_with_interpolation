import cv2
import numpy as np
import time
from kinematics import *

reset_button = None
captured_pos = []
do_walking = False
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
	global reset_button,walk_button,capture_button
	img = 255 * np.ones(shape=[height, width, 3], dtype=np.uint8)
	cv2.namedWindow('Kinematic')
	cv2.rectangle(img, (0, height-30), (width, height), (0, 0, 0), -1)
	cv2.putText(img,'www.stanislavjochman.sk',(10, height-10), cv2.FONT_HERSHEY_PLAIN, 1.5,(255, 255, 255),1,cv2.LINE_AA)
	reset_button = createButton(img,width-75,25,"Reset         ")
	walk_button = createButton(img,width-75,77,"Walk            ")
	capture_button = createButton(img,width-75,129,"Capture   ")
	return img

def createButton(img,x,y,text):
	button = Button(x,y,text)
	cv2.rectangle(img, (button.size_x[0],button.size_y[0]), (button.size_x[1],button.size_y[1]), (0, 0, 0), -1)
	text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 1.5, 1)[0][0]
	cv2.putText(img,text,(button.size_x[0]+text_size//4, button.size_y[0]+32), cv2.FONT_HERSHEY_PLAIN, 1.5,(255, 255, 255),1,cv2.LINE_AA)
	return button

def getCanvas_size(img):
	return [len(img[0]),len(img)]

def capturePos():
	global captured_pos
	X_pos = cv2.getTrackbarPos('X_cor','Kinematic')
	Y_pos = cv2.getTrackbarPos('Y_cor','Kinematic')
	captured_pos.append([X_pos-150,Y_pos])
	print(captured_pos)

def mouseClick(event, x, y, flags, param):
	if(x in range(reset_button.size_x[0],reset_button.size_x[1]) and y in range(reset_button.size_y[0],reset_button.size_y[1]) and event == cv2.EVENT_LBUTTONDOWN):
		resetTrackbar()
	elif(x in range(walk_button.size_x[0],walk_button.size_x[1]) and y in range(walk_button.size_y[0],walk_button.size_y[1]) and event == cv2.EVENT_LBUTTONDOWN):
		walk()
	elif(x in range(capture_button.size_x[0],capture_button.size_x[1]) and y in range(capture_button.size_y[0],capture_button.size_y[1]) and event == cv2.EVENT_LBUTTONDOWN):
		capturePos()

def resetTrackbar():
	global captured_pos,do_walking
	do_walking = False
	cv2.setTrackbarPos('X_cor','Kinematic',150)
	cv2.setTrackbarPos('Y_cor','Kinematic',100)
	captured_pos = []

def walk():
	global captured_pos,do_walking
	if(len(captured_pos)==0):
		print("No captured positions")
	else:
		do_walking = True

def getValues():
	return do_walking,captured_pos

def createUI(img):
	width ,height = len(img[0]),len(img)
	cv2.createTrackbar('X_cor','Kinematic',0,300,nothing)
	cv2.createTrackbar('Y_cor','Kinematic',0,200,nothing)
	resetTrackbar()
	cv2.setMouseCallback("Kinematic", mouseClick)
	
def updateCanvas(img,fps,X_pos,Y_pos,legposition):
	width ,height = len(img[0]),len(img)
	img = createCanvas(width = width, height = height)
	cv2.putText(img,"FPS: "+str(fps),(width-100, height-10), cv2.FONT_HERSHEY_PLAIN, 1.5,(255, 255, 255),1,cv2.LINE_AA)
	img = drawBody(img,legposition)
	img = drawLeg(img,X_pos,Y_pos,[legposition[0]+60,legposition[1]])
	img = drawLeg(img,X_pos,Y_pos,[legposition[0]-220,legposition[1]])
	for x in range(len(captured_pos)):
		drawCross(img,[captured_pos[x][0]+legposition[0]+60,captured_pos[x][1]+legposition[1]],5)
		drawCross(img,[captured_pos[x][0]+legposition[0]-220,captured_pos[x][1]+legposition[1]],5,color = (255,0,0))
	return img

def drawCross(img,pos,size,thickness = 2,color = (0,0,255)):
	cv2.line(img,(pos[0]-size,pos[1]-size),(pos[0]+size,pos[1]+size),color,thickness)
	cv2.line(img,(pos[0]-size,pos[1]+size),(pos[0]+size,pos[1]-size),color,thickness)

def drawBody(img,legposition):
	cv2.circle(img,(legposition[0]+85, legposition[1]-35),35,(0,204, 255), -1)
	cv2.circle(img,(legposition[0]+105, legposition[1]-45),5,(0,0, 0), -1)
	cv2.rectangle(img, (legposition[0]-240, legposition[1]+10), (legposition[0]+80, legposition[1]-30), (0,204, 255), -1)
	return img

def drawLeg(img,X_pos,Y_pos,legposition):
	kinematics = calKinematics(130,X_pos,Y_pos)
	cv2.line(img,(legposition[0],legposition[1]),(legposition[0]+kinematics[2],legposition[1]+kinematics[3]),(100,100,100),1)
	cv2.circle(img,(legposition[0],legposition[1]),5,(255,128,0),-1)
	cv2.line(img,(legposition[0],legposition[1]),(legposition[0]+kinematics[0],legposition[1]+kinematics[1]),(0,255,0),2)
	cv2.circle(img,(legposition[0]+kinematics[0],legposition[1]+kinematics[1]),5,(255,128,0),-1)
	cv2.line(img,(legposition[0]+kinematics[0],legposition[1]+kinematics[1]),(legposition[0]+kinematics[2],legposition[1]+kinematics[3]),(255,0,255),2)
	return img
def countFPS():
	global start_time
	fps = int(1/(time.time()-start_time))
	start_time = time.time()
	return fps

