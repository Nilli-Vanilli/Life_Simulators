'''imports'''

import pygame as pg
from classes import *




'''main'''

def run_pl(config):
    
    # position multipliers
    x = config.window.width
    y = config.window.height
    
    # create title
    title = Title(text="PARTICLE LIFE", pos=(0.5 * x, 0.1 * y), size=0.05 * x)
    
    # create input matrix
    input_matrix = Input_Matrix(config.matrix, (0.2 * x, 0.2 * y, 0.4 * x, 0.4 * x))
    
    # create buttons
    run_button = Button((0.78 * x, 0.5 * y , 0.2 * x, 0.3 * y), "RUN!", font="Impact")
    return_button = Button((0.06 * x, 0.07 * y, 0.07 * x, 0.07 * y), "BACK")
    mystery_button = Button((0.94 * x, 0.07 * y, 0.07 * x, 0.07 * y), "SECRET", hidden=True)
    

    
    # running loop
    running = True
    while running:
        
        key = False
        
        for event in pg.event.get():
            
            # window close button (windows)
            if event.type == pg.QUIT:
                running = not running
                break
            
            # detect button press
            if event.type == pg.KEYDOWN:
                key = event
                
                # end simulation (escape)
                if event.key == pg.K_ESCAPE:
                    running = False
                    break
                
                # run sim (enter)
                if event.key == pg.K_RETURN and all(validities):
                    config.run()
                
                elif event.key == pg.K_SPACE:
                    input_matrix.add_dim()
                
                elif event.key == pg.K_BACKSPACE:
                    input_matrix.remove_dim()
                     
        
        
        # draw background
        config.window.draw_bg()
        
        # draw title
        title.draw(config.window)
        
        
        
        # draw input matrix
        config.matrix = input_matrix.draw(config.window)
        
        
        
        # temp validities
        validities = [True]
        
        
        
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
            
            # lock input matrix
            input_matrix.toggle_lock()
            
            '''
            # lock input boxes
            for box in boxes:
                box.toggle_lock("MYSTERY BOX!!!")
            
            # unlock FPS cap
            fps_box.toggle_lock(None)
            '''
        
        
        
        # update screen
        config.window.update(fps=60)
    
    
    
    # reset mystery box
    config.mb = False
