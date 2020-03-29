"""
Draw a grid fractal trees

Based on 'Recursive Tree' example by Daniel Shiffman.
"""

add_library('svg')

cell_size = 150 # grid cell size, px
n_cells = 6 # number of cols and rows 
angle_step = 90 / n_cells
branch_color = 20
left_color = '#ca3617'
center_color = '#009431'
right_color = '#edaf14'

has_leaves = True

def setup():
    size(n_cells * cell_size + cell_size,
         n_cells * cell_size + cell_size, SVG, 'fractal_trees_color.svg')
    background(255)
    stroke(branch_color)


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
    elif has_leaves:
        draw_leaf(h, left_angle, right_angle)


def draw_leaf(h, left_angle, right_angle):
    strokeWeight(0.3)
    stroke(50)
    
    # leaf's color depends on where the tree is in the grid:
    # on the main diagonal - center_color
    # in the top right corner - right_color
    # in the bottom left corner - left_color
    # anywhere in between - the color is interpolated between 
    #                       the main diagonal and one of the corners
    
    # calculate distance to the grid's main diagonal 
    row = left_angle / angle_step
    col = right_angle / angle_step
    
    v1 = PVector(row, col)
    v2 = PVector(col, row)
    v3 = (v1 - v2) / 2
    
    delta = v3.mag() / PVector(n_cells, n_cells).mag() * 5 
    
    if left_angle > right_angle:
        c = lerpColor(center_color, left_color, delta)
    elif left_angle < right_angle:
        c = lerpColor(center_color, right_color, delta)
    else:
        c = center_color
    fill(c);
    circle(0, -h/2, 2.5*h)
    
    strokeWeight(1)
    stroke(branch_color)
