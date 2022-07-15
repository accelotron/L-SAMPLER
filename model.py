import torch
import numpy as np
import os
import soundfile as sf
import librosa as li


class ModelWrapperRave:
    def __init__(self, ts_file, sr):
        self.sr = sr
        self.model = torch.jit.load(ts_file)
        self.model.eval()

    def get_latent(self, x):
        x = torch.from_numpy(x).reshape(1, 1, -1).float()
        z = self.model.encode(x)
        return z

    def generate(self, z):
        return self.model.decode(z).cpu().detach().numpy()[0][0]

    def random_gen(self):
        return self.generate(torch.randn([1, 16, 16]))

    def mash_two(self, path1, path2, f=0.5):
        sr_1 = li.get_samplerate(path1)
        sr_2 = li.get_samplerate(path2)
        audio_1 = li.resample(li.load(path1, sr=sr_1)[0], sr_1, self.sr)
        audio_2 = li.resample(li.load(path2, sr=sr_2)[0], sr_2, self.sr)

        # pad audio so it's equal length
        if len(audio_1) != len(audio_2):
            if len(audio_1) < len(audio_2):
                audio_1 = np.pad(audio_1, (0, len(audio_2) - len(audio_1)), 'constant')
            else:
                audio_2 = np.pad(audio_2, (0, len(audio_1) - len(audio_2)), 'constant')

        l1 = self.get_latent(audio_1)
        l2 = self.get_latent(audio_2)
        lm = (l2 * f) + ((1 - f) * l1)
        dec = self.generate(lm)
        return dec


if __name__ == "__main__":
    mw = ModelWrapperRave('models/rave-nsynth-epic.ts', 16000)
    mashed = mw.mash_two(
        os.path.join('samples', 'flute_synthetic_006-048-127.wav'),
        os.path.join('samples', 'keyboard_synthetic_000-048-127.wav'),
        .5
    )
    print(mashed.shape)

    # mashed = li.effects.pitch_shift(mashed, 16000, -12)
    sf.write(os.path.join("outputs", "mashed-test.wav"), mashed, 16000)

    # for i in range(20):
    #     random = mw.generate(torch.randn([1, 16, 16]))
    #     sf.write(os.path.join("outputs", f"random_{i}.wav"), random, 16000)

