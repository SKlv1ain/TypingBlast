# === Updated game_controller.py: correct word destroyed count ===
import random
import pygame as pg
from pygame import Rect

from Models.word import Word
from Models.bullet import Bullet
from Models.game_stats import GameStats

from Views.dashboard_view import DashboardView

from Utils.randomizer import randomxy, randomresolve
from Utils.sound_manager import SoundManager

class GameController:
    def __init__(self, renderer, rocket_pos=(400, 500), nwords=3):
        self.renderer = renderer

        self.hits = 0
        self.max_hits = 3
        self.is_game_over = False

        self.words = []
        self.locked_word = None
        self.nwords = nwords

        self.rocket_pos = rocket_pos
        self.bullets = pg.sprite.Group()

        self.sound_manager = SoundManager()
        self.word_list = []
        self.stats = GameStats()
        
        self.dashboard = DashboardView(renderer.screen)


        self.load_words()

    def load_words(self, path='/usr/share/dict/words'):
        with open(path) as f:
            words = [w.strip() for w in f if 4 <= len(w.strip()) <= 6 and w.strip().isalpha()]
        random.shuffle(words)
        self.word_list = words

    def spawn_word(self):
        letters = next(w for w in self.word_list if not any(word.letters == w for word in self.words))
        word = Word(letters, self.rocket_pos)
        rect = word.rect()
        spawn_area = pg.Rect(100, -4 * rect.height, 700, rect.height)
        rect.topleft = randomxy(spawn_area)
        randomresolve(rect, spawn_area, [w.rect() for w in self.words])
        word.sprites[0].rect.topleft = rect.topleft
        word.y = word.sprites[0].rect.y
        word.align()
        self.renderer.add_sprites(word.get_sprites())
        self.words.append(word)

    def spawn_bullet(self, target_word):
        bullet = Bullet(self.rocket_pos, target_word.get_target_position())
        self.bullets.add(bullet)
        self.renderer.add_sprites([bullet])

    def handle_input(self, letter):
        if self.stats.start_time is None:
            self.stats.start_timer()

        if self.locked_word and not self.locked_word.is_alive():
            self.locked_word = None

        if self.locked_word:
            if self.locked_word.shoot(letter):
                self.sound_manager.play_typing_sound()
                self.spawn_bullet(self.locked_word)
                self.stats.record_correct()
            else:
                self.sound_manager.play_error_sound()
                self.stats.record_incorrect()
        else:
            for word in self.words:
                if word.shoot(letter.lower()):
                    self.locked_word = word
                    self.sound_manager.play_typing_sound()
                    self.spawn_bullet(word)
                    self.stats.record_correct()
                    return
            self.sound_manager.play_error_sound()
            self.stats.record_incorrect()

    def update(self):
        if len(self.words) < self.nwords and not self.is_game_over:
            self.spawn_word()

        rocket_rect = Rect(self.rocket_pos[0] - 30, self.rocket_pos[1] - 30, 60, 60)

        for word in self.words:
            word.update()

            if word.rect().colliderect(rocket_rect):
                self.hits += 1
                word.explode()
                if not word.already_destroyed:
                    self.stats.record_word_destroyed()
                if word == self.locked_word:
                    self.locked_word = None

            elif not word.is_alive() and not word.already_destroyed:
                word.already_destroyed = True
                self.stats.record_word_destroyed()
                if word == self.locked_word:
                    self.locked_word = None

        if self.hits >= self.max_hits:
            self.is_game_over = True

        self.bullets.update()
        self.words = [w for w in self.words if w.is_alive()]
        self.renderer.update()
        self.dashboard.draw(self.stats.export()) 

    def is_over(self):
        return self.is_game_over

    def get_final_stats(self):
        return self.stats.export()
