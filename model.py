import torch
import os
import soundfile as sf
import librosa as li


class ModelWrapper:
    def __init__(self, ts_file):
        self.model = torch.jit.load(ts_file)
        self.model.eval()

    def get_latent(self, path):
        x = li.load(path)[0]
        x = torch.from_numpy(x).reshape(1, 1, -1).float()
        z = self.model.encode(x)
        return z

    def generate(self, z):
        return self.model.decode(z).cpu().detach().numpy()[0][0]

    def mash_two(self, path1, path2):
        l1 = self.get_latent(path1)
        l2 = self.get_latent(path2)
        lm = (l1 + l2) / 2
        dec = self.generate(lm)
        return dec


if __name__ == "__main__":
    mw = ModelWrapper('rave_nsynth.ts')
    mashed = mw.mash_two(
        os.path.join('samples', 'flute_acoustic_028-048-127.wav'),
        os.path.join('samples', 'organ_electronic_067-048-127.wav')
    )

    # mashed = li.effects.pitch_shift(mashed, 16000, -12)

    sf.write(os.path.join("outputs", "test_mean.wav"), mashed, 16000)

