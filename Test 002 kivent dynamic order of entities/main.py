import kivy 
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window
import kivent_core
import kivent_cymunk
from kivent_core.systems.renderers import RotateRenderer
from kivent_core.managers.resource_managers import texture_manager
from os.path import dirname, join, abspath
from operator import itemgetter

from playersystem import PlayerSystem

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
        'elasticity': 0.0,
        'collision_type': 1,
        'shape_info': circle,
        'friction': 0.0}
    character_physics = {
        'main_shape': 'circle',
        'velocity': (70,70),
        'vel_limit': 200,
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
    keys = []
    layers = []
    
    def __init__(self, **kwargs):
        super(TestGame, self).__init__(**kwargs)
        # Add 100 layers to gameworld
        for i in range(10):
            s = 'layer_%s' % (i)
            sys = RotateRenderer()
            sys.system_id = s
            sys.gameworld = self.gameworld
            sys.zones = ['general']
            sys.system_names = [s,'position','rotate']
            sys.frame_count = 1
            sys.size_of_batches = 4
            sys.size_of_component_block = 1
            sys.shader_source = SHADER_POSROT
            sys.gameview = 'camera'
            self.gameworld.add_system(sys)
        # Init gameworld 
        self.gameworld.init_gameworld(
            ['camera','rotate','position','physics'],
            callback=self.init_game)
        # Bind keyboard events 
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

    def init_game(self):
        self.setup_states()
        self.set_state()
        self.draw_some_stuff()
    
    def draw_some_stuff(self):
        sp = self.gameworld.system_manager['playersys']
        # Draw player in layer_0
        p = get_physics_dictionary((50,50),15,70)
        comp, order = get_component_dictionary(p,
        'layer_0','pj_blue',(40,80))
        id_ent = self.gameworld.init_entity(comp,order)
        sp.player = self.gameworld.entities[id_ent]
        self.layers.append([sp.player,'layer_0'])
        # Draw 9 pillars, each in its layer
        for i in range(9):
            layer = 'layer_%s' % (i+1)
            px = 100+(i*100)
            py = 100+(i*100)
            p = get_physics_dictionary((px,py),15,0)
            comp, order = get_component_dictionary(p,
            layer,'pillar',(40,80))
            id_ent = self.gameworld.init_entity(comp,order)
            ent = self.gameworld.entities[id_ent]
            self.layers.append([ent,layer])
        self.order_layers()
        Clock.schedule_once(self.order_layers)
        
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
        
    def on_key_down(self,window,key,*args):
        if not key in self.keys:
            self.keys.append(key)
        
    def on_key_up(self,window,key,*args):
        if key in self.keys:
            self.keys.remove(key)
            
    def order_layers(self,*args):
        camera = self.gameworld.system_manager['camera']
        a1 = []
        a2 = []
        for layer in self.layers:
            a1.append([layer[0].position.y,layer[1]])
        a1 = sorted(a1, key=itemgetter(0))
        for layer in a1:
            a2.append(layer[1])
        camera.render_system_order = reversed(a2)
        Clock.schedule_once(self.order_layers,0.05)
        
class MainApp(App):
    title = 'Test 001: Kivent dynamic layers'
    def build(self):
        return TestGame()
        
if __name__ == '__main__':
    MainApp().run() 
