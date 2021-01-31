#!/usr/bin/python3

"""
Frogger game made with Python3 and Pygame
Author: Ricardo Henrique Remes de Lima <https://www.github.com/rhrlima>
Source: https://www.youtube.com/user/shiffman
"""

import random

import pygame
from pygame.locals import *
import numpy as np
from talos import *
from actors2 import *
#pygame.init()
#duck_sound = pygame.mixer.Sound("duck.wav")
#frog_sound = pygame.mixer.Sound("frog.wav")
g_vars = {}
g_vars['width'] = 416
g_vars['height'] = 416
g_vars['fps'] = 30
g_vars['grid'] = 32
g_vars['window'] = pygame.display.set_mode( [g_vars['width'], g_vars['height']], pygame.HWSURFACE)

matrix = np.array([[0,0,0], [0,0,0], [0,0,0]])

class App:
#intizializing the application
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Frogger")
        
        self.running = None
        self.state = None
        self.frog = None
        self.score = None
        self.lanes = None
        self.bot= None
        self.movimiento = None
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Courier New', 16)
        
        
#intizializing the game
    def init(self):
        self.running = True
        self.state = 'START'
        
        #Player's frog 
        self.frog = Frog(g_vars['width']/2 - g_vars['grid']/2, 12 * g_vars['grid'], g_vars['grid'],(34, 177, 76))
        #Bot's frog
        self.frog2 = Frog(g_vars['width']/2 - g_vars['grid']/2 - 3*g_vars['grid'], 12* g_vars['grid'], g_vars['grid'],(255, 0, 0))
        
        self.frog.attach(None)
        self.frog2.attach(None)
        self.score = Score()
        #Score for Frog 2
        self.score2 = Score()

        self.lanes = []
        self.lanes.append( Lane( 1, c=( 50, 192, 122) ) )
        self.lanes.append( Lane( 2, t='log', c=(153, 217, 234), n=2, l=6, spc=350, spd=0.03) )
        self.lanes.append( Lane( 3, t='log', c=(153, 217, 234), n=3, l=2, spc=180, spd=-0.04) )
        self.lanes.append( Lane( 4, t='log', c=(153, 217, 234), n=4, l=2, spc=140, spd=0.05) )
        self.lanes.append( Lane( 5, t='log', c=(153, 217, 234), n=2, l=3, spc=230, spd=-0.02) )
        #Juan Pablo power up and comment
        self.lanes.append( Lane( 6, t='superpos', c=(50, 192, 122), n=1, l=1, spc=100, spd=1.5) )
        #self.lanes.append( Lane( 6, c=(50, 192, 122) ) )
        self.lanes.append( Lane( 7, t='tunnel', c=(50, 192, 122), n=1, l=1, spc=100, spd=-1.5) )
        #self.lanes.append( Lane( 7, c=(50, 192, 122) ) )
        self.lanes.append( Lane( 8, t='car', c=(195, 195, 195), n=3, l=2, spc=180, spd=-0.02) )
        self.lanes.append( Lane( 9, t='car', c=(195, 195, 195), n=2, l=4, spc=240, spd=-0.04) )
        self.lanes.append( Lane( 10, t='car', c=(195, 195, 195), n=4, l=2, spc=130, spd=0.03) )
        self.lanes.append( Lane( 11, t='car', c=(195, 195, 195), n=3, l=3, spc=200, spd=0.05) )
        self.lanes.append( Lane( 12, c=(50, 192, 122) ) )


#Controls for the players frog
    def event(self, event):
        if event.type == QUIT:
            self.running = False

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.running = False

        if self.state == 'START':
            if event.type == KEYDOWN and event.key == K_RETURN:
                self.state = 'PLAYING'

        if self.state == 'PLAYING':
            if event.type == KEYDOWN and event.key == K_LEFT:
                self.frog.move(-1, 0)
            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.frog.move(1, 0)
            if event.type == KEYDOWN and event.key == K_UP:
                self.frog.move(0, -1)
            if event.type == KEYDOWN and event.key == K_DOWN:
                self.frog.move(0, 1)
                
        '''
            #Juan Pablo Frog 2 event
            if event.type == KEYDOWN and event.key == ord('a'):
                self.frog2.move(-1, 0)
            if event.type == KEYDOWN and event.key == ord('d'):
                self.frog2.move(1, 0)
            if event.type == KEYDOWN and event.key == ord('w'):
                self.frog2.move(0, -1)
            if event.type == KEYDOWN and event.key == ord('s'):
                self.frog2.move(0, 1)
        '''
    
#Controls for the bot's frog
    def event2(self, event):
        if self.state == 'PLAYING':
            if event=='left':
                self.frog2.move(-1, 0)
            if event=='right':
                self.frog2.move(1, 0)
            if event=='up':
                self.frog2.move(0, -1)
            if event=='down':
                self.frog2.move(0, 1)     
            if event=='none':
                self.frog2.move(0,0)     
                
                
                
