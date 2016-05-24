import pyglet

class GameModel(pyglet.event.EventDispatcher):

    is_event_handler = True

    def __init__(self):
        super(GameModel, self).__init__()
        self.left_score = 0
        self.right_score = 0
        self.current_scene = 0

    def lpaddle_scores(self):
        self.left_score += 1
        self.dispatch_event('on_lpaddle_score')
        if(self.left_score >= 10):
            self.dispatch_event('on_game_over', 'Red Player', (255, 0, 0, 255))

    def rpaddle_scores(self):
        self.right_score += 1
        self.dispatch_event('on_rpaddle_score')
        if(self.right_score >= 10):
            self.dispatch_event('on_game_over', 'Green Player', (0, 255, 0, 255))

    def game_over(self):
        self.dispatch_event('on_game_over')

GameModel.register_event_type('on_lpaddle_score')
GameModel.register_event_type('on_rpaddle_score')
GameModel.register_event_type('on_game_over')