import librosa as li
import pygame as pg
import numpy as np


class PianoSounds:
    def __init__(self, root, sr):
        self.root = root
        self.sr = sr
        self.pg_sounds = []

        for i in range(-5, 7):
            note_sound = (li.effects.pitch_shift(root, 16000, float(i))*32768).astype(np.int16)
            note_sound = np.repeat(note_sound[:, np.newaxis], 2, axis=1).reshape([note_sound.shape[0], 2])
            self.pg_sounds.append(pg.sndarray.make_sound(note_sound))

    def play_sound(self, note_id):
        pg.mixer.stop()
        self.pg_sounds[note_id].play()


if __name__ == "__main__":
    import os
    import time

    pg.mixer.init(frequency=16000, channels=1)

    sound = li.load(os.path.join('samples', 'keyboard_synthetic_000-048-127.wav'), sr=16000)[0]
    piano_sounds = PianoSounds(sound, 16000)

    for k in range(12):
        piano_sounds.play_sound(k)
        time.sleep(1)
