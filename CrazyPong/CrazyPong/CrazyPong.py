from cocos.director import director
from cocos.scene import Scene
from mylayers import GameLayer
#comment
director.init(800, 600)
director.run(Scene(GameLayer()))