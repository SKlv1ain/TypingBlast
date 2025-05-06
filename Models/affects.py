import math
from .particle import Particle

def sprite2particles(sprite, alphathreshold=0, center=None, accel=None):
    if center is None:
        center = sprite.rect.center
    accel = accel or (.005, .005)
    centerx, centery = center
    accelx, accely = accel

    particles = []
    for y in range(sprite.image.get_height()):
        for x in range(sprite.image.get_width()):
            color = sprite.image.get_at((x, y))
            if color.hsva[3] > alphathreshold:
                p = Particle(color=color)
                p.x = sprite.rect.x + x
                p.y = sprite.rect.y + y
                dx, dy = centerx - p.x, centery - p.y
                distance = math.hypot(dx, dy)
                angle = math.atan2(dy, dx)
                p.ax = math.cos(angle) * -distance * accelx
                p.ay = math.sin(angle) * -distance * accely
                particles.append(p)
    return particles