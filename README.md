# Life_Simulators

## Final Project Python Course

This project is the culmination of what I have been able to learn during a beginner python course. It features three cellular automata, as well as a popular simulation called Particle Life. Each of these simulations shows how complex, nature-like structures can emerge from a simple, deterministic set of rules. What I think is especially interesting is how unpredictable these systems can prove to be, and I have really enjoyed interacting with the digital 'creatures' that have popped up on my screen. For this reason, I have attempted to make these simulations as interactive as possible, and I encourage you to not just watch, but play around with them as well.

## requirements

This programme makes use of the following libraries:

1) [Pygame](https://pypi.org/project/pygame/)
2) [NumPy](https://numpy.org/)
3) [quads](https://pypi.org/project/quads/)

As long as these three libraries have been installed, you can run the programme by simply running the file called 'main.py'

## how to use

### Main Menu

when running the programme, you should find yourself in the main menu. Here you can navigate between the four different simulations, as well as exit the programme using the quit button or the 'escape' key. Here, it is also possible to change the colour scheme of the programme. You can enter dark mode with a secret button hidden in the top right corner of the screen, or you can press 'R' to be surprised with a completely random set of colours.

### Elementary Cellular Automata

The first cellular automaton is the set of [*ECA's*](https://mathworld.wolfram.com/ElementaryCellularAutomaton.html) explored by Stephen Wolfram in his book '*A New Kind of Science*'. You should be met with a screen containing seven different input boxes. You can click on these boxes to alter the configuration of the CA by typing in them.

The rule is what determines how a certain generation will evolve over time. It should be an integer between 0 and 255, which can be entered in either binary or decimal.

The size refers to the width and height of each cell in pixels. It can be any integer between five and a hundred. Do note that the size directly affects the amount of cells that make up a generation.

The start indices are the cells that will be turned on in the first generation. It can either be a single integer or a list of them, as long as they do not exceed the number of cells in a generation (the programme will tell you if a certain index is out of bounds). Furthermore, it is possible to enter 'middle' to turn on only the middle cell, or 'empty' to turn on no cells at all.

Then there is the boundary condition. This describes what happens at the edges of the grid, since unfortunately it is not infinite (yet). Currently, four different boundary conditions are supported:

1) 'periodic' - the grid wraps around to connect to itself.
2) 'Dirichlet 0' - the edges are always zero.
3) 'Dirichlet 1' - the edges are always one.
4) 'Neumann' - the edges share the state of their neighbour.

