'''
Todo:



MAIN:
readme
github
paper



ECA:



GOL:



PL:
input handling



SMOOTHLIFE:
'''






'''imports'''

import pygame as pg

from classes import *
from simulators import *



'''main'''

def main():
    
    # create window
    window = Window()
    
    # create cellular automata
    CA = Cellular_Automata(window)
    
    # position multipliers
    x = window.width
    y = window.height
    
    # create title
    title = Title(text="LIFE SIMULATORS", pos=(0.5 * x, 0.15 * y), size=0.1 * x)
    subtitle = Title(text="By Niels den Hollander :)", pos=(0.5 * x, 0.3 * y), size = 0.03 * x, font=window.fonts.subtitle, underlined=False)
    
    # create buttons
    eca_button = Button((0.25 * x, 0.45 * y, 0.45 * x, 0.1 * y), "ELEMENTARY CELLULAR AUTOMATA")
    gol_button = Button((0.75 * x, 0.45 * y, 0.45 * x, 0.1 * y), "GAME OF LIFE")
    pl_button = Button((0.25 * x, 0.75 * y, 0.45 * x, 0.1 * y), "PARTICLE LIFE")
    sl_button = Button((0.75 * x, 0.75 * y, 0.45 * x, 0.1 * y), "SMOOTH LIFE")
    
    quit_button = Button((0.06 * x, 0.07 * y, 0.07 * x, 0.07 * y), "QUIT")
    
    theme_button = Button((0.94 * x, 0.07 * y, 0.07 * x, 0.07 * y), "DARK", hidden=True)
    
    
    
    # running loop
    running = True
    while running:
        
        close = False
        
        for event in pg.event.get():
            
            # window close button (when tabbed out)
            if event.type == pg.QUIT:
                running = not running
             
            # exit programme (escape)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    close = not close

                elif event.key == pg.K_r:
                    theme_button.hidden = True
                    window.colours.rnd_colours()
                
                    
        
        # draw background
        window.draw_bg()
        
        
        
        # draw title
        title.draw(window)
        subtitle.draw(window)
        
        
        
        # draw quit button
        if quit_button.draw(window):
            close = True
        
        
        
        # draw theme button
        if theme_button.draw(window):
            theme_button.hidden = False
            window.colours.toggle_dark_mode()
            theme_button.text = "DARK" if window.colours.dark_mode else "LIGHT"
        
        
        
        # draw eca button
        if eca_button.draw(window):
            CA.eca.window = window
            run_eca(CA.eca)
        
        
        
        # draw gol button
        if gol_button.draw(window):
            CA.gol.window = window
            run_gol(CA.gol)
        
        
        
        # draw pl button
        if pl_button.draw(window):
            CA.pl.window = window
            run_pl(CA.pl)
        
        
        
        # draw sl button
        if sl_button.draw(window):
            CA.sl.window = window
            run_sl(CA.sl)
        
        
        
        # if quit button or escape is pressed, call exit screen
        if close: # only call after everything else is drawn onto the screen
            running = exit_screen(window)
        
        
        
        # update screen
        window.update(fps=60)
    
    
    
    # close programme
    pg.quit()
    
    
    


if __name__ == "__main__":
    main()
            