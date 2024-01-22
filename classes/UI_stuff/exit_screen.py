# not a class but oh well
import pygame as pg
from classes.UI_stuff import *

def exit_screen(window):
    
    # position multipliers
    x = window.width
    y = window.height
    
    # create text
    title = Title("Are you sure you want to quit?", (0.5 * x,0.35 * y), 0.04 * x,
                  font=window.fonts.subtitle, underlined=False)
    
    # create buttons
    yes_button = Button((0.5 * x, 0.5 * y, 0.3 * x, 0.1 * y), "YES")
    no_button = Button((0.5 * x, 0.65 * y, 0.3 * x, 0.1 * y), "NO")
    
    # create surface to change opacity
    surface = pg.Surface((window.width, window.height), pg.SRCALPHA)
    
    # draw surface
    colour = window.colours.bg + (200,) # add alpha value of 200 to current background
    pg.draw.rect(surface, colour, (0,0,window.width,window.height))
    window.screen.blit(surface, (0,0))
    
    # running loop
    running = True
    while running:
        
        for event in pg.event.get():
            
            # window close button (when tabbed out)
            if event.type == pg.QUIT:
                running = False
                stay = False
             
            # exit programme (escape)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                    stay = False

        # draw text
        title.draw(window)
        
        # draw yes button
        if yes_button.draw(window):
            running = False
            stay = False
        
        # draw no buton
        elif no_button.draw(window):
            running = False
            stay = True
        
        # update screen
        window.update(fps=60)
    
    # if user does anything, return to main
    # tell main to exit unless user clicks no
    return stay