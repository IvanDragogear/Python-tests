import kivy 
from kivy.app import App
from kivy.uix.widget import Widget

import kivent_core
import kivent_cymunk
from kivent_core.managers.resource_managers import texture_manager

from os.path import dirname, join, abspath

texture_manager.load_atlas(join(dirname(
    dirname(abspath(__file__))), 'images',
    'sprite_sheet_001.atlas'))

SHADER_POS = join(dirname(dirname(abspath(__file__))),
    'kivent_stuff', 'glsl','positionshader.glsl')

SHADER_POSROT = join(dirname(dirname(abspath(__file__))),
    'kivent_stuff', 'glsl','positionrotateshader.glsl')
    
def get_physics_dictionary(position, radius, mass):
    circle = {
        'inner_radius': 0,
        'outer_radius': radius,
        'mass': mass,
        'offset': (0,0)}
    col_shape = {
        'shape_type': 'circle',
        'elasticity': 1.0,
        'collision_type': 1,
        'shape_info': circle,
        'friction': 1.0}
    character_physics = {
        'main_shape': 'circle',
        'velocity': (0,0),
        'vel_limit': 100,
        'position': position,
        'angle': 0,
        'angular_velocity': 0,
        'ang_vel_limit': 0,
        'mass': mass,
        'col_shapes':[col_shape]}
    return character_physics
    
def get_component_dictionary(physics, layer, texture, size):
    component = {
        'position': physics['position'],
        'rotate': 0,
        'physics': physics,
        layer: {'texture': texture,'size': size}
        }
    order = ['position', 'rotate','physics',layer]
    return (component,order)

class TestGame(Widget):
    def __init__(self, **kwargs):
        super(TestGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(
            ['camera','layer01','rotate','position',
            'physics'],callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.set_state()
        self.draw_some_stuff()
    
    def draw_some_stuff(self):
        p = get_physics_dictionary((50,05),15,70)
        comp, order = get_component_dictionary(p,
        'layer01','pj_red',(40,80))
        self.gameworld.init_entity(comp,order)
        
        
    def setup_states(self):
        self.gameworld.add_state(
            state_name='main',
            systems_added=[],
            systems_removed=[], 
            systems_paused=[],
            systems_unpaused=['camera','physics'],
            screenmanager_screen='main')
            
    def set_state(self):
        self.gameworld.state = 'main'
        

        
class MainApp(App):
    title = 'Test 001: Kivent dynamic layers'
    def build(self):
        return TestGame()
        
if __name__ == '__main__':
    MainApp().run() 
