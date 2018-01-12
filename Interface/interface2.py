import urllib.request
import time
import pygame
import os
import socket
import threading

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")


def loadImages(*args):
	imageList = []
	for arg in args:
		img = pygame.image.load	(os.path.join(img_folder, arg) + ".jpg")
		imageList.append(img)
	return imageList


#images
iLAMP = loadImages("lamp_on","lamp_off")
iWASH = loadImages("wash", "wash_ready", "wash_working","wash_done")
iPLANT = loadImages("plant", "give_water", "water_status")
iSOUND = loadImages("sound")
iWINDOW = loadImages("window_open", "window_closed")

#colors
WHITE 		= 	(255,255,255)
BLACK 		= 	(0,0,0)
LIGHT_BLUE 	= 	(180,233,255)
GREEN		=	(0,255,0)

#GAME CONSTANTS
TITLE 	= 	"Home Destroyinator 2000"
WIDTH 	= 	512
HEIGHT 	= 	768

#Lists and constants for modules and IP
modules = []
currentIP = []
port = 80

#NEW interface values
COLUMNS = 2
SQUARE = 128
SPACING = 80
LEFTINDENT = (WIDTH - 2*SQUARE - SPACING)/2 
TOPINDENT = 172
BORDER = 4
title_x = 50
title_y = 50
refresh_x = 300
refresh_y = 20

class Module():
	#Def thyself and at thyself to the list of thys.
	def __init__(self, ip, typ, name):
		self.ip = ip
		self.typ = typ
		self.name = name
		self.menu = False
		modules.append(self)
		
	def setButton(self, a, b, c, d):
		self.a = a
		self.b = b
		self.c = a+c
		self.d = b+d

	def draw(self,r,c,i=0):
		self.loc = ((LEFTINDENT+c*(SPACING+SQUARE),TOPINDENT+r*(SQUARE+SPACING)))
		pygame.draw.rect(window,BLACK,(self.loc[0]-BORDER,self.loc[1]-BORDER,SQUARE+2*BORDER,SQUARE+2*BORDER),BORDER)
		window.blit(self.image[i],self.loc)	
		self.setButton(self.loc[0],self.loc[1],SQUARE,SQUARE)
		if self.menu == True:
			self.drawMenu()

	def checkModuleButton(self):
		if checkButton(self.a,self.b,self.c,self.d):
			if self.menu == False:
				self.menu = True
			else:
				self.menu = False

	def drawMenu(self):
		pass

class Relais(Module):
	def __init__(self, ip, typ, name):
		
		self.state = "false"
		self.image = iLAMP
		super(Relais,self).__init__(ip,typ,name)
		try:
			socket.setdefaulttimeout(3)
			self.state = str(urllib.request.urlopen("http://" + str(self.ip) + "/state").read())[2:-1]
		except:
			print ("cant read state of:" + self.ip)

	def Turn(self):
		try:
			if self.state == "false":
				whois = urllib.request.urlopen("http://" + str(self.ip) + "/on").read()
				print("turned relais on " +  str(self.ip))
				self.state = "true"
			elif self.state == "true":
				whois = urllib.request.urlopen("http://" + str(self.ip) + "/off").read()
				self.state = "false"
				print("turned relais off "  + str(self.ip))
			else: print ("error in data while turning: " + str(self.ip))
		except Exception as e:
			print ("Error in turning relais: Can't connect to page")
	
	def checkModuleButton(self):
		if checkButton(self.a,self.b,self.c,self.d):
			self.Turn()

	def draw(self, r, c):
		if self.state =="false":
			i = 1
		else:
			i = 0
		super(Relais,self).draw(r,c,i)

class Plant(Module):
	def __init__(self, ip, typ, name):
		self.state = "0"
		self.image = iPLANT
		super(Plant,self).__init__(ip,typ,name)

	# def readState(self):
	# 	sta = str(urllib.request.urlopen("http://" + a + "/state").read())[2:-1]
	# 	self.state = sta

	def drawMenu(self):
		window.blit(self.image[2],(self.loc[0]+SQUARE+BORDER,self.loc[1]+SQUARE/4))	
		window.blit(self.image[1],(self.loc[0],self.loc[1]+SQUARE+BORDER*2))
		if checkButton(self.loc[0],self.loc[1]+SQUARE+BORDER*2,self.loc[0]+32,self.loc[1]+SQUARE+BORDER*2+32):
			print ("Watering")

