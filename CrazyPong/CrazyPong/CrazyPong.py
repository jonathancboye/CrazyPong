# Author: Jonathan Carpenter
# Email: carpenter.102@wright.edu
# Date: 5/30/2016
# File: CrazyPong.py
# Description: Starts the game

from cocos.director import director
from cocos.scene import Scene
from mylayers import GameLayer

director.init(800, 600)
director.run(Scene(GameLayer()))