from classes.style import Colours, Fonts
from classes.window import Window
import pygame as pg

class Title():
    
    # states
    lock_colour = False
    lock_font = False

    # other stuff
    x = None
    y = None
    text_width = None
    text_height = None
    colour = None
    font = None
    
    def __init__(self, text: str, pos: tuple, size: float, colour=None, font=None, underlined=True) -> None:
        
        self.colours = Colours()
        self.fonts = Fonts()
        
        if colour: 
            self.colours.title = colour
            self.lock_colour = True
        
        if font:
            self.fonts.title = font
            self.lock_font = True
            
        self.text = text
        self.size = size
        self.x0, self.y0 = pos
        self.underlined = underlined
        
        
        
    def reset(self):
        
        # reset colour and font
        self.colour = self.colours.title
        self.font = pg.font.SysFont(self.fonts.title, int(self.size))
        
        # reset size and position
        self.text_width, self.text_height = self.font.size(self.text)
        self.x = self.x0 - self.text_width / 2
        self.y = self.y0 - self.text_height / 2
        
        # render text again
        text_img = self.font.render(self.text, True, self.colours.title)
        
        return text_img
        
    
    
    def draw(self, window: Window):
        
        # reset colours and fonts
        if not self.lock_colour:
            self.colours = window.colours
        if not self.lock_font:
            self.fonts = window.fonts
        
        # reset text
        text_img = self.reset()
        
        # draw title
        window.screen.blit(text_img, (self.x, self.y))
        
        # draw line under title
        if self.underlined:
            pg.draw.line(window.screen, self.colours.underline, (self.x, self.y + self.text_height),
                         (self.x + self.text_width, self.y + self.text_height), 3)
        
        