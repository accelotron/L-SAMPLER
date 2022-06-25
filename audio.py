import pygame as pg
import librosa as li
import os
from model import ModelWrapper
import soundfile as sf


class PianoSounds:
    def __init__(self, path_save, model_path, sr, init_path_1=None, init_path_2=None):
        self.model = ModelWrapper(model_path)

        self.sr = sr
        self.path_save = path_save
        if init_path_1 and init_path_2:
            self.sounds = self.generate_sounds(init_path_1, init_path_2)

    def generate_sounds(self, path_1, path_2):
        root_note = self.model.mash_two(path_1, path_2)
        pitch_shifts = [p for p in range(-12, 12)]

        raw = []
        res = []

        for p in pitch_shifts:
            raw.append(li.effects.pitch_shift(root_note, self.sr, float(p)))

        for i in range(0, 24):
            p = os.path.join(self.path_save, str(i) + ".wav")
            sf.write(os.path.join(self.path_save, str(i) + ".wav"), raw[i], self.sr)
            res.append(pg.mixer.Sound(p))

        return res

    def sound_play(self, kid):
        self.sounds[kid].play()


if __name__ == '__main__':
    pg.init()
    pg.mixer.init(frequency=16000)

    ps = PianoSounds(
        os.path.join('samples', 'flute_acoustic_028-048-127.wav'),
        os.path.join('samples', 'organ_electronic_067-048-127.wav'),
        'piano_cache',
        'rave_nsynth.ts',
        16000)