#Updating the state of the game for each movement              
    def update(self):
        for lane in self.lanes:
            lane.update()

        lane_index = self.frog.y // g_vars['grid'] - 1
        if self.lanes[lane_index].check(self.frog):
            self.score.lives -= 1
            self.score.score = 0
            
        #Juan Pablo Frog 2
        lane_index = self.frog2.y // g_vars['grid'] - 1
        if self.lanes[lane_index].check(self.frog2):
            self.score2.score = 0
            
        #Juan Pablo Frog 2
        self.frog.update()
        self.frog2.update()

        if (g_vars['height']-self.frog.y)//g_vars['grid'] > self.score.high_lane:
            if self.score.high_lane == 11:
                self.frog.reset()
                self.score.update(200)
            else:
                self.score.update(10)
                self.score.high_lane = (g_vars['height']-self.frog.y)//g_vars['grid']
                
        #Juan Pablo update Frog 2 and restart player 2
        if (g_vars['height']-self.frog2.y)//g_vars['grid'] > self.score2.high_lane:
            if self.score2.high_lane == 11:
                self.frog2.reset()
                self.score2.update(200)
            else:
                self.score2.update(10)
                self.score2.high_lane = (g_vars['height']-self.frog2.y)//g_vars['grid']



        if self.score.lives == 0:
            self.frog.reset()
            self.score.reset()
            self.state = 'START'

            
#Drawing the interface of the game
    def draw(self):
        g_vars['window'].fill( (0, 0, 0) )
        if self.state == 'START':

            self.draw_text("Frogger!", g_vars['width']/2, g_vars['height']/2 - 15, 'center')
            self.draw_text("Press ENTER to start playing.", g_vars['width']/2, g_vars['height']/2 + 15, 'center')

        if self.state == 'PLAYING':

            self.draw_text("Lives: {0}".format(self.score.lives), 5, 8, 'left')
            self.draw_text("Score: {0}".format(self.score.score), 120, 8, 'left')

            self.draw_text("High Score: {0}".format(self.score.high_score), 240, 40, 'left')
            self.draw_text("Score Talos: {0}".format(self.score2.score), 240, 8, 'left')


            for lane in self.lanes:
                lane.draw()
            self.frog.draw()
            #Juan Pablo Frog 2
            self.frog2.draw()

        pygame.display.flip()

    def draw_text(self, t, x, y, a):
        text = self.font.render(t, False, (255, 255, 255))
        if a == 'center':
            x -= text.get_rect().width / 2
        elif a == 'right':
            x += text.get_rect().width
        g_vars['window'].blit( text , [x, y])

    def cleanup(self):
        pygame.quit()
        quit()
        
#Method that describes the surroundings of the bot and creates a matrix according to it, this matrix will help the bot to choose the best path possible, it is the input to an implemeted qaoa
    def fillmatrix(self):
            #Fill 	
        global matrix
        pos = [-1,0,1]
        
        
        for j in pos:
            for i in pos:
                left = self.frog2.x+i*32
                right = self.frog2.x+self.frog2.w+i*32
                top = self.frog2.y-j*32
                bottom = self.frog2.y +self.frog2.h-j*32
                lane_index = top// g_vars['grid'] - 1
                if  lane_index !=12 and lane_index!=-1 and lane_index !=0 and lane_index !=1:
                    if self.lanes[lane_index].obstacles ==[]:
                        matrix[j+1][i+1]=0
                    else:
                        for obstacle in self.lanes[lane_index].obstacles:
                            oleft=obstacle.x
                            oright=obstacle.x+obstacle.w
                            otop=obstacle.y
                            obottom=obstacle.h+obstacle.y
                            print(lane_index)
                            if not (left >= oright or right <= oleft or top >= obottom or bottom <= otop):
                                if self.lanes[lane_index].type == 'car':
                                    matrix[j+1][i+1] = 1
                                if self.lanes[lane_index].type == 'log':
                                    matrix[j+1][i+1] = 0
                            else:
                                if self.lanes[lane_index].type == 'car':
                                    matrix[j+1][i+1] = 0
                                if self.lanes[lane_index].type == 'log':
                                    matrix[j+1][i+1] = 1
                        
                else:
                    matrix[j+1][i+1] = 0
                        
        var1=matrix[0]
        matrix[0]=matrix[2]
        matrix[2]=var1
        print(np.matrix(matrix))                   
          
#executing the game
    def execute(self):
        if self.init() == False:
            self.running = False
        while self.running:
            for event in pygame.event.get():
                self.event( event )
            self.fillmatrix()
            self.bot=QAOA_BOT(['left','right','none'],matrix)
            self.movimiento=self.bot.movimiento()
            self.event2(self.movimiento)
            self.update()
            self.draw()
            self.clock.tick(g_vars['fps'])
        self.cleanup()


if __name__ == "__main__":
    gameApp = App()
    gameApp.execute()
