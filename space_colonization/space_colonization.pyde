"""
Draw tree like structures using Space Colonization algorithm

https://www.youtube.com/watch?v=kKT0v3qhIQY
https://medium.com/@jason.webb/space-colonization-algorithm-in-javascript-6f683b743dc5
"""
add_library('svg')

leaf_prob = 0.01 # ratio of non-white pixels that are converted to leaves

max_dist = 50 # max distance between a leaf and a branch such that the branch is influenced by the leaf 
min_dist = 4 # min distance between a leaf and a branch such when reached the leaf become 'consumed'
branch_len = 3
tree = None

class Leaf:
    def __init__(self, pos):
        self.pos = pos # position
        self.reached = False # whether a branch has reached this leaf's min_dist
        
    def draw(self):
        if not self.reached:
            point(self.pos.x, self.pos.y)

class Branch:
    def __init__(self, parent, pos, dir):
        self.parent = parent
        self.n_children = 0
        self.pos = pos # position
        self.dir = dir.copy().normalize() # direction
        self.attractors = [] # leafs that the branch is attracted to
        
    def grow(self):
        if len(self.attractors) == 0:
            return None

        new_dir = self.dir.copy()
        for a in self.attractors:
            attr_dir = PVector.sub(a.pos, self.pos)
            # not normalizing 'attr_dir' helps bias the tree towards
            # areas of more leaves 
            # attr_dir.normalize()
            new_dir.add(attr_dir)
        # new_dir.add(PVector(random(-0.01, 0.01), random(-0.01, 0.01)))
        new_dir.normalize()
        new_dir.mult(branch_len)

        self.attractors = []
        
        new_pos = PVector.add(self.pos, new_dir)
        new_branch = Branch(self, new_pos, new_dir)
        
        # sometimes a branch gets stuck between 2 equidistant leaves.
        # Break the tie by adding noise
        dp = new_branch.dir.dot(self.dir)
        if abs(1-dp) < 0.002:
            random_offset = PVector(random(-0.2, 0.2), random(-0.2, 0.2))
            new_branch.pos.add(random_offset)
        return new_branch
    
    def add_attractor(self, leaf):
        self.attractors.append(leaf)
    
    def draw(self):
        if self.parent is not None:
            weight = map(log(1 + self.n_children), 0, 3, 0.5, 1.5)
            strokeWeight(weight)
            line(self.pos.x, self.pos.y, self.parent.pos.x, self.parent.pos.y)


class Tree:
    def __init__(self, root, leaves):
        self.leaves = leaves
        self.active_branches = [root] # branches that are still growing
        self.passive_branches = [] # branches that stopped growing
        
        # inital growth
        reached = False
        while not reached:
            branch = self.active_branches[-1]
            for l in self.leaves:
                d = PVector.dist(l.pos, branch.pos)
                if d < min_dist:
                    reached = True
                    break

            if not reached:
                # add a temp attractor to let the branch grow 
                branch.add_attractor(Leaf(PVector.add(branch.pos, branch.dir)))
                new_branch = branch.grow()
                self.active_branches.append(new_branch)

    
    def grow(self):
        # for each leaf find the closest branch within max_dist
        for l in self.leaves:
            curr_dist = None
            closest_branch = None
            for b in self.active_branches:
                d = PVector.dist(l.pos, b.pos)
                if d < min_dist:
                    l.reached = True
                
                if curr_dist is None or curr_dist > d:
                    curr_dist = d
                    closest_branch = b
            
            if closest_branch is not None and curr_dist < max_dist:
                closest_branch.add_attractor(l)
        
        # grow active branches
        new_active_branches = []
        for b in self.active_branches:
            new_branch = b.grow()
            if new_branch is not None:
                new_active_branches.append(b)
                new_active_branches.append(new_branch)
            else:
                self.passive_branches.append(b)
        self.active_branches = new_active_branches
        
        # remove reached leaves
        remain_leaves = []
        for l in self.leaves:
            if not l.reached:
                remain_leaves.append(l)
        self.leaves = remain_leaves
        print('n_leaves = %d  n_active = %d  n_passive = %d' 
              % (len(self.leaves), len(self.active_branches), len(self.passive_branches)))


    def update_passive_counts(self):
        children_map = {}
        
        for b in self.passive_branches:
            b.n_childrens = 0

        for b in self.passive_branches:
            parent = b.parent
            while parent is not None:
                parent.n_children += 1
                if parent.parent is None:
                    root = parent

                parent = parent.parent
        # assert len(self.passive_branches) == root.n_children + 1


    def draw(self, leaves=False, branches=True):
        if leaves:
            for l in self.leaves:
                strokeWeight(2)
                stroke(0)
                l.draw()
        
        if branches:
            strokeWeight(1)
            for b in self.passive_branches:
                stroke(0)
                b.draw()
            for b in self.active_branches:
                stroke(255, 0, 0)
                b.draw()


def create_leaves_random():
    leaves = []
    for _ in range(n_leaves):
        leaf = Leaf(PVector(random(width), random(height-100)))
        leaves.append(leaf)
    return leaves


def create_leaves_from_image():
    img = loadImage('maple_leaf.png')
    img.loadPixels()

    leaves = []
    for y in range(img.height):
        for x in range(img.width):
            i = x + y * img.width
            if red(img.pixels[i]) < 255:
                if random(1) < leaf_prob:
                    xl = map(x, 0, img.width, 0, width)
                    yl = map(y, 0, img.height, 0, height)
                    leaves.append(Leaf(PVector(xl, yl)))
    return leaves


def setup():
    global tree
    size(500, 500)
    background(255)

    randomSeed(43)
    
    leaves = create_leaves_from_image()
    
    root = Branch(parent=None,
                  pos=PVector(width/2, height),
                  dir=PVector(0, -1))
    tree = Tree(root, leaves)

    
def draw():
    if len(tree.active_branches) == 0:
        noLoop()
        # tree.update_passive_counts()
        beginRecord(SVG, "maple_leaf.svg")
        tree.draw(leaves=True, branches=True)
        endRecord()
        print('finished')
        return

    background(255)
    tree.grow()
    tree.update_passive_counts()
    tree.draw(leaves=True, branches=True)

    # enable to save frames to generate gif
    # saveFrame("frame-######.png")
    
def keyPressed():
    if key == 'p':
        print('stopping the loop')
        noLoop()
