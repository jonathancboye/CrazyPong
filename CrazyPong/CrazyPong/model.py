import pyglet

class GameModel(pyglet.event.EventDispatcher):

    is_event_handler = True

    def __init__(self):
        super(GameModel, self).__init__()
        self.left_score = 0
        self.right_score = 0
        self.states = {'playing': 0, 'paused' : 1, 'menu': 2, 'game_over':3}
        self.state =  self.states['menu']

    def update_scores(self, paddle):

        if paddle == 'left':
            self.left_score += 1
        elif paddle == 'right':
            self.right_score += 1
        
        if(self.left_score >= 10):
            self.state = self.states['game_over']
            self.dispatch_event('on_game_over', 'Red Player', (255, 0, 0, 255))
            print 'game over'
        elif(self.right_score >= 10):
            self.state = self.states['game_over']
            self.dispatch_event('on_game_over', 'Green Player', (0, 255, 0, 255))
            print 'game over'
       
        self.dispatch_event('on_update_scores')
        
 
    def game_paused(self):
        self.state = self.states['paused']
        self.dispatch_event('on_game_pause')
        print 'game paused'

    # Start a new game
    def game_start(self):
        self.left_score = 9
        self.right_score = 9
        self.state = self.states['playing']
        self.dispatch_event('on_game_start')
        self.dispatch_event('on_update_scores')
        print 'game start'

    def game_resume(self):
        self.state = self.states['playing']
        self.dispatch_event('on_game_resume')
        print 'game resume'

    def game_over(self):
        self.state = self.states['game_over']
        self.dispatch_event('on_game_over')
        print 'game over'

    def menu(self):
        self.state = self.states['menu']
        print 'menu'

GameModel.register_event_type('on_update_scores')
GameModel.register_event_type('on_game_over')
GameModel.register_event_type('on_game_pause')
GameModel.register_event_type('on_game_start')
GameModel.register_event_type('on_game_resume')