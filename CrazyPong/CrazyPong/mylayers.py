import cocos
import pyglet
from cocos.actions import *
from cocos.director import director
from pyglet.window import key
from collections import defaultdict
import cocos.collision_model as cm
from mysprites import PingPong, Paddle
from model import GameModel


class PlayLayer(cocos.layer.Layer):

    is_event_handler = True
    
    def __init__(self, model):
        width = director._window_virtual_width
        height = director._window_virtual_height
        super(PlayLayer, self).__init__()
        self.model = model
        self.pingpong = PingPong(width/2, height/2, self.model)
        self.lpaddle = Paddle(0, height/2,
                              255, 0, 0)
        self.rpaddle = Paddle(width,
                              height/2,
                              0, 255, 255)
        self.score_text_left = cocos.text.Label("0", position=(20, height - 20), bold=True, font_size = 15, \
                                                color=(255, 0, 0, 255), width=20, height=20, anchor_x='center', anchor_y='center')
        self.score_text_right = cocos.text.Label("0", position=(width - 20, height - 20), bold=True, font_size = 15, \
                                                color=(0, 255, 0, 255), width=20, height=20, anchor_x='center', anchor_y='center')

        cellsize = self.pingpong.width * 1.25
        self.collman = cm.CollisionManagerGrid(0, width, 0, height,
                                               cellsize, cellsize)
        self.input = defaultdict(int)     
        self.lpaddle.position = 0, height/2
        self.rpaddle.position = width, height/2
        self.pingpong.init()
        self.add(self.pingpong)
        self.add(self.rpaddle)
        self.add(self.lpaddle)
        self.add(self.score_text_left)
        self.add(self.score_text_right)
        self.do(Repeat(CallFunc(self.update)))
        self.lpaddle.do(RotateBy(360, 2))
        self.rpaddle.do(RotateBy(360, 2))   
        self.model.push_handlers(self)
        
    def on_key_press(self, k, m):
        self.input[k] = 1
        
    def on_key_release(self, k, m):
        self.input[k] = 0    

    def on_lpaddle_score(self):
        self.score_text_left.element.text = str(self.model.left_score)

    def on_rpaddle_score(self):
        self.score_text_right.element.text = str(self.model.right_score)

    def on_game_over(self, winner, winner_color):
        w = director._window_virtual_width
        h = director._window_virtual_height
        winning_text = cocos.text.Label("%s Wins!!!!!" % winner, position=(w/2, h/2), bold=True, font_size = 15,\
                                        color=winner_color, width=20, height=20, anchor_x='center', anchor_y='center')        
        self.add(winning_text)
        self.stop()
        
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
        self.pingpong.do(CallFunc(self.pingpong.move))

class MenuLayer(cocos.layer.Layer):
    
    is_event_handler = True

    def __init__(self):
        super(MenuLayer, self).__init__()
        self.wwidth = director._window_virtual_width
        self.wheight = director._window_virtual_height
        title = cocos.text.Label("WELCOME TO CRAZYPONG", \
                                 position=(self.wwidth/3, self.wheight - self.wheight/2))
        option1 = cocos.text.Label("  1) Player vs. Player", \
                                 position=(self.wwidth/3, self.wheight - self.wheight/2 - 30))
        option2 = cocos.text.Label("  2) Player vs. Computer", \
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
        self.gamemodel = GameModel()
        super(GameLayer, self).__init__(MenuLayer(), PlayLayer(self.gamemodel))

    def on_key_press(self, k, m):
        # Player vs. Player
        if k == key._1:
            self.gamemodel.current_scene = 1
            self.switch_to(1)
        # Player vs. Computer
        if k == key._2:
            pass
        # Pause to menu
        if k == key.P:
            self.gamemodel.current_scene = 2
            self.switch_to(0)

