import pygame as pg
from classes.style import Colours, Fonts

class Window:
    
    # get colours
    colours = Colours()
    fonts = Fonts()
    
    
        
    def __init__(self) -> None:
        
        pg.init()
        
        self.screen = pg.display.set_mode((0,0), pg.FULLSCREEN | pg.DOUBLEBUF | pg.HWSURFACE)
        pg.display.set_caption("Life Simulators")
        
        self.width, self.height = pg.display.get_surface().get_size()
        
        self.clock = pg.time.Clock()
        
        pg.key.set_repeat(300,50)
        
    
    
    def draw_bg(self):
        
        self.screen.fill(self.colours.bg)
        
        
    
    def update(self, fps: int):
        
        pg.display.flip()
        pg.display.update()
        self.clock.tick(fps)