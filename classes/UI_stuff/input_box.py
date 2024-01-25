from classes.style import Colours, Fonts
from classes.window import Window
import pygame as pg

class Input_Box():
    
    # states
    active = False
    valid = False
    hover = False
    lock = False
    lock_colour = False
    lock_font = False
    
    # text size
    text_len = 0
    text_height = 0
    
    # cursor index and timer
    cursorindex = None
    timer = None
    

    
    def __init__(self, name: str, rect: tuple, text: str, error_message: str, font=None) -> None:
        
        x, y, width, height = rect
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.text = text
        self.name = name
        self.error = error_message
        
        self.colours = Colours()
        self.fonts = Fonts()
        
        if font:
            self.fonts.text = font
            self.lock_font = True

        self.font = pg.font.SysFont(self.fonts.text, int(self.height))
    
    
    
    def reset(self):
        
        # render font and texts again
        self.font = pg.font.SysFont(self.fonts.text, int(self.height))
        text_img = self.font.render(self.text, True, self.colours.input_text)
        name_img = self.font.render(self.name, True, self.colours.input_text)
        error_img = self.font.render(self.error, True, self.colours.input_invalid)
        
        return text_img, name_img, error_img
    
    
    
    def colours(self, active: tuple, hover: tuple, inactive: tuple, invalid: tuple, text: tuple):
        
        # set new colours and lock them
        self.colours.input_active = active
        self.colours.input_hover = hover
        self.colours.input_inactive = inactive
        self.colours.input_invalid = invalid
        self.colours.input_text = text
        self.lock_colour = True
    
    
    
    def toggle_lock(self, text: str):
        
        # if locked, unlock and get stored text
        if self.lock:
            self.text = self.lock
            self.lock = False
        
        # if unlocked, lock and store current text
        else:
            self.lock = self.text
            self.text = text
    
    
    
    def create_rects(self, text_img: pg.Surface):
        
        #create rect for box
        input_rect = pg.Rect(self.x, self.y, self.width, self.height)
        
        # create rect for text
        text_rect = text_img.get_rect()
        text_rect.x, text_rect.y = (self.x + 5, self.y + self.height // 2 - self.text_height // 2)
        
        return input_rect, text_rect
        
        
        
    def get_text_width(self, text: str):
        
        # render text and get its width on the screen
        text = self.font.render(text, True, self.colours.input_text)
        rect = text.get_rect()
        width = rect.w
        
        return width
    
    
    
    def update_index(self, text_rect: pg.Surface, x: float):
        
        # get relative size of text to determine how precise our search should be
        scale = len(self.text) // 10
        
        # get estimate of index
        x -= text_rect.x # get position of mouse relative to text
        index = int(x / text_rect.w * len(self.text)) - scale # get ratio and multiply by amount of characters to find an estimate
        
        # because width of characters is not uniform, get width of text slices of neighbouring indices
        # and find the one closest to the position of the mouse relative to the text, to adjust the index
        diffs = [abs(self.get_text_width(self.text[:index + i]) - x) for i in range(3 + scale)]
        index += diffs.index(min(diffs))
        
        self.cursorindex = index
        
    
    
    def draw_cursor(self, screen: pg.Surface):
        
        # if cursor not all the way to the left, find width of text up to the cursor index and use to get cursor pos
        if self.cursorindex > 0:   
            x = self.x + 5 + self.get_text_width(self.text[:self.cursorindex])
        
        # if cursor is to the left, just set cursor pos at the left side of the box
        else: x = self.x + 5
        
        # height and vertical pos just matches that of text
        y = self.y + self.height // 2 - self.text_height // 2
        
        # create bool that inverts every half second and only draw cursor when it is true
        if ((pg.time.get_ticks() - self.timer)//500 + 1) % 2:
            pg.draw.line(screen, self.colours.input_cursor, (x,y), (x,y + self.text_height - 2), 3)
        
        
    
    def check_mouseover(self, input_rect: pg.Surface, text_rect: pg.Surface):
        
        # get mouse position and check if left mousebutton is clicked
        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]
        
        # check if mouse is hovering over box
        if input_rect.collidepoint(pos):
            self.hover = True
            
            # if mouse is clicked activate box
            if click:
                self.active = True
                self.timer = pg.time.get_ticks() # reset timer for cursor (so it gets drawn)
                
                # if text is clicked, update cursor index
                if text_rect.collidepoint(pos):
                    self.update_index(text_rect, pos[0])
                
                # if mouse is clicked to the right of text, set cursor index to last
                else: self.cursorindex = len(self.text)
                    
        # if mouse is clicked outside of box, deactivate it
        elif click:
            self.active = False
        
        # if mouse is not hovering over box
        else: self.hover = False
        
    
    
    def active_mode(self, screen: pg.Surface, key: pg.event.Event):
        
        # check if a key was pressed
            if key:
                
                # if backspace:
                if key.key == pg.K_BACKSPACE:
                    
                    # check if there is text in the box and the cursor is not all the way to the left
                    if len(self.text) * self.cursorindex > 0:
                        
                        # remove a character behind the cursor and decrease the cursor index
                        self.text = self.text[:self.cursorindex - 1] + self.text[self.cursorindex:]
                        self.cursorindex -= 1
                
                # if left arrow, move cursor index left if possible
                elif key.key == pg.K_LEFT and self.cursorindex > 0:
                    self.cursorindex -= 1
                
                # if right arrow, move cursor index right if possible
                elif key.key == pg.K_RIGHT and self.cursorindex < len(self.text):
                    self.cursorindex += 1
                
                # ignore these inputs (don't add empty character)
                elif key.key in [pg.K_RETURN, pg.K_LSHIFT, pg.K_RSHIFT, pg.K_LCTRL, pg.K_RCTRL, pg.K_CAPSLOCK]: 
                    pass
                    
                # if user inputs character and box is not full,
                # add character in front of cursor and increase the cursor index
                elif self.text_len <= self.width - 15:
                    self.text = self.text[:self.cursorindex] + key.unicode + self.text[self.cursorindex:]
                    self.cursorindex += 1
                  
            # draw cursor
            self.draw_cursor(screen)
             
    
    
    def get_colour(self):
        
        if self.lock: colour = self.colours.input_inactive     # locked
        
        elif self.active: colour = self.colours.input_active   # active
            
        elif self.hover: colour = self.colours.input_hover     # hovering
        
        elif self.valid: colour = self.colours.input_inactive  # inactive
        
        else: colour = self.colours.input_invalid              # invalid
            
        return colour
    
    
    
    def shade_box(self, screen: pg.Surface):
        
        pg.draw.line(screen, self.colours.shade_pos, (self.x, self.y), (self.x + self.width, self.y), 2)
        pg.draw.line(screen, self.colours.shade_pos, (self.x, self.y), (self.x, self.y + self.height), 2)
        pg.draw.line(screen, self.colours.shade_neg, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pg.draw.line(screen, self.colours.shade_neg, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)
        
        
    
    def draw(self, window: Window, key: pg.event.Event):
        
        # reset colours and fonts
        if not self.lock_colour:
            self.colours = window.colours
        if not self.lock_font:
            self.fonts = window.fonts
        
        # reset text images
        text_img, name_img, error_img = self.reset()

        # update text size
        self.text_len = text_img.get_width()
        self.text_height = text_img.get_height()
        
        # create rect objects
        input_rect, text_rect = self.create_rects(text_img)
        
        # check mouseover
        self.check_mouseover(input_rect, text_rect)
        
        # if box is active and not locked, allow user to input text
        if self.active and not self.lock:
            self.active_mode(window.screen, key)
            
        # get colour
        colour = self.get_colour()
        
        # draw box
        pg.draw.rect(window.screen, colour, input_rect, 2)
        
        # add shading to box
        self.shade_box(window.screen)
        
        # draw text in box
        window.screen.blit(text_img, (self.x + 5, self.y + self.height // 2 - self.text_height // 2))
        
        # draw name
        window.screen.blit(name_img, (self.x + 5, self.y - self.height // 2 - self.text_height // 2))
        
        # if invalid, draw error message
        if not self.valid and not self.active:
            window.screen.blit(error_img, (self.x + 5, self.y + 3 * self.height // 2 - self.text_height // 2 + 5))