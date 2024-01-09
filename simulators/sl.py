'''imports'''

import pygame as pg
from classes import *




'''main'''

def run_sl(config):
    
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
                              error_message="todo"),
        
        ra_box := Input_Box(name="OUTER RADIUS:",
                            rect=(0.05 * x, 0.55 * y, 0.5 * x, 0.03 * y),
                            text=f"{config.ra}",
                            error_message="todo"),
        
        birth_box := Input_Box(name="BIRTH RANGE:",
                               rect=(0.05 * x, 0.65 * y, 0.5 * x, 0.03 * y),
                               text=f"{config.birth_range}",
                               error_message="todo"),  
        
        survival_box := Input_Box(name="SURVIVAL RANGE:",
                                  rect=(0.05 * x, 0.75 * y, 0.5 * x, 0.03 * y),
                                  text=f"{config.survival_range}",
                                  error_message="todo"),
        
        widths_box := Input_Box(name="SIGMOID WIDTHS:",
                                rect=(0.05 * x, 0.85 * y, 0.5 * x, 0.03 * y),
                                text=f"{config.sigmoid_widths}",
                                error_message="todo"),                                     
        
        fps_box := Input_Box(name="FPS-CAP",
                             rect=(0.67 * x, 0.6 * y, 0.1 * x, 0.03 * y),
                             text=f"{config.fps_cap}",
                             error_message="fps cap should be an int greater than zero"),
        
        dt_box := Input_Box(name="DT:",
                            rect=(0.79 * x, 0.6 * y, 0.1 * x, 0.03 * y),
                            text=f"{config.dt}",
                            error_message="todo")
        
        ]
    
    # create buttons
    run_button = Button((0.78 * x, 0.4 * y , 0.2 * x, 0.3 * y), "RUN!", font="Impact")
    return_button = Button((0.06 * x, 0.07 * y, 0.07 * x, 0.07 * y), "BACK")
    mystery_button = Button((0.94 * x, 0.07 * y, 0.07 * x, 0.07 * y), "SECRET", hidden=True)
    
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
            
        
        
        # temp validities
        input_validities = [True]
        
        # check if at least one rgb channel is selected
        rgb_validity = [any([config.red, config.green, config.blue])]
        
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
            
            # unlock FPS cap
            fps_box.toggle_lock(None)
            
        
        
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