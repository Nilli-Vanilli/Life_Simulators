'''imports'''

import pygame as pg
from classes import *




'''main'''

def run_sl(config: SL):
    
    # position multipliers
    x = config.window.width
    y = config.window.height
    
    # create title
    title = Title(text="SMOOTH LIFE", pos=(0.5 * x, 0.1 * y), size=0.05 * x)
    
    # create text for rgb channels
    rgb_title = Title(text="RGB CHANNELS:", pos=(0.78 * x, 0.7 * y), size=0.03 * x, font=config.window.fonts.subtitle)
    rgb_error = Title(text="at least one channel should be selected", pos=(0.78 * x, 0.91 * y),size=0.03 * y,
                      font=config.window.fonts.text, colour=(255,0,0), underlined=False)
    
    # create input boxes
    boxes = [
        
        modes_box := Input_Box(name="SIGMOID- AND STEPMODE:",
                               rect=(0.05 * x, 0.25 * y, 0.5 * x, 0.03 * y),
                               text=f"{(config.sigmode, config.stepmode)}",
                               error_message="modes should be a pair of ints between 1 and 4 (or step 0 for discrete time step)"),
        
        types_box := Input_Box(name="SIGMOID- AND MIXTYPES:",
                               rect=(0.05 * x, 0.35 * y, 0.5 * x, 0.03 * y),
                               text=f"{(config.sigtype, config.mixtype)}",
                               error_message="types should be a pair of ints out of {0,1,4}"),
        
        size_box := Input_Box(name="SIZE:",
                              rect=(0.05 * x, 0.45 * y, 0.5 * x, 0.03 * y),
                              text=f"{config.size}",
                              error_message="size should be an int between 5 and 20"),
        
        ra_box := Input_Box(name="OUTER RADIUS:",
                            rect=(0.05 * x, 0.55 * y, 0.5 * x, 0.03 * y),
                            text=f"{round(config.ra, 3)}",
                            error_message="outer radius should be a float between 5 and 50"),
        
        birth_box := Input_Box(name="BIRTH RANGE:",
                               rect=(0.05 * x, 0.65 * y, 0.5 * x, 0.03 * y),
                               text=f"{tuple(round(a, 3) for a in config.birth_range)}",
                               error_message="birth range should be a pair of floats between 0 and 1 such that range[0] < range[1]"),  
        
        survival_box := Input_Box(name="SURVIVAL RANGE:",
                                  rect=(0.05 * x, 0.75 * y, 0.5 * x, 0.03 * y),
                                  text=f"{tuple(round(a, 3) for a in config.survival_range)}",
                                  error_message="survival range should be a pair of floats between 0 and 1 such that range[0] < range[1]"),
        
        widths_box := Input_Box(name="SIGMOID WIDTHS:",
                                rect=(0.05 * x, 0.85 * y, 0.5 * x, 0.03 * y),
                                text=f"{tuple(round(a, 3) for a in config.sigmoid_widths)}",
                                error_message="sigmoid widths should be a pair of floats such that 0 < widths[0] <= 0.2 and 0 < widths[1] <= 1"),                                     
        
        fps_box := Input_Box(name="FPS-CAP:",
                             rect=(0.67 * x, 0.6 * y, 0.1 * x, 0.03 * y),
                             text=f"{config.fps_cap}",
                             error_message="fps cap should be an int greater than five"),
        
        dt_box := Input_Box(name="DT:",
                            rect=(0.79 * x, 0.6 * y, 0.1 * x, 0.03 * y),
                            text=f"{config.dt}",
                            error_message="dt should be a float between 0 and 1")
        
        ]
    
    # create buttons
    run_button = Button((0.78 * x, 0.4 * y , 0.2 * x, 0.3 * y), "RUN!", font="Impact")
    return_button = Button((0.06 * x, 0.07 * y, 0.07 * x, 0.07 * y), "BACK")
    mystery_button = Button((0.94 * x, 0.07 * y, 0.07 * x, 0.07 * y), "SECRET", hidden=True)
    
    # rgb channel buttons
    red_button = Button((0.68 * x, 0.82 * y, 0.07 * x, 0.07 * x), "R")
    green_button = Button((0.78 * x, 0.82 * y, 0.07 * x, 0.07 * x), "G")
    blue_button = Button((0.88 * x, 0.82 * y, 0.07 * x, 0.07 * x), "B")
    

    
    # running loop
    running = True
    while running:
        
        key = False
        
        for event in pg.event.get():
            
            # window close button (when tabbed out)
            if event.type == pg.QUIT:
                running = not running
            
            # detect button press
            if event.type == pg.KEYDOWN:
                key = event
                
                # end simulation (escape)
                if event.key == pg.K_ESCAPE:
                    running = not running
                
                # run sim (enter)
                if event.key == pg.K_RETURN and all(validities):
                    config.run()
                     
        
        
        # draw background
        config.window.draw_bg()
        
        # draw title
        title.draw(config.window) 
            
        
        
        # check input box validities
        modes_box.valid = True if config.mb else valid_modes(config, modes_box.text.lower())
        types_box.valid = True if config.mb else valid_types(config, types_box.text.lower())
        size_box.valid = True if config.mb else valid_size(config, size_box.text.lower())
        ra_box.valid = True if config.mb else valid_ra(config, ra_box.text.lower())
        birth_box.valid = True if config.mb else valid_birth(config, birth_box.text.lower())
        survival_box.valid = True if config.mb else valid_survival(config, survival_box.text.lower())
        widths_box.valid = True if config.mb else valid_widths(config, widths_box.text.lower())
        fps_box.valid = valid_fps(config, fps_box.text.lower()) # allowed to change during mb
        dt_box.valid = valid_dt(config, dt_box.text.lower()) # allowed to change during mb
        
        input_validities = [box.valid for box in boxes]
        
        # check if at least one rgb channel is selected
        rgb_validity = [any([config.red, config.green, config.blue])]
        
        # combine validities
        validities = input_validities + rgb_validity
        
        
        
        # draw boxes
        for box in boxes:
            box.draw(config.window, key)
        
        
        
        # draw run button
        if all(validities):
            run_button.set_colours("green2", "green", "green3", "white")  # valid
            if run_button.draw(config.window): config.run()
        
        else:
            run_button.set_colours("gray62", "gray75", "gray57", "white") # invalid
            run_button.draw(config.window)
        
        
        
        # draw return button
        if return_button.draw(config.window):
            running = False
            
            

        # draw mystery box button
        if mystery_button.draw(config.window):
            config.mb = not config.mb
            mystery_button.hidden = not mystery_button.hidden
            
            # lock input boxes
            for box in boxes:
                box.toggle_lock("MYSTERY BOX!!!")
            
            # unlock FPS cap and dt
            fps_box.toggle_lock(None)
            dt_box.toggle_lock(None)
            
        
        
        # draw RGB buttons
        if config.red: red_button.set_colours("red2", "red", "red3", "white")                # red
        else: red_button.set_colours("red4", "red3", "red", "white")
        if red_button.draw(config.window): config.red = not config.red
        
        if config.green: green_button.set_colours("green2", "green", "green3", "white")     # green
        else: green_button.set_colours("green4", "green3", "green", "white")
        if green_button.draw(config.window): config.green = not config.green
        
        if config.blue: blue_button.set_colours("blue2", "blue", "blue3", "white")          # blue
        else: blue_button.set_colours("blue4", "blue3", "blue", "white")
        if blue_button.draw(config.window): config.blue = not config.blue
        
        # draw RBG titles
        rgb_title.draw(config.window)             # rgb channels
        if not rgb_validity[0]:
            rgb_error.draw(config.window)         # error message
        
        
        
        # update screen
        config.window.update(fps=60)
        
        
    
    # reset mystery box
    config.mb = False
    
    
    
    
    
    '''input handeling'''

