import random
import pygame as pg

from Models.word import Word
from Models.bullet import Bullet

from Utils.game_utils import randomxy, randomresolve
from Utils.sound_manager import SoundManager


class GameController:
    def __init__(self, renderer):
        self.renderer = renderer
        self.words = []
        self.lock = None
        self.nwords = 3
        self.sound_manager = SoundManager()
        
        # Add rocket
        self.rocket_pos = (400, 500)  # Bottom center position of screen
        
        # Add sprite group for bullets
        self.bullets = pg.sprite.Group()
        
        self.load_words()

    def load_words(self):
        # Load words from dictionary
        with open('/usr/share/dict/words') as f:
            words = [word.strip() for word in f.readlines() 
                    if 4 <= len(word.strip()) <= 6 
                    and set(word.strip()).issubset(set('abcdefghijklmnopqrstuvwxyz'))]
        random.shuffle(words)
        self.word_list = words

    def spawn_word(self):
        while True:
            letters = random.choice(self.word_list)
            taken = any(word.letters == letters for word in self.words)
            if not taken:
                break

        newword = Word(letters, self.rocket_pos)  # Pass rocket position
        rect = newword.rect()
        spawn = pg.Rect(100, -4 * rect.height, 800-100-rect.width, rect.height)
        rect.topleft = randomxy(spawn)
        randomresolve(rect, spawn, [w.rect() for w in self.words])
        newword.sprites[0].rect.topleft = rect.topleft
        newword.y = newword.sprites[0].rect.y
        newword.align()
        
        self.renderer.add_sprites(newword.get_sprites())
        self.words.append(newword)

    def spawn_bullet(self, target_word):
        # Create bullet from rocket to word using correct position
        target_pos = target_word.get_target_position()
        bullet = Bullet(self.rocket_pos, target_pos)
        self.bullets.add(bullet)
        self.renderer.add_sprites([bullet])

    def handle_input(self, letter):
        # If locked word is finished (fully typed), unlock it
        if self.lock and not self.lock.is_alive():
            self.lock = None
        
        # If there's a word currently being typed
        if self.lock:
            if self.lock.shoot(letter):
                self.sound_manager.play_typing_sound()
                # Fire bullet when typed correctly
                self.spawn_bullet(self.lock)
            else:
                # When typed incorrectly, play sound but do not unlock
                self.sound_manager.play_error_sound()
        # If no word is locked yet, find a new one
        elif not self.lock:
            hit = False
            for word in self.words:
                if word.shoot(letter):
                    self.lock = word
                    self.sound_manager.play_typing_sound()
                    # Fire bullet when typed correctly
                    self.spawn_bullet(word)
                    hit = True
                    break
            if not hit:
                self.sound_manager.play_error_sound()

    def update(self):
        if len(self.words) < self.nwords:
            self.spawn_word()
        
        # Update words and check collisions
        for word in self.words:
            word.update()
            # If this word was hit and disappeared
            if not word.is_alive() and word == self.lock:
                self.lock = None  # Unlock to allow typing a new word
        
        # Update bullets
        self.bullets.update()
        
        # Remove dead words
        self.words = [word for word in self.words if word.is_alive()]
        
        # Update renderer
        self.renderer.update()