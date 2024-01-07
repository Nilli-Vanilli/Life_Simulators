import pygame as pg
from random import randint

class Window:
    
    # define colours
    cbg = (225, 225, 225)
    ctitle = (0,0,0)
    
    cshade_pos = (255,255,255)
    cshade_neg = (0,0,0)
    
    cinput_text = (0,0,0)
    cinput_active = (25,190,225)
    cinput_hover = (75,225,255)
    cinput_inactive = (10,10,10)
    cinput_invalid = (255,0,0)
    
    cbutton_text = (255,255,255)
    cbutton_body = (25,190,225)
    cbutton_hover = (75,225,255)
    cbutton_click = (50,150,255)
    

    
    # define fonts
    ftitle = "Impact"
    finput = "freesansbold"
    fbutton = "freesansbold"
    
    
        
    def __init__(self) -> None:
        
        pg.init()
        
        self.screen = pg.display.set_mode((0,0), pg.FULLSCREEN | pg.DOUBLEBUF | pg.HWSURFACE)
        pg.display.set_caption("Life Simulators")
        
        self.width, self.height = pg.display.get_surface().get_size()
        
        self.clock = pg.time.Clock()
        self.fps_cap = 60
        
        pg.key.set_repeat(300,50)
        
        
    
    def update(self, fps=None):
        
        pg.display.flip()
        pg.display.update()
        
        if fps: self.clock.tick(fps)
        else: self.clock.tick(self.fps_cap)