from cocos.director import director
from cocos.scene import Scene
from mylayers import GameLayer

width = 800
height = 800
director.init(800, 800)
director.run(Scene(GameLayer()))