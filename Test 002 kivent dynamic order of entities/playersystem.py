from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivent_core.systems.gamesystem import GameSystem

class PlayerSystem(GameSystem):
    player = ObjectProperty(None)
    game = ObjectProperty(None)
    
    def update(self,dt):
        if self.player is not None:
            self.move_player()
    
    def move_player(self):
        k = self.game.keys
        b = self.player.physics.body
        if 273 in k and 275 in k:
            b.velocity = [140,140]
        elif 273 in k and 276 in k:
            b.velocity = [-140,140]
        elif 274 in k and 275 in k:
            b.velocity = [140,-140]
        elif 274 in k and 276 in k:
            b.velocity = [-140,-140]
        elif 273 in k:   # up
            b.velocity = [0,200]
        elif 274 in k: # down
            b.velocity = [0,-200]
        elif 275 in k: # right
            b.velocity = [200,0]
        elif 276 in k: # left
            b.velocity = [-200,0]
        else:
            b.velocity = [0,0]

Factory.register('PlayerSystem',cls=PlayerSystem)
