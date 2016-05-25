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
    
    def __init__(self, model, input):
        super(PlayLayer, self).__init__()
        self.input = input
        self.model = model
        width = director._window_virtual_width
        height = director._window_virtual_height
        super(PlayLayer, self).on_enter()
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
        self.pause_text = cocos.text.Label("PAUSED", position=(width/2, height/2), bold=True, font_size = 20, \
                                                color=(51, 153, 255, 255), width=40, height=40, anchor_x='center', anchor_y='center')
        self.winning_text = cocos.text.Label("", position=(width/2, height/2), bold=True, font_size = 15,\
                                             color=(0, 0, 0, 0), width=20, height=20, anchor_x='center', anchor_y='center')
        self.gameover_info_text = cocos.text.Label("PRESS SPACE FOR MENU", position=(width/2, 40), bold=True, font_size = 20,\
                                             color=(0, 0, 0, 0), width=40, height=40, anchor_x='center', anchor_y='center')
        self.pause_info_text = cocos.text.Label("PRESS SPACE TO QUIT TO MENU", position=(width/2, 40), bold=True, font_size = 20,\
                                             color=(51, 153, 255, 255), width=40, height=40, anchor_x='center', anchor_y='center')
        cellsize = self.pingpong.width * 1.25
        self.collman = cm.CollisionManagerGrid(0, width, 0, height,
                                               cellsize, cellsize)
        self.lpaddle.position = 0, height/2
        self.rpaddle.position = width, height/2
        self.add(self.rpaddle)
        self.add(self.lpaddle)
        self.add(self.score_text_left)
        self.add(self.score_text_right)
        self.add(self.pingpong)  
        self.model.push_handlers(self)
        self.callupdate = None


    def on_update_scores(self):
        self.score_text_left.element.text = str(self.model.left_score)
        self.score_text_right.element.text = str(self.model.right_score)

    def on_game_start(self):
        width = director._window_virtual_width
        height = director._window_virtual_height
        self.lpaddle.position = 0, height/2      
        self.rpaddle.position = width, height/2
        self.pingpong.init()
        self.lpaddle.do(RotateBy(360, 2))
        self.rpaddle.do(RotateBy(360, 2))
        self.pingpong.do(RotateBy(360, 2))
        self.callupdate = self.do(Delay(2) + Repeat(CallFunc(self.update)))     
        self.resume() 
    
    def on_game_pause(self):
        ''' Handles on_game_pause events.
            Displays paused text and pauses
            the game. '''
        
        self.add(self.pause_text, z=2)
        self.add(self.pause_info_text, z=2)
        self.pause()

    def on_game_resume(self):
        ''' Handles on_game_resume events.
            Removes paused text from screen
            and resumes the game. ''' 
            
        self.remove(self.pause_text)
        self.remove(self.pause_info_text)
        self.resume()

    def on_game_over(self, winner, winner_color):
        ''' Handles on_game_over events.
            Displays who won and pauses the game. '''

        self.winning_text.element.color = winner_color
        self.gameover_info_text.element.color = winner_color  
        self.winning_text.element.text = "%s Wins!!!!" % winner        
        self.add(self.winning_text, z=2)
        self.add(self.gameover_info_text, z=2)
        self.pause()

    def on_exit(self):
        super(PlayLayer, self).on_exit()
        self.remove_action(self.callupdate)
        try:
            self.remove(self.winning_text)
            self.remove(self.gameover_info_text)
        except Exception:
            pass

        try:
            self.remove(self.pause_text)
            self.remove(self.pause_info_text)
        except Exception:
            pass
   
    
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
        self.input = defaultdict(int) 
        self.model = GameModel()
        self.menu = MenuLayer()
        self.play = PlayLayer(self.model, self.input)
        super(GameLayer, self).__init__(self.menu, self.play)
                
    def on_key_press(self, k, m):
        self.input[k] = 1
       
        # Player vs. Player
        if self.input[key._1]:
            if(self.model.state == self.model.states['menu']):
                self.model.game_start()
                self.switch_to(1)
       
        # Player vs. Computer
        if self.input[key._2]:
             if(self.model.state == self.model.states['menu']):
               # TODO: implement AI for computer
                pass
       
        # Pause game
        if self.input[key.P]:
            if(self.model.state == self.model.states['playing']):
                self.model.game_paused()
            elif(self.model.state == self.model.states['paused']):
                self.model.game_resume()

        if self.input[key.Q]:
            if(self.model.state == self.model.states['paused']):
                self.model.menu()

        if self.input[key.SPACE]:
            if(self.model.state == self.model.states['game_over'] or \
               self.model.state == self.model.states['paused']):
                self.model.menu()
                self.switch_to(0)

    def on_key_release(self, k, m):
        self.input[k] = 0   

