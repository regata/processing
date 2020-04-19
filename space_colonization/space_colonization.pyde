"""
Draw tree like structures using Space Colonization algorithm

https://www.youtube.com/watch?v=kKT0v3qhIQY
https://medium.com/@jason.webb/space-colonization-algorithm-in-javascript-6f683b743dc5
"""
add_library('svg')

n_leaves = 1000

max_dist = 300
min_dist = 5

class Leaf:
    def __init__(self, pos):
        self.pos = pos # position
        self.reached = False # whether a branch has reached this leaf's min_dist
        
    def draw(self):
        if not self.reached:
            strokeWeight(1.5)
            point(self.pos.x, self.pos.y)

class Branch:
    def __init__(self, parent, pos, dir):
        self.parent = parent
        self.pos = pos # position
        self.dir = dir.copy().normalize() # direction
        self.attractors = [] # leafs that the branch is attracted to
        
    def grow(self, rate=5):
        if len(self.attractors) == 0:
            return None

        new_dir = self.dir.copy()
        for a in self.attractors:
            attr_dir = PVector.sub(a.pos, self.pos)
            attr_dir.normalize()
            new_dir.add(attr_dir)
        
        new_dir.normalize()
        new_dir.mult(rate)
            
        self.attractors = []
        
        new_pos = PVector.add(self.pos, new_dir)
        new_branch = Branch(self, new_pos, new_dir)
        return new_branch
    
    def add_attractor(self, leaf):
        self.attractors.append(leaf)
    
    def draw(self):
        strokeWeight(1)
        if self.parent is not None:
            line(self.pos.x, self.pos.y, self.parent.pos.x, self.parent.pos.y)


class Tree:
    def __init__(self, root, leaves):
        self.leaves = leaves
        self.branches = [root]
        
        # inital growth
        reached = False
        while not reached:
            branch = self.branches[-1]
            for l in self.leaves:
                d = PVector.dist(l.pos, branch.pos)
                if d < min_dist:
                    reached = True
                    break

            if not reached:
                branch.add_attractor(Leaf(PVector.add(branch.pos, branch.dir)))
                new_branch = branch.grow()
                self.branches.append(new_branch)

    
    def grow(self):
        # for each leaf find the closest branch within max_dist
        for l in self.leaves:
            if l.reached:
                continue
            curr_dist = None
            closest_branch = None
            for b in self.branches:
                d = PVector.dist(l.pos, b.pos)
                if d < min_dist:
                    l.reached = True
                
                if curr_dist is None or curr_dist > d:
                    curr_dist = d
                    closes_branch = b
            
            if closes_branch is not None and d < max_dist:
                closes_branch.add_attractor(l)
        
        for b in self.branches:
            new_branch = b.grow()
            if new_branch is not None:
                self.branches.append(new_branch)
        
        remain_leaves = []
        for l in self.leaves:
            if not l.reached:
                remain_leaves.append(l)
        self.leaves = remain_leaves
        print('n_leaves = %d  n_branches = %d' % (len(self.leaves), len(self.branches)))
        

    def draw(self, leaves=False, branches=True):
        if leaves:
            for l in self.leaves:
                l.draw()
        
        if branches:
            for b in self.branches:
                b.draw()


tree = None

def setup():
    global tree
    size(500, 500)
    background(255)
    
    randomSeed(42)
    
    leaves = []
    for _ in range(n_leaves):
        leaf = Leaf(PVector(random(width), random(height-100)))
        leaves.append(leaf)
    
    root = Branch(parent=None,
                  pos=PVector(width/2, height),
                  dir=PVector(0, -1))
    tree = Tree(root, leaves)
    
    # noLoop()
    
def draw():
    background(255)
    tree.grow()
    tree.draw(leaves=True, branches=True)    
    # print('finished')
