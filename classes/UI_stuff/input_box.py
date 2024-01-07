from classes.window import Window
import pygame as pg

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
        
        
        
        # check if box is clicked
        hover = False
        if input_rect.collidepoint(pos):
            
            hover = True
            
            if pg.mouse.get_pressed()[0] and not self.active:
                self.active = True
            
        else:
            if pg.mouse.get_pressed()[0] and self.active:
                self.active = False
        
        
        
        # update text
        if self.active and not self.lock and event:
                
                # if backspace, remove last character
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                
                # dont add empty "return" character when simulation is run
                elif event.key == pg.K_RETURN: pass
                    
                # if not backspace or enter, add character, unless current text box is full
                elif self.text_len <= self.width - 15:
                    self.text += event.unicode
        

        
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
        
        
        
        # render font
        text_img = self.font.render(self.text, True, self.cinput_text)
        
        # update text size
        self.text_len = text_img.get_width()
        self.text_height = text_img.get_height()
        
        # draw text in box
        self.screen.blit(text_img, (self.x + 5, self.y + self.height // 2 - self.text_height // 2))
        
        
        
        # draw name
        self.screen.blit(self.name, (self.x + 5, self.y - self.height // 2 - self.text_height // 2))
        
        # if invalid, draw error message
        if not self.valid and not self.active:
            self.screen.blit(self.error, (self.x + 5, self.y + 3 * self.height // 2 - self.text_height // 2 + 5))