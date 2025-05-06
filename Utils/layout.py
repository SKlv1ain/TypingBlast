import math
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
