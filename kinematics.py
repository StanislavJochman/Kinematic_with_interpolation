import math
def calKinematics(arm_l,posX,posY):
	if(posY==0):
		posY = 1
	lenght = math.sqrt(posX**2 + (posY)**2)
	alfa = math.degrees(math.asin(posX/lenght))
	vyska = math.sqrt(arm_l**2-(lenght/2)**2)
	alfa = math.degrees(math.asin(vyska/arm_l))+alfa
	x_cor = math.sin(math.radians(alfa))*arm_l
	y_cor = arm_l * math.cos(math.radians(alfa))  
	return [int(x_cor),int(y_cor),posX,posY]

calKinematics(37.5,50,0)