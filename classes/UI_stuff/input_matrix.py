from classes.style import Colours
import pygame as pg
import numpy as np

class Input_Matrix:
    
    locked = False
    locked_matrix = None
    
    def __init__(self, matrix: np.ndarray, rect: tuple) -> None:
        
        self.matrix = matrix
        
        self.dim = matrix.shape[0]
        
        x, y, width, height = rect
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.size = self.width / self.dim
    
    
    
    def toggle_lock(self):
        
        if self.locked:
            self.matrix = self.locked_matrix
            self.locked = False
            
        else:
            self.locked_matrix = self.matrix
            self.matrix = np.zeros((10,10))
            self.locked = True
            
            
    
    def add_dim(self):
        
        if self.dim < 10 and not self.locked:
            self.matrix = np.column_stack((self.matrix, np.zeros(self.dim)))
            self.matrix = np.row_stack((self.matrix, np.zeros(self.dim + 1)))
            self.dim += 1
        
    
    
    def remove_dim(self):
        
        if self.dim > 1 and not self.locked:
            self.matrix = np.delete(self.matrix, -1, 0)
            self.matrix = np.delete(self.matrix, -1, 1)
            self.dim -= 1
    
    
    
    def draw_hover(self, window, relative_pos):
        
        x = relative_pos[1]
        y = relative_pos[0]
        
        pg.draw.line(window.screen, window.colours.input_hover, (self.x + x * self.size, self.y + y * self.size), (self.x + x * self.size + self.size, self.y + y * self.size), 2)
        pg.draw.line(window.screen, window.colours.input_hover, (self.x + x * self.size, self.y + y * self.size), (self.x + x * self.size, self.y + y * self.size + self.size), 2)
        pg.draw.line(window.screen, window.colours.input_hover, (self.x + x * self.size, self.y + y * self.size + self.size), (self.x + x * self.size + self.size, self.y + y * self.size + self.size), 2)
        pg.draw.line(window.screen, window.colours.input_hover, (self.x + x * self.size + self.size, self.y + y * self.size), (self.x + x * self.size + self.size, self.y + y * self.size + self.size), 2)
            
            
    
    def check_mouseover(self, window, grid):
        
        pos = pg.mouse.get_pos()
        relative_pos = (int((pos[1] - self.y) / self.size), int((pos[0] - self.x) / self.size))
        
        if grid.collidepoint(pos):
            
            self.draw_hover(window, relative_pos)
            
            if pg.mouse.get_pressed()[0]:
                if self.matrix[relative_pos] < 0.98:
                    self.matrix[relative_pos] += 0.02
            
            elif pg.mouse.get_pressed()[2]:
                if self.matrix[relative_pos] > -0.98:
                    self.matrix[relative_pos] -= 0.02
                
        
        
    
    def shade_grid(self, window):
        
        pg.draw.line(window.screen, window.colours.shade_pos, (self.x, self.y), (self.x + self.width, self.y), 2)
        pg.draw.line(window.screen, window.colours.shade_pos, (self.x, self.y), (self.x, self.y + self.height), 2)
        pg.draw.line(window.screen, window.colours.shade_neg, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pg.draw.line(window.screen, window.colours.shade_neg, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)
        
        
    
    def draw(self, window):
        
        # create rect for grid
        grid_rect = pg.Rect(self.x, self.y, self.width, self.height)
        
        # update dim and cell size
        self.dim = self.matrix.shape[0]
        self.size = self.width / self.matrix.shape[0]
        
        # draw grid
        pg.draw.rect(window.screen, window.colours.underline,(self.x, self.y, self.width, self.height))
        
        # add shading to grid
        self.shade_grid(window)
        
        # draw cells
        for row, col in np.ndindex(self.matrix.shape):
            strength = abs(self.matrix[row, col]) * 255
            colour = (0,strength,0) if self.matrix[row, col] > 0 else (strength,0,0)
            pg.draw.rect(window.screen, colour, (self. x + col * self.size + 1,
                                                 self.y + row * self.size + 1,
                                                 self.size - (self.dim + 1) / self.dim,
                                                 self.size - (self.dim + 1) / self.dim))
        
        # if not locked, allow user input
        if not self.locked:
            self.check_mouseover(window, grid_rect)
        
        return self.matrix