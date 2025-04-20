import math
import random
import pygame as pg

def align(rects, **kwargs):
    """
    Taken pairwise, set the attribute of the second rect to an attribute of the first.
    e.g.: align(iter_of_rects, left='right') to set the `left` attr of each second rect 
    to the `right` attr of each first.
    """
    for r1, r2 in zip(rects[:-1], rects[1:]):
        for k2, k1 in kwargs.items():
            setattr(r2, k2, getattr(r1, k1))

def wrap(rects):
    """Get the bounding rectangle that contains all given rectangles."""
    if not rects:
        return pg.Rect(0, 0, 0, 0)
    
    attrs = ((rect.left, rect.top, rect.right, rect.bottom) for rect in rects)
    lefts, tops, rights, bottoms = zip(*attrs)
    left, top, right, bottom = min(lefts), min(tops), max(rights), max(bottoms)
    return pg.Rect(left, top, right - left, bottom - top)

def randomxy(inside):
    """Get random x,y coordinates inside the given rectangle."""
    x = random.randint(inside.left, inside.right)
    y = random.randint(inside.top, inside.bottom)
    return (x, y)

def randomresolve(rect, inside, rects):
    """Randomly position rect inside the given area without colliding with other rects."""
    while any(rect.colliderect(r) for r in rects):
        rect.topleft = randomxy(inside)

def sprite2particles(sprite, alphathreshold=0, center=None, accel=None):
    """Convert a sprite into particle effects."""
    if center is None:
        center = sprite.rect.center
    centerx, centery = center
    if accel is None:
        accel = (.005, .005)
    accelx, accely = accel
    particles = []
    for y in range(sprite.image.get_height()):
        for x in range(sprite.image.get_width()):
            color = sprite.image.get_at((x,y))
            if color.hsva[3] > alphathreshold:
                from Models.particle import Particle
                p = Particle(color=color)
                p.x = sprite.rect.x + x
                p.y = sprite.rect.y + y
                dx = centerx - p.x
                dy = centery - p.y
                distance = math.hypot(dx, dy)
                angle = math.atan2(dy, dx)
                p.ax = math.cos(angle) * -distance * accelx
                p.ay = math.sin(angle) * -distance * accely
                particles.append(p)
    return particles 