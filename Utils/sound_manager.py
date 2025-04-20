import pygame as pg
from pathlib import Path


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self._load_sounds()
        
    def _load_sounds(self):
        """Load all sound effects"""
        sounds_dir = Path("assets/sounds")
        if sounds_dir.exists():
            # Support both .wav and .mp3 files
            for sound_file in sounds_dir.glob("*.[wm][ap][v3]"):
                try:
                    self.sounds[sound_file.stem] = pg.mixer.Sound(str(sound_file))
                except pg.error:
                    print(f"ไม่สามารถโหลดไฟล์เสียง {sound_file} ได้")
                    print("หากเป็นไฟล์ .mp3 กรุณาแปลงเป็น .wav ก่อน")
    
    def play_typing_sound(self):
        """Play typing sound effect"""
        if "typing" in self.sounds:
            self.sounds["typing"].play()
            
    def play_error_sound(self):
        """Play error sound when wrong key is pressed"""
        if "error" in self.sounds:
            self.sounds["error"].play() 