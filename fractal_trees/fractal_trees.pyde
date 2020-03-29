"""
Draw a grid fractal trees

Based on 'Recursive Tree' example by Daniel Shiffman.
"""

add_library('svg')

cell_size = 150 # grid cell size, px
n_cells = 6 # number of cols and rows 
angle_step = 90 / n_cells


def setup():
    size(n_cells * cell_size + cell_size,
         n_cells * cell_size + cell_size, SVG, 'fractal.svg')
    background(255)
    stroke(0)


def draw():
    translate(cell_size / 2, cell_size / 2) # add margin
    for row in range(n_cells):
        with pushMatrix():
            for col in range(n_cells):
                # square(0,0, cell_size)
                draw_tree(init_height=cell_size * 0.3,
                          left_angle=angle_step * (row + 1),
                          right_angle=angle_step * (col + 1))
                translate(cell_size, 0) # move 1 cell right
        translate(0, cell_size) # move 1 row down

    print('finished')
    exit()


def draw_tree(init_height, left_angle, right_angle):
    with pushMatrix():
        # Start the tree from the bottom of the screen
        translate(cell_size / 2, cell_size)
    
        # Draw the first line
        line(0, 0, 0, -init_height)
        # Move to the end of that line
        translate(0, -init_height)
        # Start the recursive branching!
        branch(init_height, left_angle, right_angle)


def branch(h, left_angle, right_angle):
    # Each branch will be 2/3rds the size of the previous one
    h *= 0.66
    # All recursive functions must have an exit condition!!!!
    # Here, ours is when the length of the branch is 2 pixels or less
    if h > 2:
        # Save the current state of transformation (i.e. where are we now)
        pushMatrix()
        rotate(radians(-left_angle))  # Rotate by theta
        line(0, 0, 0, -h)  # Draw the branch
        translate(0, -h)  # Move to the end of the branch
        branch(h, left_angle, right_angle)  # Ok, now call myself to draw two branches!!
        # Whenever we get back here, we "pop" in order to restore the previous
        # matrix state
        popMatrix()
        # Repeat the same thing, only branch off to the "left" this time!
        with pushMatrix():
            rotate(radians(right_angle))
            line(0, 0, 0, -h)
            translate(0, -h)
            branch(h, left_angle, right_angle)
