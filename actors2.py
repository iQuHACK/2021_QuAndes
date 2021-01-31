#!/usr/bin/python3

import random
import pygame
import numpy as np
import time
import qiskit
from qiskit import *
from pygame.locals import *
from frogger2 import *

from qiskit import Aer
from qiskit_ionq_provider import IonQProvider 
from qiskit.providers.jobstatus import JobStatus


#SOUND
pygame.init()
crash_sound = pygame.mixer.Sound("crash.wav")
def crash():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
	
tin_sound = pygame.mixer.Sound("tin.wav")
def tin():
	pygame.mixer.Sound.play(tin_sound)
	pygame.mixer.music.stop()
duck_sound = pygame.mixer.Sound("duck.wav")
def duck():
	pygame.mixer.Sound.play(duck_sound)
	pygame.mixer.music.stop()


#ACTORS

#general class for the game objects
class Rectangle:

	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def intersects(self, other):
		left = self.x
		top = self.y
		right = self.x + self.w
		bottom = self.y + self.h

		oleft = other.x
		otop = other.y
		oright = other.x + other.w
		obottom = other.y + other.h

		return not (left >= oright or right <= oleft or top >= obottom or bottom <= otop)

#Class for every lane in the game
class Lane(Rectangle):

	def __init__(self, y, c=None, n=0, l=0, spc=0, spd=0):
		super(Lane, self).__init__(0, y * g_vars['grid'], g_vars['width'], g_vars['grid'])
		self.type = t
		self.color = c
		self.obstacles = []
		offset = random.uniform(0, 200)
		if self.type == 'car':
			o_color = (128, 128, 128)
		if self.type == 'log':
			o_color = (185, 122, 87)
        #Juan Pablo power up
		if self.type== 'superpos':
			o_color=(255,255,0)
		if self.type== 'tunnel':
			o_color=(148,0,211)
		for i in range(n):
			self.obstacles.append(Obstacle(offset + spc * i, y * g_vars['grid'], l * g_vars['grid'], g_vars['grid'], spd, o_color, ready=0))

#Class for the frog 
class Frog(Rectangle):

	def __init__(self, x, y, w, c):
		super(Frog, self).__init__(x, y, w, w)
		self.x0 = x
		self.y0 = y
		self.color = c
		self.attached = None
		self.qc = QuantumCircuit(2,2)  
		self.state = '00'
		self.powup = None
#Reset the frog to the initial status and state
	def reset(self):
		print("Reset")
		self.x = self.x0
		self.y = self.y0
		self.attach(None)
		self.qc = QuantumCircuit(2,2)
		self.state = '00'
		self.powup = None 
#Move the frog
	def move(self, xdir, ydir):
		self.x += xdir * g_vars['grid']
		self.y += ydir * g_vars['grid']
        # Daniel saves direction
		self.xdir = xdir
		self.ydir = ydir
        # Daniel sound
		duck()
    #Daniel return
	def devolver(self):
		self.x -= self.xdir * g_vars['grid']
		self.y -= self.ydir * g_vars['grid']
        
    #Daniel tunneling
	def tunnel(self):
		self.x += self.xdir * g_vars['grid']
		self.y += self.ydir * g_vars['grid']
#Attach a frog to some obstacle in the lane
	def attach(self, obstacle):
		self.attached = obstacle
#Movement for the obstacles, discrete movement
	def update(self):
		if self.attached is not None:
			#Modificado para movimiento discreto            
			if abs(self.attached.ready) > 1 and self.attached.speed != 0:
				if self.attached.speed > 0:
					self.x += g_vars['grid']
				else:
					self.x -= g_vars['grid']
				self.ready = 0
            
			#self.x += self.attached.speed

		if self.x + self.w > g_vars['width']:
			self.x = g_vars['width'] - self.w
		
		if self.x < 0:
			self.x = 0
		if self.y + self.h > g_vars['width']:
			self.y = g_vars['width'] - self.w
		if self.y < 0:
			self.y = 0

	def draw(self):
		rect = Rect( [self.x, self.y], [self.w, self.h] )
		pygame.draw.rect( g_vars['window'], self.color, rect )
        
    #Update circuit
	def update_circuit(self, type):
		if type == 'superpos' and self.powup!= 'superpos':
			self.powup = 'superpos'         
			self.qc.h(0)
			tin()
		elif type == 'tunnel' and self.powup!= 'tunnel':
			self.powup = 'tunnel'
			self.qc.h(1)
			tin()
		#self.qc.draw()
            
    #Measure circuit
	def measure_circuit(self, type):
		if type == 'superpos':
			self.qc.measure(0,0)
		elif type == 'tunnel':
			self.qc.measure(1,1)
            
        #Call provider and set token value
		provider = IonQProvider(token='95f4ff6Ka8BX0w4qPpkcZMX9q2PGyLt1')
		#qiskit_ionq_provider
		backend = provider.get_backend("ionq_simulator")
        # Then run the circuit:
		job = backend.run(self.qc, shots=1)
        #save job_id
		job_id_bell = job.job_id()

        # Fetch the result:
		result = job.result()
        
		#qpu_backend = provider.get_backend("ionq_qpu")
        # Then run the circuit:
		#qpu_job_bell = qpu_backend.run(self.qc)
        #Store job id
		#job_id_bell = qpu_job_bell.job_id()
		#if qpu_job_bell.status() is JobStatus.DONE:
		#	print("Job status is DONE")
        # Fetch the result:
		#result = qpu_job_bell.result()
        
		#backend = Aer.get_backend('qasm_simulator')
		#result = execute(self.qc,backend=backend, shots=1).result()
		counts = result.get_counts()
		self.state = max(counts, key=counts.get)
		#else:
		#	print("Job status is ", qpu_job_bell.status() )
		self.qc = QuantumCircuit(2,2)
		self.powup = None
            
