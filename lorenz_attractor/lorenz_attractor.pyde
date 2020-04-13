# Based on https://www.youtube.com/watch?v=f0lkz2gSsIk
#  https://en.wikipedia.org/wiki/Lorenz_system

add_library('peasycam')
add_library('svg')

x = 0.0001
y = 0.0
z = 0.0

a = 10.0; # sigma
b = 28.; # rho
c = 8/3.0; # beta

points = []

record = False

def setup():
    size(600, 600, P3D)
    
    cam = PeasyCam(this, 500)
    # cam.setMinimumDistance(50)
    # cam.setMaximumDistance(300)
    # cam.setYawRotationMode()
    
def draw():
    global y, x, z, record

    dt = 0.005
    dx = (a * (y - x)) * dt
    dy = (x * (b - z) - y) * dt
    dz = (x * y - c * z) * dt
    
    x = x + dx
    y = y + dy
    z = z + dz
    points.append(PVector(x, y, z))

    if record:
        print('saving...')
        beginRaw(SVG, "lorenz.svg");
    
    background(255); 
    stroke(50)
    
    noFill()
    translate(0, 0, -80)
    scale(4)
    
    strokeWeight(1)
    point(points[0].x, points[0].y, points[0].z)
    point(points[-1].x, points[-1].y, points[-1].z)

    strokeWeight(0.3)
    beginShape()
    for i, p in enumerate(points):            
        vertex(p.x, p.y, p.z)
    endShape()
    
    if record:
        endRaw()
        record = False
    

def keyPressed():
    global record
    if key == 's':
        record = True
