#! /usr/bin/env python3
import random
import vector
import processing

################################################################################

# QVGA Resolution
WIDTH = 320
HEIGHT = 240

################################################################################

class Demonstration(processing.Process):

    MAX_SPEED = 60.0
    MAX_FORCE = 1.0
    BACKGROUND = '#000'
    SCHOOLS = (('#F00', '#0FF'),
               ('#0F0', '#F0F'),
               ('#00F', '#FF0'),
               ('#0FF', '#F00'),
               ('#F0F', '#0F0'),
               ('#FF0', '#00F'))

    def setup(self):
        self.display(WIDTH, HEIGHT, self.BACKGROUND)
        self.__adding = 0
        self.__schools = []
        for stroke, fill in self.SCHOOLS:
            self.__schools.append(School(stroke, fill))
            self.__schools[-1].center = vector.Vector2(random.randrange(WIDTH),
                                                       random.randrange(HEIGHT))
            
    def render(self, context):
        if self.__adding != -1:
            school = self.__schools[self.__adding]
            boid = Boid(school.center.copy(), self.MAX_SPEED, self.MAX_FORCE)
            school.add_boid(boid)
            self.__adding = (self.__adding + 1) % len(self.__schools)
        boids = 0
        for school in self.__schools:
            school.render(context)
            boids += len(school)
        context.render()
        context.write(10, 10, boids, '#FFF')

    def update(self, interval):
        for school in self.__schools:
            school.update(interval)

    def mouse_pressed(self, event):
        boid = Boid(vector.Vector2(event.x, event.y),
                    self.MAX_SPEED, self.MAX_FORCE)
        random.choice(self.__schools).add_boid(boid)

    def speed_warning(self):
        random.choice(self.__schools).remove_boid()
        self.__adding = -1

################################################################################

class Boid:

    SIZE = 3.0

    SEP_FACTOR = 1.5
    ALI_FACTOR = 1.0
    COH_FACTOR = 1.0

    DESIRED_SEPARATION = 20.0
    NEIGHBOR_DISTANCE = 30.0

    SHAPE = processing.Shape()
    SHAPE.vertex(SIZE * 2, 0)
    SHAPE.vertex(SIZE * -2, SIZE)
    SHAPE.vertex(SIZE * -2, -SIZE)

    ########################################################################

    def __init__(self, location, max_speed, max_force):
        self.__loc = location
        self.__vel = vector.Polar2(random.randint(1, 20), random.randrange(360))
        self.__acc = vector.Vector2(0, 0)
        self.__max_speed = max_speed
        self.__max_force = max_force
        # Calculate Constants
        size = self.SIZE
        self.__neg_size = -size
        self.__width_size = WIDTH + size
        self.__height_size = HEIGHT + size
        # Create Shape
        self.__shape = self.SHAPE.ngon_copy()

    def set_colors(self, stroke, fill):
        self.__shape.stroke(stroke)
        self.__shape.fill(fill)

    def update(self, boids, interval):
        self.school(boids)
        self.move(interval)
        self.borders()

    ########################################################################

    def school(self, boids):
        self_loc, self_acc = self.__loc, self.__acc
        sep = vector.Vector2(0, 0)
        ali = vector.Vector2(0, 0)
        coh = vector.Vector2(0, 0)
        separation = False
        neighbor = 0
        for other in boids:
            if other is not self:
                other_loc = other.__loc
                diff = self_loc - other_loc
                dist = diff.magnitude
                if dist < self.DESIRED_SEPARATION:
                    sep += diff.normalize() / dist
                    separation = True
                if dist < self.NEIGHBOR_DISTANCE:
                    ali += other.__vel
                    coh += other_loc
                    neighbor += 1
        if separation:
            self_acc += self.steer(sep) * self.SEP_FACTOR
        if neighbor:
            self_acc += self.steer(ali) * self.ALI_FACTOR + \
                        self.steer(coh / neighbor - self_loc) * self.COH_FACTOR

    def move(self, interval):
        vel, acc = self.__vel, self.__acc
        vel += acc
        self.__loc += vel.limit(self.__max_speed) * interval
        acc.xy = 0, 0

    def borders(self):
        loc, neg_size, width_size, height_size = \
             self.__loc, self.__neg_size, self.__width_size, self.__height_size
        x, y = loc.x, loc.y
        if x < neg_size:
            loc.x = width_size
        if y < neg_size:
            loc.y = height_size
        if x > width_size:
            loc.x = neg_size
        if y > height_size:
            loc.y = neg_size

    def render(self, context):
        context.push_matrix()
        context.push_shape(self.__shape)
        context.rotate(self.__vel.direction)
        context.translate(self.__loc)

    ########################################################################

    def steer(self, target):
        target.magnitude = self.__max_speed
        return (target - self.__vel).limit(self.__max_force)

################################################################################

class School:

    def __init__(self, stroke='', fill=''):
        self.__stroke = stroke
        self.__fill = fill
        self.__boids = []

    def __len__(self):
        return len(self.__boids)

    def render(self, context):
        for boid in self.__boids:
            boid.render(context)

    def update(self, interval):
        boids = self.__boids
        for boid in boids:
            boid.update(boids, interval)

    def add_boid(self, boid):
        boid.set_colors(self.__stroke, self.__fill)
        self.__boids.append(boid)

    def remove_boid(self):
        self.__boids = self.__boids[1:]

################################################################################

import recipe576904; recipe576904.bind_all(globals())
        
################################################################################

if __name__ == '__main__':
    Demonstration.main()
