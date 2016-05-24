import cocos
from cocos.actions import *
from cocos.director import director
import cocos.collision_model as cm
import cocos.euclid as eu
from pyglet.window import key
from collections import defaultdict
import random

class PingPong(cocos.sprite.Sprite):

    def __init__(self, x, y):
        super(PingPong, self).__init__('KA_Ball.png', scale=.2)
        self.position = x, y
        center = eu.Vector2(x,y)
        self.cshape = cm.CircleShape(center, self.width/2)
        self.window_height = director._window_virtual_height
        self.window_width = director._window_virtual_width
        self.init()

        
        
        self.do(Repeat(CallFunc(self.update)))
    
    def init(self):
        self.velocity_x = 5
        self.accleration_x = 0
        self.velocity_y = 0
        self.accleration_y = 0
        self.maxspeed = 10
        self.position = self.window_width/2, self.window_height/2
        self.cshape.center = eu.Vector2(self.window_width/2, self.window_height/2)
          
        if(random.randint(0,1)):
            self.direction_x = 1
        else:
            self.direction_x = -1

        self.direction_y = 0
        self.do(RotateBy(360, 2))   

    def update(self):
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
            right_diff = self.window_width - self.position[0] + self.width/2
            if right_diff > 0:
                # ball is still in play
                dx = self.velocity_x * self.direction_x
            else:
               # ball has left the board
               # Left side scores a point
               self.init()
        else:
            # check if ball has exited left side of the board
            left_diff = self.position[0] - self.width/2
            if left_diff > 0:
                # ball is still in play
                dx = self.velocity_x * self.direction_x
            else:
                # ball has left the board
                # right side scores a point
                self.init()

        if self.direction_y > 0:
            # check if ball has exited top of the board
            top_diff = self.window_height - self.position[1] + self.height/2
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
            #left paddle
            self.direction_x = 1
            self.do(RotateBy(360, 1))
        else:
            #right paddle
            self.direction_x = -1
            self.do(Reverse(RotateBy(360, 1)))
        if(paddle.velocity != 0):
            self.velocity_x = paddle.velocity
        
        self.velocity_y = paddle.velocity/2
        self.direction_y = paddle.direction
    

class Paddle(cocos.sprite.Sprite):
    
    def __init__(self, x, y, r, g, b):
        super(Paddle, self).__init__('rectangle.png', color=(r, g, b), scale=.2)
        self.window_height = director._window_virtual_height
        self.position = x, y
        center = eu.Vector2(x, y)
        self.cshape = cm.AARectShape(center, self.width/2, self.height/2)
        self.velocity = 0
        self.accleration = 0
        self.direction = 0
        self.maxspeed = 100   
       
    def move(self, dy):
     
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
                top_diff = self.window_height - (self.position[1] + self.height/2)                        
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
                    


class PlayLayer(cocos.layer.Layer):

    is_event_handler = True
    
    
    def __init__(self):
        global width, height

        super(PlayLayer, self).__init__()


        
        self.pingpong = PingPong(width/2, height/2)
        self.lpaddle = Paddle(0, height/2,
                              255, 0, 0)
        self.rpaddle = Paddle(width,
                              height/2,
                              0, 255, 255)
        cellsize = self.pingpong.width * 1.25
        self.collman = cm.CollisionManagerGrid(0, width, 0, height,
                                               cellsize, cellsize)
        self.input = defaultdict(int)
        
        self.add(self.pingpong)
        self.add(self.rpaddle)
        self.add(self.lpaddle)

        self.do(Repeat(CallFunc(self.update)))

    def on_enter(self):
        super(PlayLayer, self).on_enter()
        global width, height
        self.lpaddle.position = 0, height/2
        self.rpaddle.position = width, height/2
        self.pingpong.init()
        self.lpaddle.do(RotateBy(360, 2))
        self.rpaddle.do(RotateBy(360, 2))

    def on_key_press(self, k, m):
        self.input[k] = 1
        
    def on_key_release(self, k, m):
        self.input[k] = 0    


    def update(self):
        self.collman.clear()
        
        for node in self.get_children():
            if (hasattr(node, 'cshape')):
                self.collman.add(node)
        
        for obj in self.collman.iter_colliding(self.pingpong):
            self.pingpong.do(CallFunc(self.pingpong.collided, obj))
         

        lpaddle_dy = self.input[key.W] - self.input[key.S]
        rpaddle_dy = self.input[key.UP] - self.input[key.DOWN]
        
        self.lpaddle.do(CallFunc(self.lpaddle.move, lpaddle_dy))
        self.rpaddle.do(CallFunc(self.rpaddle.move, rpaddle_dy))

class MenuLayer(cocos.layer.Layer):
    
    is_event_handler = True

    def __init__(self):
        super(MenuLayer, self).__init__()
        self.wwidth = director._window_virtual_width
        self.wheight = director._window_virtual_height
        title = cocos.text.Label("WELCOME TO CRAZYPONG", \
                                 position=(self.wwidth/3, self.wheight - self.wheight/2))
        option1 = cocos.text.Label("  1) Player vs. Computer", \
                                 position=(self.wwidth/3, self.wheight - self.wheight/2 - 30))
        option2 = cocos.text.Label("  2) Player vs. Player", \
                                 position=(self.wwidth/3, self.wheight - self.wheight/2 - 50))
        select = cocos.text.Label("  Press 1 or 2 to PLAY", \
                                  position=(self.wwidth/3, self.wheight - self.wheight/2 - 80))
        self.input = defaultdict(int)                
        
        self.add(title)
        self.add(option1)
        self.add(option2)
        self.add(select)

  
class GameLayer(cocos.layer.MultiplexLayer):

    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__(MenuLayer(), PlayLayer())

    def on_key_press(self, k, m):
        # Player vs. Computer
        if k == key._1:
            self.switch_to(1)
        # Player vs. Player
        if k == key._2:
            self.switch_to(1)
        # Pause to menu
        if k == key.P:
            self.switch_to(0)



if __name__ == '__main__':
    width = 800
    height = 800
    director.init(800, 800)
    director.run(cocos.scene.Scene(GameLayer()))