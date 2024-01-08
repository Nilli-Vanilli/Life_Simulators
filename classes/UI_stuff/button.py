from classes.window import Window
import pygame as pg

class Button(Window):
    
    clicked = False
    
    def __init__(self, rect: tuple, text: str, font=None, hidden=False) -> None:
        super().__init__()
        
        x, y, width, height = rect
        
        self.x = x - width / 2
        self.y = y - height / 2
        self.width = width
        self.height = height
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        
        self.colour = self.cbutton_body
        
        self.font_size = self.height // 2
        
        if font: self.font = pg.font.SysFont(font, int(self.font_size))
        else: self.font = pg.font.SysFont(self.fbutton, int(self.font_size))
        
        self.text = self.font.render(text, True, self.cbutton_text)
        
        self.text_len = self.text.get_width()
        self.text_height = self.text.get_height()
            
        self.hidden = hidden
        
    
    
    def colours(self, cbody: tuple, chover: tuple, cclick: tuple, ctext: tuple):
        
        self.cbutton_body = cbody
        self.cbutton_hover = chover
        self.cbutton_click = cclick
        self.cbutton_text = ctext
        
    
    
    def check_mouseover(self):
        
        # return value
        action = False
        
        # get mouse position
        pos = pg.mouse.get_pos()

        # check if mouse is hovering over button
        if self.rect.collidepoint(pos):
            
            # if the mouse is clicked, display click colour
            if pg.mouse.get_pressed()[0]:
                self.clicked = True
                self.colour = self.cbutton_click
            
            # after a click, reset and send button output
            elif not pg.mouse.get_pressed()[0] and self.clicked:
                self.clicked = False
                action = True
                self.colour = self.cbutton_hover
            
            # if mouse is hovering display hover colour
            else: self.colour = self.cbutton_hover
        
        # if mouse is not hovering display regular colour
        else: self.colour = self.cbutton_body
        
        return action
        
      
      
    def shade_button(self):
        
        pg.draw.line(self.screen, self.cshade_pos, (self.x, self.y), (self.x + self.width, self.y), 2)
        pg.draw.line(self.screen, self.cshade_pos, (self.x, self.y), (self.x, self.y + self.height), 2)
        pg.draw.line(self.screen, self.cshade_neg, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pg.draw.line(self.screen, self.cshade_neg, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)
            
          
    
    def draw(self):
        
        # check mouseover
        action = self.check_mouseover()
        
        # if button is not hidden
        if not self.hidden:
            
            # draw button
            pg.draw.rect(self.screen, self.colour, self.rect)

            # add shading to button
            self.shade_button()

            # draw text on button
            self.screen.blit(self.text, (self.x + self.width // 2 - self.text_len // 2, self.y + self.height // 2 - self.text_height // 2))
         
        return action