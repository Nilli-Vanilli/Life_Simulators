from classes.window import Window
import pygame as pg
from math import floor

class Input_Box(Window):
    
    # states
    active = False
    valid = False
    hover = False
    lock = False
    
    # text size
    text_len = 0
    text_height = 0
    
    # cursor index and time
    cursorindex = None
    start_time = pg.time.get_ticks()
    

    
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
    
    
    
    def create_rects(self, text_img):
        
        #create rect for box
        input_rect = pg.Rect(self.x, self.y, self.width, self.height)
        
        # create rect for text
        text_rect = text_img.get_rect()
        text_rect.x, text_rect.y = (self.x + 5, self.y + self.height // 2 - self.text_height // 2)
        
        return input_rect, text_rect
        
        
        
    def get_text_width(self, text):
        
        text = self.font.render(text, True, self.cinput_text)
        rect = text.get_rect()
        width = rect.w
        
        return width
    
    
    
    def update_index(self, text_rect, x):
        
        # get relative size of text to determine how precise our search should be
        scale = len(self.text) // 10
        
        # get estimate of index
        x -= text_rect.x # get position of mouse relative to text
        idx = int(x / text_rect.w * len(self.text)) - scale # get ratio and multiply by amount of characters to find an estimate
        
        # because width of characters is not uniform, get width of text slices of neighbouring indices
        # and find the one closest to the position of the mouse relative to the text, to adjust the index
        diffs = [abs(self.get_text_width(self.text[:idx + i]) - x) for i in range(3 + scale)]
        idx += diffs.index(min(diffs))
        
        self.cursorindex = idx
        
    
    
    def draw_cursor(self):
        
        # if cursor not all the way to the left, find width of text up to the cursor index and use to get cursor pos
        if self.cursorindex > 0:   
            x = self.x + 5 + self.get_text_width(self.text[:self.cursorindex])
        
        # if cursor is to the left, just set cursor pos at the left side of the box
        else: x = self.x + 5
        
        # height and vertical pos just matches that of text
        y = self.y + self.height // 2 - self.text_height // 2
        
        # create bool that inverts every half second and only draw cursor when it is true
        if ((pg.time.get_ticks() - self.start_time)//500 + 1) % 2:
            pg.draw.line(self.screen, self.cshade_neg, (x,y), (x,y + self.text_height - 2), 3)
        
        
    
    def check_mouseover(self, input_rect, text_rect):
        
        # check if mouse is clicked
        clicked = pg.mouse.get_pressed()[0]
        
        # get mouse position
        pos = pg.mouse.get_pos()
        
        # check if mouse is hovering over box
        if input_rect.collidepoint(pos):
            self.hover = True
            
            # if mouse is clicked activate box
            if clicked:
                self.active = True
                self.start_time = pg.time.get_ticks() # reset timer for cursor (so it gets drawn)
                
                # if text is clicked, update cursor index
                if text_rect.collidepoint(pos):
                    self.update_index(text_rect, pos[0])
                
                # if mouse is clicked to the right of text, set cursor index to last
                else: self.cursorindex = len(self.text)
                    
        # if mouse is clicked outside of box, deactivate it
        elif clicked:
            self.active = False
        
        # if mouse is not hovering over box
        else: self.hover = False
        
    
    
    def active_mode(self, event):
        
        # check if a key was pressed
            if event:
                
                # if backspace:
                if event.key == pg.K_BACKSPACE:
                    
                    # check if there is text in the box and the cursor is not all the way to the left
                    if len(self.text) * self.cursorindex != 0:
                        
                        # remove a character behind the cursor and decrease the cursor index
                        self.text = self.text[:self.cursorindex - 1] + self.text[self.cursorindex:]
                        self.cursorindex -= 1
                
                # dont add empty "return" character when simulation is run with enter
                elif event.key == pg.K_RETURN: pass
                    
                # if not backspace or enter, add character in front of cursor and increase the cursor index
                elif self.text_len <= self.width - 15:
                    self.text = self.text[:self.cursorindex] + event.unicode + self.text[self.cursorindex:]
                    self.cursorindex += 1
                  
            # draw cursor
            self.draw_cursor()
             
    
    
    def get_colour(self):
        
        if self.lock: colour = self.cinput_inactive     # locked
        
        elif self.active: colour = self.cinput_active   # active
            
        elif self.hover: colour = self.cinput_hover     # hovering
        
        elif self.valid: colour = self.cinput_inactive  # inactive
        
        else: colour = self.cinput_invalid              # invalid
            
        return colour
    
    
    
    def shade_box(self):
        
        pg.draw.line(self.screen, self.cshade_pos, (self.x, self.y), (self.x + self.width, self.y), 2)
        pg.draw.line(self.screen, self.cshade_pos, (self.x, self.y), (self.x, self.y + self.height), 2)
        pg.draw.line(self.screen, self.cshade_neg, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pg.draw.line(self.screen, self.cshade_neg, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)
        
        
    
    def draw(self, event):
        
        # render font
        text_img = self.font.render(self.text, True, self.cinput_text)

        # update text size
        self.text_len = text_img.get_width()
        self.text_height = text_img.get_height()
        
        # create rect objects
        input_rect, text_rect = self.create_rects(text_img)
        
        # check mouseover
        self.check_mouseover(input_rect, text_rect)
        
        # if box is active and not locked, allow user to adjust text
        if self.active and not self.lock:
            self.active_mode(event)
            
        # get colour
        colour = self.get_colour()
        
        # draw box
        pg.draw.rect(self.screen, colour, input_rect, 2)
        
        # add shading to box
        self.shade_box()
        
        # draw text in box
        self.screen.blit(text_img, (self.x + 5, self.y + self.height // 2 - self.text_height // 2))
        
        # draw name
        self.screen.blit(self.name, (self.x + 5, self.y - self.height // 2 - self.text_height // 2))
        
        # if invalid, draw error message
        if not self.valid and not self.active:
            self.screen.blit(self.error, (self.x + 5, self.y + 3 * self.height // 2 - self.text_height // 2 + 5))