class Ldr(Module):
	def __init__(self, ip, typ, name):
		self.state = "0"
		self.image = iWASH
		super(Ldr,self).__init__(ip,typ,name)

	# def readState(self):
	# 	sta = str(urllib.request.urlopen("http://" + a + "/state").read())[2:-1]
	# 	self.state = sta


#NOT IMPLEMENTED YET
class Button():
	def __init__(self,size,location,ima):
		self.x = location[0]
		self.y = location[1]
		self.a = location[0]+size[0]
		self.b = location[1]+size[1]
		self.image = ima

	def checkButton(self):
		click = pygame.mouse.get_pressed()
		if  click[0] == 1: 
			mouse = pygame.mouse.get_pos()
			x = mouse[0]
			y = mouse[1]
			if (x>=self.x and x < self.a and y >= self.y and y < self.b):
				return True

	def draw(self):
		pass


	
#Pygame font Init
pygame.font.init()
def text_to_screen(screen, text, x, y, size = 20,
            color = BLACK, font_type = 'Arial'):
    text = str(text)
    font = pygame.font.SysFont(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))



def findModule(a, b, timeOut):
	for i in range(a, b):

		addr = "192.168.15." +  str(i)
		iplist = []
		for m in modules:
			iplist.append(m.ip)
		if addr not in iplist: 
			socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			currentIP[:] = []
			currentIP.append(addr)
			socket.setdefaulttimeout(timeOut)
			result = socket_obj.connect_ex((addr,port))
			if result == 0:
				socket.setdefaulttimeout(3)
				print("Connecting to: " + str(addr) + "/who")

				try:
					whois = str(urllib.request.urlopen("http://" + addr + "/who").read())[2:-1]
					if whois == "relais":
						mod = Relais(str(addr),str(whois),str(whois))
					if whois == "plant":
						mod = Plant(str(addr),str(whois),str(whois))
					if whois == "ldr":
						mod = Ldr(str(addr),str(whois),str(whois))
					print(addr + ": " + str(mod) + " " + str(whois))
				except:
					print("Cant read who page of:" + str(addr))
			socket_obj.close()

#TRHEAD THE SHIT OUT OF IT
threads = []
def refresh():
	
	threads[:] = []
	t = threading.Thread(target=findModule, args=(3,150,0.4))
	threads.append(t)
	t.start()
	t = threading.Thread(target=findModule, args=(151,254,0.4))
	threads.append(t)
	t.start()

def checkButton(a,b,c,d):
	click = pygame.mouse.get_pressed()
	if  click[0] == 1: 
		mouse = pygame.mouse.get_pos()
		x = mouse[0]
		y = mouse[1]
		if (x>=a and x < c and y >= b and y < d):
			return True

def checkState():
	for m in modules:
		try:
			m.state = str(urllib.request.urlopen("http://" + m.ip + "/state").read())[2:-1]
		except:
			print("cant find state for: " + m.ip)

#Pygame initializing things
pygame.init()
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
gameLoop = True

refresh()

while gameLoop:
	for event in pygame.event.get():
		if (event.type==pygame.QUIT):
			gameLoop = False
#INTERFACE YES YES
	window.fill(WHITE)
	text_to_screen(window, "Home Destroyinator 2000", title_x, title_y, size = 20)
	text_to_screen(window, str(currentIP[0]), refresh_x-100, refresh_y, size = 10)
	#Refresh Button
	pygame.draw.rect(window,LIGHT_BLUE,(refresh_x,refresh_y,50,50))
	if checkButton(refresh_x,refresh_y,refresh_x + 50,refresh_y + 50):
		modules[:] = []
		refresh()
	pygame.draw.rect(window,LIGHT_BLUE,(refresh_x + 100,refresh_y,50,50))
	if checkButton(refresh_x + 100,refresh_y,refresh_x + 150,refresh_y + 50):
		checkState()
	
	if (len(modules) != 0):		

		r = 0
		c = 0
		for m in modules:
			m.draw(r,c)	
			#Check if clicked on button
			m.checkModuleButton()
			c+=1
			if c==COLUMNS:
				c = 0
				r += 1
	else:
		pass
	pygame.display.flip()
#PENCILS DOWN, QUIT DRAWING
	clock.tick (10)
pygame.quit()