import urllib.request
import time
import pygame
import os
import socket
import threading

game_folder = os.path.dirname(__file__)

#colors
WHITE 		= 	(255,255,255)
BLACK 		= 	(0,0,0)
LIGHT_BLUE 	= 	(180,233,255)
GREEN		=	(0,255,0)

#GAME CONSTANTS
TITLE 	= 	"Home Destroyinator 2000"
WIDTH 	= 	1536
HEIGHT 	= 	864

#Lists and constants for modules and IP
modules = []
currentIP = []
port = 80

#Interface Values
moduleList_x = 200
moduleList_y = 200
title_x = 50
title_y = 50
refresh_x = WIDTH-(2*moduleList_x)-50
refresh_y = moduleList_y-50

class Module():
	#Def thyself and at thyself to the list of thys.
	def __init__(self, ip, typ, name):
		self.ip = ip
		self.typ = typ
		self.name = name
		modules.append(self)
		
	def setButton(self, a, b, c, d):
		self.a = a
		self.b = b
		self.c = a+c
		self.d = b+d





class Relais(Module):
	def __init__(self, ip, typ, name):
		#Pre checking of state is not working AT ALL
		self.state = "false"
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
			print ("Error in turining relais: Can't connect to page")
	
	def checkModuleButton(self):
		if checkButton(self.a,self.b,self.c,self.d):
			self.Turn()
			

#uncomment this for testing, creates a fake module
# mod = Relais("192.168.178.1", "relais", "lamp1")

class Plant(Module):
	def __init__(self, ip, typ, name, state):
		self.state = state
		super(Plant,self).__init__(ip,typ,name)

	# def readState(self):
	# 	sta = str(urllib.request.urlopen("http://" + a + "/state").read())[2:-1]
	# 	self.state = sta

	def checkModuleButton(self):
		if checkButton(self.a,self.b,self.c,self.d):
			pass

class Ldr(Module):
	def __init__(self, ip, typ, name, state):
		self.state = state
		super(Ldr,self).__init__(ip,typ,name)

	# def readState(self):
	# 	sta = str(urllib.request.urlopen("http://" + a + "/state").read())[2:-1]
	# 	self.state = sta

	def checkModuleButton(self):
		if checkButton(self.a,self.b,self.c,self.d):
			pass
	
#Pygame font Init
pygame.font.init()
def text_to_screen(screen, text, x, y, size = 20,
            color = (200, 000, 000), font_type = 'Comic Sans MS'):
    text = str(text)
    font = pygame.font.SysFont(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))



def findModule(a, b, timeOut):
	for i in range(a, b):

		addr = "192.168.178." +  str(i)
		iplist = []
		for m in modules:
			iplist.append(m.ip)
		if addr not in iplist: 
			socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			
			currentIP[:] = []
			currentIP.append(addr)
			socket.setdefaulttimeout(timeOut)
			result = socket_obj.connect_ex((addr,port))
			whois = "nobody"
			if result == 0:
				socket.setdefaulttimeout(3)
				print("Connecting to: " + str(addr) + "/who")

				try:
					whois = str(urllib.request.urlopen("http://" + addr + "/who").read())[2:-1]
					if whois == "relais":
						mod = Relais(str(addr),str(whois),str(whois))
					if whois == "plant":
						mod = Plant(str(addr),str(whois),str(whois), 0)
					if whois == "ldr":
						mod = Ldr(str(addr),str(whois),str(whois), 0)
					print(addr + ": " + str(mod) + " " + str(whois))

				except:
					print("Cant read who page of:" + str(addr))
					pass

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
	text_to_screen(window, "Home Destroyinator 2000", title_x, title_y, size = 50)
	text_to_screen(window, str(currentIP[0]), refresh_x-100, refresh_y, size = 10)
	#Refresh Button
	pygame.draw.rect(window,LIGHT_BLUE,(refresh_x,refresh_y,50,50))
	if checkButton(refresh_x,refresh_y,refresh_x + 50,refresh_y + 50):
		modules[:] = []
		refresh()
	pygame.draw.rect(window,LIGHT_BLUE,(refresh_x + 100,refresh_y,50,50))
	if checkButton(refresh_x + 100,refresh_y,refresh_x + 150,refresh_y + 50):
		
		checkState()
		#MODULE LIST
	#Module list RECT
	pygame.draw.rect(window,BLACK,(moduleList_x,moduleList_y,WIDTH-moduleList_x*2,HEIGHT-moduleList_y*2 ))


	if (len(modules) != 0):		
		#a is for article
		a = 1
		text_to_screen(window, "name", moduleList_x +50, moduleList_y +10)
		text_to_screen(window, "type", moduleList_x +200,moduleList_y +10)
		text_to_screen(window, "IP", moduleList_x +300,moduleList_y +10)
		text_to_screen(window, "State", moduleList_x +500,moduleList_y +10)

		for m in modules:
			text_to_screen(window, m.name, moduleList_x +50,moduleList_y +a*50)
			text_to_screen(window, m.typ, moduleList_x +200,moduleList_y +a*50)
			text_to_screen(window, m.ip, moduleList_x +300,moduleList_y +a*50)
			
			if m.typ == "relais":
				text_to_screen(window, m.state, moduleList_x +500,moduleList_y +a*50)
				pygame.draw.rect(window,(180,233,255),(moduleList_x +700,moduleList_y +a*50,30,30))
				m.setButton(moduleList_x +700,moduleList_y +a*50,30,30)
			if m.typ == "plant":
				pygame.draw.rect(window,(180,233,255),(moduleList_x +700,moduleList_y +a*50,30,30))
				text_to_screen(window, m.state, moduleList_x +500,moduleList_y +a*50)
			if m.typ == "ldr":
				pygame.draw.rect(window,(180,233,255),(moduleList_x +700,moduleList_y +a*50,30,30))
				pygame.draw.rect(window,(180,233,255),(moduleList_x +750,moduleList_y +a*50,30,30))
				pygame.draw.rect(window,(180,233,255),(moduleList_x +800,moduleList_y +a*50,30,30))
			a+=1

			#Check if clicked on button
			m.checkModuleButton()
				

	else:
		text_to_screen(window, "nothing found", moduleList_x +50,moduleList_y +50)
	


	pygame.display.flip()
#PENCILS DOWN, QUIT DRAWING
	clock.tick (10)
pygame.quit()






# for a in ipList:
# 	try:
# 		whois = urllib.request.urlopen("http://" + a + "/on").read()
# 		time.sleep(1)
# 		whois = urllib.request.urlopen("http://" + a + "/off").read()
# 		time.sleep(1)
# 		whois = urllib.request.urlopen("http://" + a + "/on").read()
# 		time.sleep(1)
# 		whois = urllib.request.urlopen("http://" + a + "/off").read()
# 		time.sleep(1)
# 		whois = urllib.request.urlopen("http://" + a + "/on").read()
# 		time.sleep(1)
# 		whois = urllib.request.urlopen("http://" + a + "/off").read()
# 		time.sleep(1)
# 	except:
# 		pass


