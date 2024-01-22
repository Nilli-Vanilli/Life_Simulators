import pygame as pg
from classes.style import Colours, Fonts

class Window:
    
    # get colours and fonts
    colours = Colours()
    fonts = Fonts()
    
    
        
    def __init__(self) -> None:
        
        # create a pygame window and store some important stuff
        pg.init()
        self.screen = pg.display.set_mode((0,0), pg.FULLSCREEN | pg.DOUBLEBUF | pg.HWSURFACE)
        self.width, self.height = pg.display.get_surface().get_size()
        self.clock = pg.time.Clock()
        
        # set display caption and key repeat setting
        pg.display.set_caption("Life Simulators")
        pg.key.set_repeat(300,50)
        
    
    
    def draw_bg(self):
        
        # really just a shorthand
        self.screen.fill(self.colours.bg)
        
        
    
    def update(self, fps: int):
        
        # and another shorthand
        pg.display.flip()
        pg.display.update()
        self.clock.tick(fps)