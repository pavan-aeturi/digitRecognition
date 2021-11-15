import pygame
import numpy as np
import tensorflow as tf
from button import button
BLUE=[106,159,181]
RED=[255,0,0]
c=(230, 230, 255)
ROW=28
COL=28
UNIT=15
MSG_HEIGHT=UNIT*5

def displayMessage(msg,window,fontsize=20):
	Setdst=button(BLUE,0,(ROW*UNIT)+1,(ROW*UNIT)+1,MSG_HEIGHT,msg)
	Setdst.draw(window,fontsize=fontsize)
	pygame.display.update()
def createHurdles(h,grid,ar):
	if ar==1:
		pygame.draw.rect(window,(0,0,0),(h[0]*UNIT+2,h[1]*UNIT+2,UNIT-2,UNIT-2))
		grid[h[1]][h[0]]=0
		pygame.display.update()
	else:
		pygame.draw.rect(window,(255,255,255),(h[0]*UNIT+2,h[1]*UNIT+2,UNIT-2,UNIT-2))
		grid[h[1]][h[0]]=1
		pygame.display.update()

def drawInitialSetup(window):
	window.fill((255,255,255))
	for x in range(0,(ROW*UNIT)+1,UNIT):
		pygame.draw.line(window,c,(0,x),((ROW*UNIT)+1,x),2)
	for y in range(0,(ROW*UNIT)+1,UNIT):
		pygame.draw.line(window,c,(y,0),(y,(ROW*UNIT)+1),2)
	displayMessage("Draw any digit and press P",window,fontsize=16)
	pygame.display.update()
    
pygame.init()
window = pygame.display.set_mode(((ROW*UNIT),(COL*UNIT)+MSG_HEIGHT))
pygame.display.set_caption("Predict the Digit")

window.fill((255,255,255))
pygame.display.update()
pygame.display.flip()
def index():
	model = tf.keras.models.load_model('epic_num_reader.model')
	drawInitialSetup(window)
	run=True
	grid=[[1 for x in range(COL)] for y in range(ROW)]
	state = 1
	while run:
		for event in pygame.event.get():
			if state==1 and event.type==pygame.MOUSEBUTTONDOWN and event.button%2==1:
				k=event.button
				follow=True
				while follow:
					pos=pygame.mouse.get_pos()
					if pos[0]>=0 and pos[0]<COL*UNIT and pos[1]>=0 and pos[1]<ROW*UNIT:
						h=(int(pos[0]/UNIT),int(pos[1]/UNIT))
						createHurdles(h,grid,k)
					else:
						break
					for event in pygame.event.get():
						if event.type==pygame.MOUSEBUTTONUP and event.button%2==1:
							follow=False
			if state==1 and event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					grid=np.array(grid)
					grid=abs(1-grid)
					x_test = np.array([[[0 for i in range(28)] for j in range(28)]])
					for row in range(28):
						for x in range(28):
 							x_test[0][row][x] = grid[row][x]
 							if grid[row][x]==1:
 								for dr in [[-1,1],[-1,0],[-1,-1],[0,1],[0,-1],[1,0],[1,-1],[1,1]]:
 									dx,dy=dr
 									if row+dx>=0 and row+dx<28 and x+dy>=0 and x+dy<28:
 										x_test[0][row+dx][x+dy] = (x_test[0][row+dx][x+dy]+1)/2
					predictions = model.predict(x_test[:1])
					t = (np.argmax(predictions[0]))
					displayMessage("Prediction: "+str(t)+" Press R (Restart)",window,fontsize=20)
					state=2
			if state==2 and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				state=1
				grid=[[1 for x in range(COL)] for y in range(ROW)]
				drawInitialSetup(window)
			if event.type==pygame.QUIT:
				pygame.quit()
				run=False


if __name__=="__main__":
    try:
    	index()
    except:
    	pass