import pygame as pg
from Utils.randomizer import randomxy, randomresolve

class WordSpawner:
    @staticmethod
    def place_word(word, existing_words):
        rect = word.rect()
        spawn_area = pg.Rect(100, -4 * rect.height, 800 - 100 - rect.width, rect.height)
        rect.topleft = randomxy(spawn_area)
        randomresolve(rect, spawn_area, [w.rect() for w in existing_words])
        word.sprites[0].rect.topleft = rect.topleft
        word.y = word.sprites[0].rect.y
        word.align()
