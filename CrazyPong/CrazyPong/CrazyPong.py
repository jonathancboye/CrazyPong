from cocos.director import director
from cocos.scene import Scene
from mylayers import GameLayer

director.init(800, 600)
director.run(Scene(GameLayer()))