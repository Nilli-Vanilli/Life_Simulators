from classes.window import Window
import pygame as pg
from math import floor

class Input_Box(Window):
    
    # states
    active = False
    valid = False
    lock = False
    
    # text size
    text_len = 0
    text_height = 0
    

    
    def __init__(self, name: str, rect: tuple, text: str, error_message: str, font=None) -> None:
        super().__init__()
        
        x, y, width, height = rect
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.text = text
        
        self.cursorindex = 0
        
        if font: self.font = pg.font.SysFont(font, int(self.height))
        else: self.font = pg.font.SysFont(self.finput, int(self.height))
        
        self.name = self.font.render(name, True, self.cinput_text)
        self.error = self.font.render(error_message, True, self.cinput_invalid)
    
    
    
    def set_error(self, text):
        
        self.error = self.font.render(text, True, self.cinput_invalid)
    
    
    
    def colours(self, cactive: tuple, chover: tuple, cinactive: tuple, cinvalid: tuple, ctext: tuple):
        
        self.cinput_active = cactive
        self.cinput_hover = chover
        self.cinput_inactive = cinactive
        self.cinput_invalid = cinvalid
        self.ctext = ctext
    
    
    
    def toggle_lock(self, text: str):
        
        if self.lock:
            self.text = self.lock
            self.lock = False
        
        else:
            self.lock = self.text
            self.text = text
    
    
    
    def draw(self, event):
        
        # get mouse position
        pos = pg.mouse.get_pos()

		#create rect
        input_rect = pg.Rect(self.x, self.y, self.width, self.height)
        
        # render font
        text_img = self.font.render(self.text, True, self.cinput_text)
        
        # create another rect
        text_rect = text_img.get_rect()
        text_rect.x, text_rect.y = (self.x + 5, self.y + self.height // 2 - self.text_height // 2)

        # update text size
        self.text_len = text_img.get_width()
        self.text_height = text_img.get_height()
        
        
        
        # check mouseover
        hover = False
        clicked = pg.mouse.get_pressed()[0]
        
        # check if mouse is hovering over box
        if input_rect.collidepoint(pos):
            hover = True
            
            # if mouse is clicked activate box
            if clicked:
                self.active = True
                
                # if text is clicked, update cursor index
                if text_rect.collidepoint(pos):
                    self.cursorindex = floor(((pos[0] - text_rect.x) / text_rect.w * len(self.text)))
                
                # if mouse is clicked to the right of text, set cursor index to last
                else: self.cursorindex = len(self.text) - 1
                    
        # if mouse is clicked outside of box, deactivate it
        elif clicked:
                self.active = False
        
        
        
        # active mode
        if self.active and not self.lock:
            
            # if a key was pressed
            if event:
                
                # if backspace and there is text in the box, remove last character
                if event.key == pg.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:self.cursorindex] + self.text[self.cursorindex + 1:]
                        if self.cursorindex > 0:
                            self.cursorindex -= 1
                
                # dont add empty "return" character when simulation is run
                elif event.key == pg.K_RETURN: pass
                    
                # if not backspace or enter, add character, unless current text box is full
                elif self.text_len <= self.width - 15:
                    text_ = self.text[:self.cursorindex + 1] + event.unicode
                    if self.cursorindex < len(self.text):
                        text_ += self.text[self.cursorindex + 1:]
                    self.text = text_
                    self.cursorindex += 1
                    
            # draw cursor
            pass
        

        
        # get colour
        if self.lock: colour = self.cinput_inactive         # locked
        else:
            if self.active: colour = self.cinput_active     # active
            
            elif hover: colour = self.cinput_hover          # hovering
            
            elif self.valid: colour = self.cinput_inactive  # inactive
            
            else: colour = self.cinput_invalid              # invalid
        
        # draw box
        pg.draw.rect(self.screen, colour, input_rect, 2)
        
        
        
        # add shading to box
        pg.draw.line(self.screen, self.cshade_pos, (self.x, self.y), (self.x + self.width, self.y), 2)
        pg.draw.line(self.screen, self.cshade_pos, (self.x, self.y), (self.x, self.y + self.height), 2)
        pg.draw.line(self.screen, self.cshade_neg, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pg.draw.line(self.screen, self.cshade_neg, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)
        
        # draw text in box
        self.screen.blit(text_img, (self.x + 5, self.y + self.height // 2 - self.text_height // 2))
        
        
        
        # draw name
        self.screen.blit(self.name, (self.x + 5, self.y - self.height // 2 - self.text_height // 2))
        
        # if invalid, draw error message
        if not self.valid and not self.active:
            self.screen.blit(self.error, (self.x + 5, self.y + 3 * self.height // 2 - self.text_height // 2 + 5))