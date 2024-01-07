'''
Todo:



MAIN:
exit screen
dark mode (local)



ECA:



GOL:



PL:
input screen (matrix!!!)
mystery box



SMOOTHLIFE:
mouse draw regions
input screen
r to fill grid
mystery box
'''






'''imports'''

import pygame as pg

from classes import *
from simulators import *



'''main'''

def main():
    
    # create window
    window = Window()
    
    # position multipliers
    x = window.width
    y = window.height
    
    # create title
    title = Title(text="LIFE SIMULATORS", pos=(0.5 * x, 0.15 * y), size=0.1 * x)
    subtitle = Title(text="By Niels den Hollander :)", pos=(0.5 * x, 0.3 * y), size = 0.03 * x, font="Times New Roman", underlined=False)
    
    # create buttons
    eca_button = Button((0.25 * x, 0.45 * y, 0.45 * x, 0.1 * y), "ELEMENTARY CELLULAR AUTOMATA")
    gol_button = Button((0.75 * x, 0.45 * y, 0.45 * x, 0.1 * y), "GAME OF LIFE")
    pl_button = Button((0.25 * x, 0.75 * y, 0.45 * x, 0.1 * y), "PARTICLE LIFE")
    sl_button = Button((0.75 * x, 0.75 * y, 0.45 * x, 0.1 * y), "SMOOTH LIFE")
    
    quit_button = Button((0.06 * x, 0.07 * y, 0.07 * x, 0.07 * y), "QUIT")
    
    
    
    # running loop
    running = True
    while running:
        
        for event in pg.event.get():
            
            # window close button (when tabbed out)
            if event.type == pg.QUIT:
                running = not running
             
            # exit programme (escape)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = not running
                
                    
        
        # draw background
        window.screen.fill(window.cbg)
        
        # draw title
        title.draw()
        subtitle.draw()
        
        
        
        # draw quit button
        if quit_button.draw():
            running = False
        
        
        
        # draw eca button
        if eca_button.draw():
            
            # initialise CA
            config = ECA(
                rule="01101110", 
                size=10, 
                start_indices=[],      # set to middle cell on default
                boundary="periodic",
                fps_cap=60
                )

            # run CA
            eca(config)
        
        
        
        # draw gol button
        if gol_button.draw():
            
            # initialise CA
            config = GOL(
                rules=(2,3,3),
                size=20,
                boundary="periodic",
                fps_cap=10
                )
             
            # run CA
            gol(config)
        
        
        
        # draw pl button
        if pl_button.draw():
            
            # initialise CA
            config = PL(
                matrix=rnd_matrix(6),
                num_particles=300,
                size=3,
                fric_hl=0.04,
                r_max=0.1,
                beta=0.3,
                forcefactor=20,
                follow_mouse=False,
                dt=0.02,
                fps_cap=60
            )
    
            # run CA
            pl(config)
        
        
        
        # draw sl button
        if sl_button.draw():
            
            # initialise CA
            config = SL(
               size=5,
               outer_radius=21,
               sigmode=4,
               sigtype=4,
               mixtype=4,
               stepmode=0,
               dt=0,
               fps_cap=60
            )
    
            # run CA
            sl(config)
        
        
        
        # update screen
        window.update(fps=60)
    
    
    # close programme
    pg.quit()
    
    



if __name__ == "__main__":
    main()
            