#Class for the obstacles of the game
class Obstacle(Rectangle):

	def __init__(self, x, y, w, h, s, c, ready):
		super(Obstacle, self).__init__(x, y, w, h)
		self.color = c
		self.speed = s
		self.ready=0

	def update(self):
        #Hecho por Ana para movimiento discreto
		if abs(self.ready) > 1 and self.speed != 0:
			if self.speed > 0:
				self.x += g_vars['grid']
			else:
				self.x -= g_vars['grid']
			self.ready = 0
		else:
			self.ready += (self.speed)
 
		if self.speed > 0 and self.x > g_vars['width'] + g_vars['grid']:
			self.x = -self.w
		elif self.speed < 0 and self.x < -self.w:
			self.x = g_vars['width']

	def draw(self):
		pygame.draw.rect( g_vars['window'], self.color, Rect( [self.x, self.y], [self.w, self.h] ) )


class Lane(Rectangle):

	def __init__(self, y, t='safety', c=None, n=0, l=0, spc=0, spd=0):
		super(Lane, self).__init__(0, y * g_vars['grid'], g_vars['width'], g_vars['grid'])
		self.type = t
		self.color = c
		self.obstacles = []
		offset = 0#random.uniform(0, 200)
		if self.type == 'car':
			o_color = (128, 128, 128)
		if self.type == 'log':
			o_color = (185, 122, 87)
        #Juan Pablo power up
		if self.type== 'superpos':
			o_color=(255,255,0)
		if self.type== 'tunnel':
			o_color=(148,0,211)
		for i in range(n):
			#Modificado para movimiento discreto
			self.obstacles.append(Obstacle(offset + spc * i, y * g_vars['grid'], l * g_vars['grid'], g_vars['grid'], spd, o_color, ready=0))

	def check(self, frog):
		checked = False
		attached = False
		frog.attach(None)
		for obstacle in self.obstacles:
            
            
#actions for the differenet obsatxcles in the game          
			if frog.intersects(obstacle):
				crash()
                #Se estrella con carro o cae al agua
				if self.type == 'car':
					if frog.powup!=None:
						print("Estrella carro. powup: "+frog.powup)                   #PRINTTT
						if frog.powup=='superpos':
							frog.measure_circuit('superpos')
							print("Estado antes de verificar "+frog.state)
							if frog.state=='11' or frog.state=='01':
                                #Se devuelve a donde estaba antes
								print("Estrella carro. Se devuelve estado: "+frog.state)           #PRINTTT
								frog.devolver()
								frog.qc = QuantumCircuit(2,2)
						elif frog.powup=='tunnel':
							frog.measure_circuit('tunnel')
							if frog.state=='11' or frog.state=='01':
                                #Atraviesa el obstaculo
								print(frog.state)
								frog.tunnel()
								frog.qc = QuantumCircuit(2,2)
					else:
                    #Se muere
						frog.reset()
						checked = True
                            
				if self.type == 'log':
					attached = True
					frog.attach(obstacle)
                    
                #Puertas cuánticas
				if self.type == 'superpos':
					print("Coje la puerta "+self.type)           #PRINTT
					frog.update_circuit('superpos')
					frog.qc.draw()                              #PRINTTT
				if self.type == 'tunnel':
					frog.update_circuit('tunnel')
                    
		if not attached and self.type == 'log':
			if frog.powup!=None:
				if frog.powup=='superpos':
					frog.measure_circuit('superpos')
					if frog.state=='11' or frog.state=='01':
                       #Se devuelve a donde estaba antes
						print(frog.state)
						frog.devolver()
						frog.qc = QuantumCircuit(2,2)
				elif frog.powup=='tunnel':
					frog.measure_circuit('tunnel')
					if frog.state=='11' or frog.state=='10':
                        #Atraviesa el obstaculo
						print(frog.state)
						frog.tunnel()
						frog.qc = QuantumCircuit(2,2)
			else:
               #Se muere
				frog.reset()
				checked = True

		return checked

	def update(self):
		for obstacle in self.obstacles:
			obstacle.update()

	def draw(self):
		if self.color is not None:
			pygame.draw.rect( g_vars['window'], self.color, Rect( [self.x, self.y], [self.w, self.h] ) )
		for obstacle in self.obstacles:
			obstacle.draw()


#SCORE
class Score:

	def __init__(self):
		self.score = 0
		self.high_score = 0
		self.high_lane = 1
		self.lives = 3

	def update(self, points):
		self.score += points
		if self.score > self.high_score:
			self.high_score = self.score

	def reset(self):
		self.score = 0
		self.high_lane = 1
		self.lives = 3