Finally there are the colours. These should be RGB-triples, meaning tuples of length three with integers between 0 and 255. It is also possible to enter any named Pygame colour out of this [list](https://www.pygame.org/docs/ref/color_list.html).

As an added bonus, if you feel like spicing up the cellular experience, each box also allows you to input 'random', which will randomise that part of the configuration each run. If you are feeling truly adventurous, then you might be tempted to try out the secret **mystery box!!!** mode, which can be accessed through a secret button hidden in the top right corner of the screen.

As the simulation is running, it is possible to interact with it in three ways. You can pause and unpause the simulation with the 'space' key. Additionally, You can click (or hold) the left mousebutton anywhere on the screen to toggle on/off cells in the current generation. If this does not keep you entertained, then simply press 'R' to completly randomise the current rule. To exit simply press 'escape'.

### Game of Life

The next cellular automaton is the tremendously famous '[*Game of Life*](https://conwaylife.com/wiki/Conway%27s_Game_of_Life)', designed by John Conway. You should again see seven input boxes you can alter to your heart's content. We will briefly run through them again.

The rule is a tuple this time, containing integers between 0 and 9. The first two digits make up the interval of how many live neighbours a cell should have in order to survive. Since it is an interval, the second digit should be greater than- or equal to the first. The last digit says how many live neighbours a cell needs in order for it to be born.

The size, boundary condition and colours are the exact same as before. I highly recommend trying out the boundary condition: 'Dirichlet 1', and leaving the grid empty.

Of course it is still possible to enter 'random' in all the boxes, and for the especially brave, there is always the **mystery box!!!**

When you run the simulation, it will start off in it's paused state. Here you can use the left mousebutton to turn on cells and the right mousebutton if you would like to turn some off again. Pressing space will then unpause the simulation and turn whatever lovely drawing you have made into a lively spectacle. Note that it is still possible to draw, and thus interact with the simulation in it's unpaused state. Finally, you can press the 'R' key to populate a great portion of the grid with fresh, new life. To exit, simply press 'escape'.

### Particle Life

Probably my favourite out of the four. [*Particle Life*](https://www.youtube.com/watch?app=desktop&v=p4YirERTVF0) is a simulation based on the work of Jeffrey Ventrella. It simulates different groups of particles (represented by their colour), which excert forces on each other. these forces are characterised by a sort of 'gravitational constant', which determines how much a certain group attracts, or repels another group. We can represent the relations between all groups with a matrix, where each element is such a gravitational constant. In the input screen, the elements of this matrix are visualised using colour. Green means a positive force, meaning an attraction, and red means a negative force, or repulsion. You can alter the elements of the matrix by hovering over them with the mouse and then holding the left mousebutton to increase- or the right mousebutton to decrease them. There are also three buttons next to the matrix. The '**+**' button adds a new group, the '**-**' button removes one, and the '**RND**' button randomises the elements of the matrix while keeping it's shape.

Of course there are also more input boxes to toy around with.
The number of particles determines how many particles will be created overall. It can be any integer greater than zero, though, I would not go too crazy since the entire thing runs on the CPU.

The size determine the radius of each particle in pixels. It can again be any integer greater than zero.

The range determines the maximum distance at which two particles affect one another. It can be any float between zero and one, where a range of one means the entire screen. 

Lastly, there is the force factor, which is used to scale each force. Thus, a greater forcefactor means particles will excert much greater forces on each other. It can be any integer greater than zero.

I also want to mention that it is possible to adjust the dt (change in time), however, I recommend only touching this if particles are constantly oscillating like crazy.

At this point I probably don't have to mention it anymore, but do try out the **mystery box!!!**

As the simulation is running, you can again pause and unpause using the 'space' key. You can also attract particles towards your mouse using the left mousebutton, as well as push them away from you with the right mousebutton. If the current configuration starts to bore you, just press the 'R' key to randomise the elements of the matrix, completely changing the behaviour of all particles on the screen. To exit, simply press 'escape'.

### Smooth Life

Last but not least is a cellular autamaton called '[*Smooth Life*](https://arxiv.org/abs/1111.1567)'. It was created by Stephan Rafler and was meant to generalise Conway's game of life to a continuous domain. This means each pixel now holds a state that can be any floating point number between 0 and 1, and a 'cell' is now viewed as a dense region of 'healthy' pixels. How this CA is implemented was (and still is honestly) quite hard to wrap my head around, so most of the credit here actually goes to [duckythescientist](https://github.com/duckythescientist/SmoothLife), whose incredible python implementation I used as a framework to build mine around.

In the input screen you are again met with seven input boxes. We'll briefly run through them one last time. The sigmoidmode and stepmode are combined into the modes box. The sigmoidmode refers to how we calculate the state of each pixel at the next timestep. the stepmode refers to how we transition to this next state over time. The modes should be entered as a tuple of two integers, where the sigmoid modes are labeled one through four and the stepmodes zero through four.

Then there are the types. These determine what type of smoothstep functions we use when we apply the sigmoidmode to calculate the next state for each pixel. There are two different types, each with three different options, labeled zero, one and four. These should again be entered in a tuple.

Next is the size. This, unsurprisingly, refers to the size of each 'pixel' in real pixels. It can be any integer between five and twenty.

The outer radius is what determines the size of a cell. there are two radii, an inner and outer one. When determining the new state of a pixel, all the other pixels within the inner radius are considered as the cells own state, while all the pixels that are in the outer radius but not the inner one (that is the annulus) are considered the neighbourhood of that cell. By default, the inner radius is a third of the given outer radius. The outer radius can be any float between five and fifty.

Now for the birth and death intervals. These are used together with the sigmoid mode to create thresholds between which the next state of each pixel is interpolated. Because they are intervals, obviously the second number in each pair should be greater than the first. Besides that, all numbers should be floats between zero and one.

Lastly, There are the sigmoid widths. These are two floats that are used to define (some of) the different smoothstep functions used to calctulate the next state of each pixel. The widths are again combined into a tuple. The first should be between 0 and 0.2, since you really would not want it to be greater than that, and the second should be between zero and one.

Of course none of this actually matters since I know you are going to be using the **mystery box!!!**

When you run the simulation, nothing will happen. This is because, similarly to *Game of Life*, You have to create the cells yourself by drawing them with the left mousebutton. In the default configuration, a cell will die if it is stationary. Therefore, try holding the left mousebutton and gently moving it around, and watch what happens. Of course you can also press 'R', which will automatically fill the screen with a population of live cells. To exit, simply press 'escape'.

Have fun! ;)

## references

The following videos inspired a lot of the fundamental ideas and concepts behind my code:

1) [Elementary Cellular Automata - The Coding Train](https://www.youtube.com/watch?v=W1zKu3fDQR8)
2) [Game of Life - NeuralNine](https://www.youtube.com/watch?v=cRWg2SWuXtM)
3) [Particle Life - Tom Mohr](https://www.youtube.com/watch?v=scvuli-zcRc)
4) [Smooth Life - duckythescientist](https://github.com/duckythescientist/SmoothLife)
5) [Button - Coding with Russ](https://www.youtube.com/watch?v=jyrP0dDGqgY)