# Author: Jonathan Carpenter
# Email: carpenter.102@wright.edu
# Date: 5/30/2016
# File: mysprites.py
# Description: Contains the pingpong sprite and paddle sprites

import cocos
import cocos.collision_model as cm
import cocos.euclid as eu
import random
from cocos.director import director
from cocos.actions import *

class PingPong(cocos.sprite.Sprite):

    def __init__(self, x, y, model):
        super(PingPong, self).__init__('SoccerBall.png', scale=.4)
        self.model = model
        self.postion = x, y
        center = eu.Vector2(x, y)
        self.cshape = cm.CircleShape(center, self.width/2)
        self.init()

    def init(self):
        width = director._window_virtual_width
        height = director._window_virtual_height
        self.position = width/2, height/2
        self.velocity_x = 5
        self.accleration_x = 0
        self.velocity_y = 0
        self.accleration_y = 0
        self.maxspeed = 10
          
        if(random.randint(0,1)):
            self.direction_x = 1
        else:
            self.direction_x = -1

        self.direction_y = 0  

    def move(self):
        width = director._window_virtual_width
        height = director._window_virtual_height
        dx = 0
        dy = 0

        self.velocity_x += self.accleration_x
        self.velocity_y += self.accleration_y
        
        if self.velocity_x > self.maxspeed:
            self.velocity_x = self.maxspeed
        
        if self.velocity_y > self.maxspeed:
            self.velocity_y = self.maxspeed

        if self.direction_x > 0:
            # check if ball has exited right side of the board
            right_diff = width - self.position[0] + self.width/2
            if right_diff > 0:
                # ball is still in play
                dx = self.velocity_x * self.direction_x
            else:
               # ball has left the board
               # Left side scores a point
               self.model.update_scores('left')
               self.init()
        else:
            # check if ball has exited left side of the board
            left_diff = self.position[0] + self.width/2
            if left_diff > 0:
                # ball is still in play
                dx = self.velocity_x * self.direction_x
            else:
                # ball has left the board
                # right side scores a point
                self.model.update_scores('right')
                self.init()

        if self.direction_y > 0:
            # check if ball has exited top of the board
            top_diff = height - self.position[1] - self.height/2
            if top_diff <= 0:
                # ball hit top
                self.direction_y *= -1
            dy = self.velocity_y * self.direction_y
        elif self.direction_y < 0:
            # check if ball has exited bottom of the board
            bottom_diff = self.position[1] - self.height/2
            if bottom_diff <= 0:
                # ball hit bottom
                self.direction_y *= -1      
            dy = self.velocity_y * self.direction_y

        self.do(MoveBy((dx, dy), 0))
        self.cshape.center = eu.Vector2(self.x, self.y)
        
    def collided(self, paddle):
        if paddle.position[0] == 0:
            # left paddle   
            self.direction_x = 1
            self.do(RotateBy(360, 1))
        else:
            # right paddle
            self.direction_x = -1
            self.do(Reverse(RotateBy(360, 1)))
        
        if(paddle.velocity != 0):
            ''' Paddle is moving give ball
                same speed in x direction as paddle '''
            self.velocity_x = paddle.velocity
        
        #ping pong moves in y direction with half speed of paddle
        self.velocity_y = paddle.velocity/2
        self.direction_y = paddle.direction

class Paddle(cocos.sprite.Sprite):
 
    def __init__(self, x, y, r, g, b):

        super(Paddle, self).__init__('rectangle.png', color=(r, g, b), scale=.2)
        self.position = x, y
        center = eu.Vector2(x, y)
        self.cshape = cm.AARectShape(center, self.width/2, self.height/2)
        self.velocity = 0
        self.accleration = 0
        self.direction = 0
        self.maxspeed = 100   
       
    def move(self, dy):
        width = director._window_virtual_width
        height = director._window_virtual_height
        if dy == 0:
            self.velocity = 0
            self.accleration = 1
            self.direction = 0
        else:
            self.accleration += .01
            self.velocity += self.accleration
            if(self.velocity > self.maxspeed):
                self.velocity = self.maxspeed

            #check if paddle is hitting the upperbound or lowerbound of table
            if dy > 0:
                self.direction = 1
                top_diff = height - (self.position[1] + self.height/2)                        
                if  top_diff > 0:              
                    self.do(MoveBy((0, self.velocity * dy), 0))
                else:
                    self.do(MoveBy((0, top_diff), 0))           
            else:
                self.direction = -1
                bottom_diff = self.position[1] - self.height/2
                if bottom_diff > 0:
                    self.do(MoveBy((0, self.velocity * dy), 0))
                else:
                    self.do(MoveBy((0, bottom_diff * -1), 0)) 
        self.cshape.center = eu.Vector2(self.x, self.y)
 
class ComputerPaddle(Paddle):

    def __init__(self, x, y, r, g, b):
        super(ComputerPaddle, self).__init__(x, y, r, g, b)

    def move(self, pingpong):
        width = director._window_virtual_width
        height = director._window_virtual_height
        dy = pingpong.position[1] - self.position[1]
        self.maxspeed = 10
     
        if abs(dy) > self.width/2:
            self.accleration += .01
            self.velocity += self.accleration
            
            if(self.velocity > self.maxspeed):
                self.velocity = self.maxspeed

            if dy > 0:
                dy = 1
            else:
                dy = -1
        else:
            dy = 0
            self.velocity = 0
            self.accleration = 1
            self.direction = 0
        
        self.do(MoveBy((0, self.velocity * dy), 0))
        self.cshape.center = eu.Vector2(self.x, self.y)
    