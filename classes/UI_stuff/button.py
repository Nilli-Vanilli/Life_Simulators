from classes.style import Colours, Fonts
import pygame as pg

class Button():
    
    # state
    clicked = False
    lock_colour = False
    lock_font = False
    
    # colour and font
    colour = None
    font = None
    
    def __init__(self, rect: tuple, text: str, font=None, hidden=False) -> None:
        
        x, y, width, height = rect
        
        self.x = x - width / 2   # make pos center of button
        self.y = y - height / 2
        self.width = width
        self.height = height
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        
        self.font_size = self.height // 2
        
        self.colours = Colours()
        self.fonts = Fonts()
        
        if font:
            self.fonts.button = font
            self.lock_font = True
        
        self.text = text
            
        self.hidden = hidden
        
    
    
    def reset(self):
        
        # render font and text again
        self.font = pg.font.SysFont(self.fonts.button, int(self.font_size))
        text_img = self.font.render(self.text, True, self.colours.button_text)
        
        # reset text length and width
        self.text_len = text_img.get_width()
        self.text_height = text_img.get_height()
        
        return text_img
    
    
    
    def set_colours(self, body: tuple, hover: tuple, click: tuple, text: tuple):
        
        # set new colours and lock them
        self.colours.button_body = body
        self.colours.button_hover = hover
        self.colours.button_click = click
        self.colours.button_text = text
        self.lock_colour = True
        
        
    
    def check_mouseover(self):
        
        # return value
        action = False
        
        # get mouse position and check if left mousebutton is clicked
        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]

        # check if mouse is hovering over button
        if self.rect.collidepoint(pos):
            
            # if the mouse is clicked, display click colour
            if click:
                self.clicked = True
                self.colour = self.colours.button_click
            
            # after a click, reset and send button output
            elif self.clicked:
                self.clicked = False
                action = True
            
            # if mouse is hovering display hover colour
            else: self.colour = self.colours.button_hover
        
        # if mouse is not hovering display regular colour
        else: self.colour = self.colours.button_body
        
        return action
        
      
      
    def shade_button(self, screen):
        
        pg.draw.line(screen, self.colours.shade_pos, (self.x, self.y), (self.x + self.width, self.y), 2)
        pg.draw.line(screen, self.colours.shade_pos, (self.x, self.y), (self.x, self.y + self.height), 2)
        pg.draw.line(screen, self.colours.shade_neg, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pg.draw.line(screen, self.colours.shade_neg, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)
            
          
    
    def draw(self, window):
        
        # reset colours and fonts if they are not locked
        if not self.lock_colour:
            self.colours = window.colours
        if not self.lock_font:
            self.fonts = window.fonts
        
        # reset text image
        text_img = self.reset()
        
        # check mouseover
        action = self.check_mouseover()
        
        # only draw button when it is not hidden
        if not self.hidden:
            
            # draw button
            pg.draw.rect(window.screen, self.colour, self.rect)

            # add shading to button
            self.shade_button(window.screen)

            # draw text on button
            window.screen.blit(text_img, (self.x + self.width // 2 - self.text_len // 2,
                                          self.y + self.height // 2 - self.text_height // 2))
         
        return action