'''imports'''

import pygame as pg
from classes import *



'''main'''

def run_gol(config: GOL):
    
    # position multipliers
    x = config.window.width
    y = config.window.height
    
    # create title
    title = Title(text="GAME OF LIFE", pos=(0.5 * x, 0.1 * y), size=0.05 * x)
    
    # create input boxes
    boxes = [
        
        rule_box := Input_Box(name="RULES:",
                              rect=(0.05 * x, 0.25 * y, 0.5 * x, 0.03 * y),
                              text=f"{config.rules}",
                              error_message="rules should be a triple of ints between 0 and 8 such that rules[0] <= rules[1]"),   

        size_box := Input_Box(name="SIZE:",
                              rect=(0.05 * x, 0.35 * y, 0.5 * x, 0.03 * y),
                              text=f"{config.size}",
                              error_message="size should be an int between 5 and 100"),  

        boundary_box := Input_Box(name="BOUNDARY CONDITION:",
                                  rect=(0.05 * x, 0.45 * y, 0.5 * x, 0.03 * y),
                                  text=config.boundary,
                                  error_message="boundary condition should be one of the following: periodic, dirichlet 0, dirichlet 1, neumann"),                

        cgrid_box := Input_Box(name="COLOUR GRID:",
                               rect=(0.05 * x, 0.55 * y, 0.5 * x, 0.03 * y),
                               text=f"{config.cgrid[:3]}",
                               error_message="colour should be a triple of ints between 0 and 255, or a named colour"),                                           

        coff_box := Input_Box(name="COLOUR OFF STATE:",
                              rect=(0.05 * x, 0.65 * y, 0.5 * x, 0.03 * y),
                              text=f"{config.coff[:3]}",
                              error_message="colour should be a triple of ints between 0 and 255, or a named colour"),
        
        coff_next_box := Input_Box(name="COLOUR OFF NEXT STATE:",
                              rect=(0.05 * x, 0.75 * y, 0.5 * x, 0.03 * y),
                              text=f"{config.coff_next[:3]}",
                              error_message="colour should be a triple of ints between 0 and 255, or a named colour"),     

        con_box := Input_Box(name="COLOUR ON STATE:",
                             rect=(0.05 * x, 0.85 * y, 0.5 * x, 0.03 * y),
                             text=f"{config.con[:3]}",
                             error_message="colour should be a triple of ints between 0 and 255, or a named colour"),
        
        fps_box := Input_Box(name="FPS-CAP:",
                             rect=(0.68 * x, 0.7 * y, 0.1 * x, 0.03 * y),
                             text=f"{config.fps_cap}",
                             error_message="fps cap should be an int greater than five")                                             
        
        ]

    # create buttons
    run_button = Button((0.78 * x, 0.5 * y , 0.2 * x, 0.3 * y), "RUN!", font="Impact")
    return_button = Button((0.06 * x, 0.07 * y, 0.07 * x, 0.07 * y), "BACK")
    mystery_button = Button((0.94 * x, 0.07 * y, 0.07 * x, 0.07 * y), "SECRET", hidden=True)
    
    

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
        
        
        
        # draw bg
        config.window.draw_bg()
        
        # draw title
        title.draw(config.window)
        
        
        
        # update validities
        rule_box.valid = True if config.mb else valid_rule(config, rule_box.text.lower())                         # rule
        size_box.valid = True if config.mb else valid_size(config, size_box.text.lower())                         # size
        boundary_box.valid = True if config.mb else valid_boundary(config, boundary_box.text.lower())             # boundary
        cgrid_box.valid = True if config.mb else valid_colour(config, cgrid_box.text.lower(), "grid")             # colour grid
        coff_box.valid = True if config.mb else valid_colour(config, coff_box.text.lower(), "off")                # colour off
        coff_next_box.valid = True if config.mb else valid_colour(config, coff_next_box.text.lower(), "offnext")  # colour off next gen
        con_box.valid = True if config.mb else valid_colour(config, con_box.text.lower(), "on")                   # colour on
        fps_box.valid = valid_fps_cap(config, fps_box.text.lower()) #allowed to change during mb                  # fps
        
        validities = [box.valid for box in boxes]
        
        
        
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
            
            # unlock FPS cap
            fps_box.toggle_lock(None)
        

        
        # update screen
        config.window.update(fps=60)
    
    
    
    # reset mystery box
    config.mb = False






'''input handeling'''

def valid_rule(config: GOL, user_input: str):
    
    try:
        rule = tuple(int(i) for i in user_input.strip("()").split(","))
        
        if len(rule) != 3 or rule[0] > rule[1]: return False
        
        if all((val in range(10)) for val in rule):
        
            config.rules = rule
            config.rule_rnd = False
            return True
        
    except:  
        if user_input == "random": config.rule_rnd = True; return True



def valid_size(config: GOL, user_input: str):
    
    try: 
        size = int(user_input)
        
        if 5 <= size <= 100:
            
            config.size = size
            config.size_rnd = False
            return True
    
    except:
        if user_input == "random": config.size_rnd = True; return True



def valid_boundary(config: GOL, user_input: str):
    
    boundary_conditions = ("periodic", "dirichlet 0", "dirichlet 1", "neumann")
    
    if user_input in boundary_conditions:
        
        config.boundary = user_input
        config.boundary_rnd = False
        return True
    
    elif user_input == "random": config.boundary_rnd = True; return True



def valid_fps_cap(config: GOL, user_input: str):
    
    try:
        fps_cap = int(user_input)
        
        if fps_cap >= 5:
            
            config.fps_cap = fps_cap
            return True
    
    except: return False



def valid_colour(config: GOL, user_input: str, obj: str):
    
    try:
        colour = tuple(int(i) for i in user_input.strip("()").split(","))
        
        if len(colour) != 3:
            return False
        
        if not all((val in range(256)) for val in colour):
            return False
        
        match obj:
            
            case "grid": config.cgrid = colour; config.cgrid_rnd = False; return True
            case "off": config.coff = colour; config.coff_rnd = False; return True
            case "offnext": config.coff_next = colour; config.coff_next_rnd = False; return True
            case "on": config.con = colour; config.con_rnd = False; return True
        
    except:  
        if user_input == "random":
            match obj:
                
                case "grid": config.cgrid_rnd = True; return True
                case "off": config.coff_rnd = True; return True
                case "offnext": config.coff_next_rnd = True; return True
                case "on": config.con_rnd = True; return True
        
        elif user_input in pg.colordict.THECOLORS.keys():
            match obj:
                
                case "grid": config.cgrid = pg.colordict.THECOLORS[user_input]; config.cgrid_rnd = False; return True
                case "off": config.coff = pg.colordict.THECOLORS[user_input]; config.coff_rnd = False; return True
                case "offnext": config.coff_next = pg.colordict.THECOLORS[user_input]; config.coff_next_rnd = False; return True
                case "on": config.con = pg.colordict.THECOLORS[user_input]; config.con_rnd = False; return True