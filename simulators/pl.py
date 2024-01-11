'''imports'''

import pygame as pg
from classes import *




'''main'''

def run_pl(config):
    
    
    
    
    
     # create buttons
    run_button = Button((600,500,200,200), "RUN!")
    return_button = Button((50,50,100,50), "back")
    mystery_button = Button((600,800,100,50), "mystery", hidden=True)
    

    
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
                     
        
        
        # draw background
        config.window.draw_bg()
        
        
        
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
