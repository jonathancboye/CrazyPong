from cocos.director import director
from cocos.scene import Scene
from mylayers import GameLayer

director.init(800, 800)
director.run(Scene(GameLayer()))