'''imports'''

import pygame as pg
from classes import *




'''main'''

def run_pl(config: PL):
    
    # position multipliers
    x = config.window.width
    y = config.window.height
    
    # create title
    title = Title(text="PARTICLE LIFE", pos=(0.5 * x, 0.1 * y), size=0.05 * x)
    
    # create input matrix
    input_matrix = Input_Matrix(config.matrix, (0.07 * x, 0.25 * y, 0.4 * x, 0.4 * x))
    
    # create input boxes
    boxes = [
        
        num_particles_box := Input_Box(name="NUMBER OF PARTICLES:",
                                       rect=(0.51 * x, 0.72 * y, 0.17 * x, 0.03 * y),
                                       text=f"{config.num_particles}",
                                       error_message="number of particles should be an int greater than zero"),
        
        size_box := Input_Box(name="SIZE:",
                              rect=(0.51 * x, 0.82 * y, 0.17 * x, 0.03 * y),
                              text=f"{config.size}",
                              error_message="size should be an int greater than zero"),
        
        r_max_box := Input_Box(name="RANGE:",
                               rect=(0.72 * x, 0.72 * y, 0.17 * x, 0.03 * y),
                               text=f"{round(config.r_max, 3)}",
                               error_message="range should be a float greater than zero"),
        
        forcefactor_box := Input_Box(name="FORCE FACTOR:",
                                     rect=(0.72 * x, 0.82 * y, 0.17 * x, 0.03 * y),
                                     text=f"{config.forcefactor}",
                                     error_message="force factor should be an int greater than zero"),
        
        fps_box := Input_Box(name="FPS-CAP:",
                             rect=(0.67 * x, 0.6 * y, 0.1 * x, 0.03 * y),
                             text=f"{config.fps_cap}",
                             error_message="fps cap should be an int greater than five"),
        
        dt_box := Input_Box(name="DT:",
                            rect=(0.79 * x, 0.6 * y, 0.1 * x, 0.03 * y),
                            text=f"{config.dt * 10}",
                            error_message="dt should be a float between zero and one")
    ]
    
    # create buttons
    run_button = Button((0.78 * x, 0.395 * y , 0.2 * x, 0.3 * y), "RUN!", font="Impact")
    return_button = Button((0.06 * x, 0.07 * y, 0.07 * x, 0.07 * y), "BACK")
    mystery_button = Button((0.94 * x, 0.07 * y, 0.07 * x, 0.07 * y), "SECRET", hidden=True)
    
    # matrix buttons
    add_button = Button((0.52 * x, 0.29 * y, 0.08 * y, 0.08 * y), "+", font="Impact")
    remove_button = Button((0.52 * x, 0.405 * y, 0.08 * y, 0.08 * y), "-", font="Impact")
    randomise_button = Button((0.52 * x, 0.52 * y, 0.08 * y, 0.08 * y), "RND")
    

    
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
        
        # draw title
        title.draw(config.window)
        
        # draw input matrix
        config.matrix = input_matrix.draw(config.window)
        
        
        
        # temp validities
        num_particles_box.valid = True if config.mb else valid_num(config, num_particles_box.text.lower()) # number of particles
        size_box.valid = True if config.mb else valid_size(config, size_box.text.lower())                  # particle size
        r_max_box.valid = True if config.mb else valid_range(config, r_max_box.text.lower())               # range
        forcefactor_box.valid = True if config.mb else valid_force(config, forcefactor_box.text.lower())   # force factor
        fps_box.valid = valid_fps(config, fps_box.text.lower()) # allowed to change during mb              # fps cap
        dt_box.valid = valid_dt(config, dt_box.text.lower()) # allowed to change during mb                 # dt
        
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
            
            # lock input matrix
            input_matrix.toggle_lock()
            
            # lock input boxes
            for box in boxes:
                box.toggle_lock("MYSTERY BOX!!!")
            
            # unlock FPS cap and dt
            fps_box.toggle_lock(None)
            dt_box.toggle_lock(None)
        
        
        
        # draw matrix buttons
        if add_button.draw(config.window):
            input_matrix.add_dim()
        
        if remove_button.draw(config.window):
            input_matrix.remove_dim()
            
        if randomise_button.draw(config.window) and not input_matrix.locked:
            input_matrix.matrix = rnd_matrix(input_matrix.dim)
        
        
        
        # update screen
        config.window.update(fps=60)
    
    
    
    # reset mystery box
    config.mb = False
    
    



'''input handeling'''

def valid_num(config: PL, user_input: str):
    
    try:
        num = int(user_input)
        
        if num > 0:
            
            config.num_particles = num
            config.num_particles_rnd = False
            return True
    
    except:
        if user_input == "random": config.num_particles_rnd = True; return True



def valid_size(config: PL, user_input: str):
    
    try:
        size = int(user_input)
        
        if size > 0:
            
            config.size = size
            config.size_rnd = False
            return True
    
    except:
        if user_input == "random": config.size_rnd = True; return True



def valid_range(config: PL, user_input: str):
    
    try:
        r = float(user_input)
        
        if 0 < r <= 1:
            
            config.r_max = r
            config.r_max_rnd = False
            return True
    
    except:
        if user_input == "random": config.r_max_rnd = True; return True



def valid_force(config: PL, user_input: str):
    
    try:
        forcefactor = int(user_input)
        
        if forcefactor > 0:
            
            config.forcefactor = forcefactor
            config.forcefactor_rnd = False
            return True
    
    except:
        if user_input == "random": config.forcefactor_rnd = True; return True
        
        

def valid_fps(config: PL, user_input: str):
    
    try:
        fps_cap = int(user_input)
        
        if fps_cap >= 5:
            
            config.fps_cap = fps_cap
            return True
    
    except: return False



def valid_dt(config: PL, user_input: str):
    
    try:
        dt = float(user_input)
        
        if 0 < dt <= 1:
            
            config.dt = dt / 10
            return True
    
    except: return False