def valid_modes(config: SL, user_input: str):
    
    try:
        modes = tuple(int(i) for i in user_input.strip("()").split(","))
        
        if len(modes) != 2:
            return False
        
        if 0 < modes[0] <= 4 and 0 <= modes[1] <= 4:
            
            config.sigmode = modes[0]
            config.stepmode = modes[1]
            config.modes_rnd = False
            return True
    
    except:
        match user_input:
            
            case "random": config.modes_rnd = True; return True
            case _: return False
            


def valid_types(config: SL, user_input: str):
    
    try:
        types = tuple(int(i) for i in user_input.strip("()").split(","))
        
        if len(types) != 2: return False
        
        if all((typ in (0,1,4)) for typ in types):
            
            config.sigtype = types[0]
            config.mixtype = types[1]
            config.types_rnd = False
            return True
    
    except:
        if user_input == "random": config.types_rnd = True; return True



def valid_size(config: SL, user_input: str):
    
    try: 
        size = int(user_input)
        
        if 5 <= size <= 20:
            
            config.size = size
            config.size_rnd = False
            return True
    
    except:
        if user_input == "random": config.size_rnd = True; return True



def valid_ra(config: SL, user_input: str):
    
    try:
        ra = float(user_input)
        
        if 5 <= ra <= 50:
            
            config.ra = ra
            config.ri = ra / 3
            config.ra_rnd = False
            return True
    
    except:
        if user_input == "random": config.ra_rnd = True; return True



def valid_birth(config: SL, user_input: str):
    
    try:
        b_range = tuple(float(i) for i in user_input.strip("()").split(","))
            
        if len(b_range) != 2 or b_range[0] >= b_range[1]:
            return False
        
        if all((0 <= val <= 1) for val in b_range):
            
            config.birth_range = b_range
            config.birth_rnd = False
            return True
    
    except:
        if user_input == "random": config.birth_rnd = True; return True
        


def valid_survival(config: SL, user_input: str):
    
    try:
        s_range = tuple(float(i) for i in user_input.strip("()").split(","))
            
        if len(s_range) != 2 or s_range[0] >= s_range[1]:
            return False
        
        if all((0 <= val <= 1) for val in s_range):
            
            config.survival_range = s_range
            config.survival_rnd = False
            return True
    
    except:
        if user_input == "random": config.survival_rnd = True; return True
        


def valid_widths(config: SL, user_input: str):
    
    try:
        widths = tuple(float(i) for i in user_input.strip("()").split(","))
            
        if len(widths) != 2:
            return False
        
        if 0 < widths[0] <= 0.2 and 0 < widths[1] <= 1:
            
            config.sigmoid_widths = widths
            config.widths_rnd = False
            return True
    
    except:
        if user_input == "random": config.widths_rnd = True; return True



def valid_fps(config: SL, user_input: str):
    
    try:
        fps_cap = int(user_input)
        
        if fps_cap >= 5:
            
            config.fps_cap = fps_cap
            return True
    
    except: return False



def valid_dt(config: SL, user_input: str):
    
    try:
        dt = float(user_input)
        
        if 0 < dt <= 1:
            
            config.dt = dt
            return True
    
    except: return False
    