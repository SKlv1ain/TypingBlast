import random
import pygame as pg
from pygame import Rect

from Models.word import Word
from Models.bullet import Bullet
from Models.game_stats import GameStats

from Views.dashboard_view import DashboardView
from Views.wave_view import WaveView

from Utils.wordspawner import WordSpawner
from Utils.sound_manager import SoundManager

class GameController:
    def __init__(self, renderer, rocket_pos=(400, 500), nwords=5):
        self.renderer = renderer

        self.hits = 0
        self.max_hits = 3
        self.is_game_over = False
        
        self.wave_delay = 60
        self.wave_timer = 0
        
        self.wave_message_timer = 0
        self.wave_font = pg.font.Font(None, 64)


        self.words = []
        self.locked_word = None
        self.nwords = nwords
        self.last_wave_words_destroyed = 0

        self.rocket_pos = rocket_pos
        self.bullets = pg.sprite.Group()

        self.sound_manager = SoundManager()
        self.word_list = []
        
        self.stats = GameStats()
        self.calculate_wave_parameters()

        
        self.dashboard = DashboardView(renderer.screen)
        self.wave_view = WaveView()

        self.load_words()
        
    def calculate_wave_parameters(self):
        wave = self.stats.get_wave()
        
        self.nwords = min(1 + wave, 12)  
        self.word_speed = min(1.5 + 0.2 * (wave - 1), 4.0) 

        print(f"[Wave {wave}] max words: {self.nwords}, word speed: {self.word_speed}")


    def load_words(self, path='/usr/share/dict/words'):
        with open(path) as f:
            words = [w.strip() for w in f if 4 <= len(w.strip()) <= 6 and w.strip().isalpha()]
        random.shuffle(words)
        self.word_list = words

    def spawn_word(self):
        while True:
            letters = random.choice(self.word_list)
            if not any(word.letters == letters for word in self.words):
                break

        word = Word(letters, self.rocket_pos, speed=self.word_speed)
        WordSpawner.place_word(word, self.words)
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
                    
            if (
                self.stats.words_destroyed > 0 and  # only check if at least one word has been destroyed
                self.stats.words_destroyed % 10 == 0 and 
                self.stats.words_destroyed != self.last_wave_words_destroyed
            ):
                self.wave_timer += 1
                if self.wave_timer >= self.wave_delay:
                    self.stats.next_wave()
                    self.last_wave_words_destroyed = self.stats.words_destroyed  
                    self.calculate_wave_parameters()
                    self.wave_timer = 0
                    self.sound_manager.play_wave_sound()
                    self.wave_view.trigger()


        if self.hits >= self.max_hits:
            if not self.is_game_over:
                self.sound_manager.play_game_over_sound()
            self.is_game_over = True

        self.bullets.update()
        self.words = [w for w in self.words if w.is_alive()]
        self.renderer.update()
        self.dashboard.draw(self.stats.export())
        
        self.wave_view.draw(self.renderer.screen.image, self.stats.get_wave())



    def is_over(self):
        return self.is_game_over

    def get_final_stats(self):
        return self.stats.export()
