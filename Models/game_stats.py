import time

class GameStats:
    def __init__(self):
        self.reset()

    def reset(self):
        self.start_time = None
        self.correct_keystrokes = 0
        self.incorrect_keystrokes = 0
        self.words_destroyed = 0
        self.max_combo = 0
        self.current_combo = 0
        self.wave = 1

    def start_timer(self):
        if self.start_time is None:
            self.start_time = time.time()

    def record_correct(self):
        self.correct_keystrokes += 1
        self.current_combo += 1
        self.max_combo = max(self.max_combo, self.current_combo)

    def record_incorrect(self):
        self.incorrect_keystrokes += 1
        self.current_combo = 0

    def record_word_destroyed(self):
        self.words_destroyed += 1
        
    def next_wave(self):
        self.wave += 1

    def get_wave(self):
        return self.wave

    def calculate_wpm(self):
        if not self.start_time:
            return 0
        elapsed_minutes = (time.time() - self.start_time) / 60
        return (self.correct_keystrokes / 5) / elapsed_minutes

    def calculate_accuracy(self):
        total = self.correct_keystrokes + self.incorrect_keystrokes
        return (self.correct_keystrokes / total) * 100 if total else 100

    def calculate_score(self):
        return int(self.calculate_wpm() * (self.max_combo + 1) + self.words_destroyed * 10)

    def export(self):
        return {
            "WPM": round(self.calculate_wpm(), 2),
            "Accuracy (%)": round(self.calculate_accuracy(), 2),
            "Words Destroyed": self.words_destroyed,
            "Max Combo": self.max_combo,
            "Score": self.calculate_score(),
            "Typing Errors": self.incorrect_keystrokes,
            "Wave": self.wave   
        }
