from classes.window import Window
import pygame as pg

class Title(Window):
    
    def __init__(self, text: str, pos: tuple, size: float, font=None, colour=None, underlined=True) -> None:
        super().__init__()
        
        if font: font = pg.font.SysFont(font, int(size))
        else: font = pg.font.SysFont(self.ftitle, int(size))
        
        if colour: colour = colour
        else: colour = self.ctitle
            
        self.text = font.render(text, True, colour)
        
        self.size = font.size(text)
        
        self.x = pos[0] - self.size[0] / 2
        self.y = pos[1] - self.size[1] / 2
        
        self.underlined = underlined
    
    def draw(self):
        
        self.screen.blit(self.text, (self.x, self.y))
        
        if self.underlined:
            pg.draw.line(self.screen, self.cshade_neg, (self.x, self.y + self.size[1]),
                         (self.x + self.size[0], self.y + self.size[1]), 3)
        
        