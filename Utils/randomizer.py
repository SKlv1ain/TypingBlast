import random

def randomxy(inside):
    x = random.randint(inside.left, inside.right)
    y = random.randint(inside.top, inside.bottom)
    return (x, y)

def randomresolve(rect, inside, others):
    while any(rect.colliderect(r) for r in others):
        rect.topleft = randomxy(inside)