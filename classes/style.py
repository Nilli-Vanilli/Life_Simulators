import numpy as np

class Colours:
    
    # initialise colours
    
    bg = (254, 249, 239)
    title = (0, 23, 31)
    underline = (0, 52, 89)
    
    shade_pos = (255,255,255)
    shade_neg = (0, 23, 31)
    
    input_text = (0, 23, 31)
    input_active = (0, 126, 167)
    input_hover = (0, 168, 232)
    input_inactive = (0, 23, 31)
    input_invalid = (239, 35, 60)
    input_cursor = (0, 52, 89)
    
    button_text = (255,255,255)
    button_body = (0, 126, 167)
    button_hover = (0, 168, 232)
    button_click = (0, 52, 89)
    
    dark_mode = False
    

    
    def toggle_dark_mode(self):
        
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            
            self.bg = (11, 19, 43)
            self.title = (255, 255, 255)
            self.underline = (111, 255, 233)
            
            self.shade_pos = (111, 255, 233)
            self.shade_neg = (0, 24, 69)
            
            self.input_text = (255, 255, 255)
            self.input_active = (91, 192, 190)
            self.input_hover = (111, 255, 233)
            self.input_inactive = (58, 80, 107)
            self.input_invalid = (183, 9, 76)
            self.input_cursor = (111, 255, 233)
            
            self.button_text = (255,255,255)
            self.button_body = (91, 192, 190)
            self.button_hover = (111, 255, 233)
            self.button_click = (61, 160, 158)
        
        else:
            
            self.bg = (254, 249, 239)
            self.title = (0, 23, 31)
            self.underline = (0, 52, 89)
            
            self.shade_pos = (255,255,255)
            self.shade_neg = (0, 23, 31)
            
            self.input_text = (0, 23, 31)
            self.input_active = (0, 126, 167)
            self.input_hover = (0, 168, 232)
            self.input_inactive = (0, 23, 31)
            self.input_invalid = (239, 35, 60)
            self.input_cursor = (0, 52, 89)
            
            self.button_text = (255,255,255)
            self.button_body = (0, 126, 167)
            self.button_hover = (0, 168, 232)
            self.button_click = (0, 52, 89)
    
    
    
    def rnd_colours(self):
        
        self.bg = tuple(np.random.random(size=3) * 256)
        self.title = tuple(np.random.random(size=3) * 256)
        self.underline = tuple(np.random.random(size=3) * 256)
        
        self.shade_pos = tuple(np.random.random(size=3) * 256)
        self.shade_neg = tuple(np.random.random(size=3) * 256)
        
        self.input_text = tuple(np.random.random(size=3) * 256)
        self.input_active = tuple(np.random.random(size=3) * 256)
        self.input_hover = tuple(np.random.random(size=3) * 256)
        self.input_inactive = tuple(np.random.random(size=3) * 256)
        self.input_invalid = tuple(np.random.random(size=3) * 256)
        self.input_cursor = tuple(np.random.random(size=3) * 256)
        
        self.button_text = tuple(np.random.random(size=3) * 256)
        self.button_body = tuple(np.random.random(size=3) * 256)
        self.button_hover = tuple(np.random.random(size=3) * 256)
        self.button_click = tuple(np.random.random(size=3) * 256)
        
    
    
class Fonts:
    
    # define fonts
    title = "Impact"
    subtitle = "Times New Roman"
    text = "freesansbold"
    button = "freesansbold"