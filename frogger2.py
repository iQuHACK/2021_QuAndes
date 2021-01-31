#!/usr/bin/python3

"""
Frogger game made with Python3 and Pygame
Author: Ricardo Henrique Remes de Lima <https://www.github.com/rhrlima>
Source: https://www.youtube.com/user/shiffman
"""

import random

import pygame
from pygame.locals import *

from actors2 import *


g_vars = {}
g_vars['width'] = 416
g_vars['height'] = 416
g_vars['fps'] = 5
g_vars['grid'] = 32
g_vars['window'] = pygame.display.set_mode( [g_vars['width'], g_vars['height']], pygame.HWSURFACE)

matrix = [[0,0,0], [0,0,0], [0,0,0]]

class App:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Frogger")
        
        self.running = None
        self.state = None
        self.frog = None
        self.score = None
        self.lanes = None

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Courier New', 16)

    def init(self):
        self.running = True
        self.state = 'START'
        
        self.frog = Frog(g_vars['width']/2 - g_vars['grid']/2, 12 * g_vars['grid'], g_vars['grid'])
        self.frog.attach(None)
        self.score = Score()

        self.lanes = []
        self.lanes.append( Lane( 1, c=( 50, 192, 122) ) )
        self.lanes.append( Lane( 2, t='log', c=(153, 217, 234), n=2, l=6, spc=350, spd=0.03) )
        self.lanes.append( Lane( 3, t='log', c=(153, 217, 234), n=3, l=2, spc=180, spd=-0.04) )
        self.lanes.append( Lane( 4, t='log', c=(153, 217, 234), n=4, l=2, spc=140, spd=0.05) )
        self.lanes.append( Lane( 5, t='log', c=(153, 217, 234), n=2, l=3, spc=230, spd=-0.02) )
        self.lanes.append( Lane( 6, c=(50, 192, 122) ) )
        self.lanes.append( Lane( 7, c=(50, 192, 122) ) )
        self.lanes.append( Lane( 8, t='car', c=(195, 195, 195), n=3, l=2, spc=180, spd=-0.02) )
        self.lanes.append( Lane( 9, t='car', c=(195, 195, 195), n=2, l=4, spc=240, spd=-0.04) )
        self.lanes.append( Lane( 10, t='car', c=(195, 195, 195), n=4, l=2, spc=130, spd=0.03) )
        self.lanes.append( Lane( 11, t='car', c=(195, 195, 195), n=3, l=3, spc=200, spd=0.05) )
        self.lanes.append( Lane( 12, c=(50, 192, 122) ) )

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
    
    def update(self):
        for lane in self.lanes:
            lane.update()
        
        lane_index = self.frog.y // g_vars['grid'] - 1
       
        if self.lanes[lane_index].check(self.frog):
            self.score.lives -= 1
            self.score.score = 0
        #Fill matrix	
        pos = [-1,0,1]
        
        matrix=[[0,0,0], [0,0,0], [0,0,0]]
        
        for j in pos:
            for i in pos:
                left = self.frog.x+i*32+j*32
                right = self.frog.x+self.frog.w+i*32+j*32
                top = self.frog.y+j*32+i*32
                bottom = self.frog.y +self.frog.h+j*32+i*32
                print(left,right,top,bottom)
                print(self.frog.x,self.frog.y)
                lane_index = (top// g_vars['grid'] - 1 ) %12
                
                for obstacle in self.lanes[lane_index].obstacles:
                    oleft=obstacle.x
                    oright=obstacle.x+obstacle.w
                    otop=obstacle.y
                    obottom=obstacle.h+obstacle.y
                    #if (left >= oright or right <= oleft or top <= obottom or bottom >= otop):
                    if (left <= oright) : 
                        matrix[j+1][i+1] = 1
                    else:
                        matrix[j+1][i+1]=0
        print(matrix)
            
        
        self.frog.update()



        if (g_vars['height']-self.frog.y)//g_vars['grid'] > self.score.high_lane:
            if self.score.high_lane == 11:
                self.frog.reset()
                self.score.update(200)
            else:
                self.score.update(10)
                self.score.high_lane = (g_vars['height']-self.frog.y)//g_vars['grid']

        if self.score.lives == 0:
            self.frog.reset()
            self.score.reset()
            self.state = 'START'

    def draw(self):
        g_vars['window'].fill( (0, 0, 0) )
        if self.state == 'START':

            self.draw_text("Frogger!", g_vars['width']/2, g_vars['height']/2 - 15, 'center')
            self.draw_text("Press ENTER to start playing.", g_vars['width']/2, g_vars['height']/2 + 15, 'center')

        if self.state == 'PLAYING':

            self.draw_text("Lives: {0}".format(self.score.lives), 5, 8, 'left')
            self.draw_text("Score: {0}".format(self.score.score), 120, 8, 'left')
            self.draw_text("High Score: {0}".format(self.score.high_score), 240, 8, 'left')

            for lane in self.lanes:
                lane.draw()
            self.frog.draw()

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

    def execute(self):
        if self.init() == False:
            self.running = False
        while self.running:
            for event in pygame.event.get():
                self.event( event )
            self.update()
            self.draw()
            self.clock.tick(g_vars['fps'])
        self.cleanup()


if __name__ == "__main__":
    gameApp = App()
    gameApp.execute()