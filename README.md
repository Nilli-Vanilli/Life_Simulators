# Life_Simulators

## Final Project Python Course

This project is the culmination of what I have been able to learn during a beginner python course. It features three cellular automata, as well as a popular simulation called Particle Life. Each of these simulations shows how complex, nature-like structures can emerge from a simple, deterministic set of rules. What I think is especially interesting is how unpredictable these systems can prove to be, and I have really enjoyed interacting with the digital 'creatures' that have popped up on my screen. For this reason, I have attempted to make these simulations as interactive as possible, and I encourage you to not just watch, but play around with them as well.

## requirements

This programme makes use of the following libraries:

1) Pygame
2) NumPy
3) quads

As long as these three libraries have been installed, you can run the programme by simply running the file called 'main.py'

## how to use

### Main Menu

when running the programme, you should find yourself in the main menu. Here you can navigate between the four different simulations, as well as exit the programme using the quit button or the 'escape' key. Here, it is also possible to change the colour scheme of the programme. You can enter dark mode with a secret button hidden in the top right corner of the screen, or you can press 'r' to be surprised with a completely random set of colours.

### Elementary Cellular Automata

The first cellular automaton is the set of ECA's explored by Stephen Wolfram in his book '*A New Kind of Science*'. You should be met with a screen containing seven different input boxes. You can click on these boxes to alter the configuration of the CA by typing in them.
The rule is what determines how a certain generation will evolve over time. It should be an integer between 0 and 255, which can be entered in either binary or decimal.
The size refers to the width and height of each cell in pixels. It can be any integer between five and a hundred. Do note that the size directly affects the amount of cells that make up a generation.
The start indices are the cells that will be turned on in the first generation. It can either be a single integer or a list of them, as long as they do not exceed the number of cells in a generation (the programme will tell you if a certain index is out of bounds). Furthermore, it is possible to enter 'middle' to turn on only the middle cell, or 'empty' to turn on no cells at all.
Then there is the boundary condition. This describes what happens at the edges of the grid, since unfortunately it is not infinite (yet). Currently four different boundary conditions are supported:

1) 'periodic' - the grid wraps around to connect to itself.
2) 'Dirichlet 0' - the edges are always zero.
3) 'Dirichlet 1' - the edges are always one.
4) 'Neumann' - the edges share the state of their neighbour.

Finally there are the colours. These should be a RGB-triples, meaning tuples of length three with integers between 0 and 255. It is also possible to enter any named Pygame colour out of this [list](https://www.pygame.org/docs/ref/color_list.html).

As an added bonus, if you feel like spicing up the cellular experience, each box also allows you to input 'random', which will randomise that part of the configuration each run. If you are feeling truly adventurous, then you might be tempted to try out the secret **mystery box!!!** mode, which can be accessed through a secret button hidden in the top right corner of the screen.

As the simulation is running, it is possible to interact with it in three ways. You can pause and unpause the simulation with the 'space' key. Additionally, You can click (or hold) the left mousebutton anywhere on the screen to toggle on/off cells in the current generation. If this does not keep you entertained, then simply press 'r' to completly randomise the current rule. Have fun! ;)

### Game of Life


