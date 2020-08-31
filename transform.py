import torch
import librosa
import random
import torch
from torchaudio.transforms import MelSpectrogram, AmplitudeToDB
import librosa
from torchvision import transforms
from torchvision.transforms import Lambda, ToTensor
import numpy as np
from librosa.feature.inverse import mel_to_audio

melspectrogram_transform_parameters = {
    "sample_rate": 44100,
    "n_mels": 256,
    "hop_length": 256,
    "win_length": 1536,
    "n_fft": 2048
}
normalization_parameters = {
    "ref_level": 20.0,
    "min_level": -80.0,
    "min_value": 0,
    "max_value": 1
}


# think about adding fast spec to wav https://arxiv.org/pdf/1808.06719.pdf

class ToMono(object):  # can be replaced with lambda
    """Convert sterio signal to mono by averaging channels."""

    def __call__(self, sound):
        if len(sound.size()) < 2:
            return sound
        return ((sound[0, ...] + sound[1, ...]) / 2).squeeze(0)


class ReduceSampleRate(object):
    def __init__(self, factor=2):
        self.factor = factor

    def __call__(self, sound):
        return sound[..., ::self.factor]


class CutRandomWindow(object):
    """Crop window from time domain.

       Args:
           window_size (int): Desired window size in.
       """

    def __init__(self, window_size):
        self.window_size = window_size

    def __call__(self, signal):
        sound_duration = signal.size()[-1]
        assert sound_duration >= self.window_size
        if sound_duration == self.window_size:
            return signal
        window_time = random.randint(self.window_size, sound_duration - self.window_size)
        return signal[..., window_time:window_time + self.window_size]


class CutRandomWindowSound(object):
    """Crop window from time domain.

       Args:
           window_size (int): Desired window size in.
       """

    def __init__(self, window_size):
        self.window_size = window_size

    def __call__(self, signal):
        sound_duration = signal.size()[-2]
        assert sound_duration >= self.window_size
        if sound_duration == self.window_size:
            return signal
        window_time = random.randint(self.window_size, sound_duration - self.window_size)
        return signal[..., window_time:window_time + self.window_size, :]


class NormalizeSpectrogram(object):
    def __init__(self, ref_level, min_level, min_value=0, max_value=1):
        self.ref_level = ref_level
        self.min_level = min_level
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, spectrogram):
        return shift_and_normalize_spec(spectrogram, self.ref_level, self.min_level, self.min_value, self.max_value)


def shift_and_normalize_spec(spectrogram, ref_level=20.0, min_level=-80, min_value=0, max_value=1):
    return normalize_spectrogram(spectrogram - ref_level, min_level) * (max_value - min_value) + min_value


def denormalize_spectrogram_and_inverse_shift(spectrogram, ref_level=20.0, min_level=-80, min_value=0, max_value=1):
    return denormalize_spectrogram(spectrogram, min_level, min_value, max_value) + ref_level


def normalize_spectrogram(spectrogram, min_level=-80.0):
    return torch.clamp(spectrogram / -min_level, -1.0, 0.0) + 1.0


def denormalize_spectrogram(spectrogram, min_level=-80.0, min_value=0, max_value=1):
    return ((torch.clamp(spectrogram, 0.0, 1.0) - 1.0) - min_value) / (max_value - min_value) * -min_level


# region transform
normalize_output = normalization_parameters is not None

transforms_to_be_composed = [
    Lambda(lambda x: (x[0] + x[1]) / 2),
    MelSpectrogram(**melspectrogram_transform_parameters),
    AmplitudeToDB()
]
if normalize_output:
    transforms_to_be_composed.append(
        Lambda(lambda x: shift_and_normalize_spec(x, **normalization_parameters))
    )
direct_transform = transforms.Compose(transforms_to_be_composed)
# endregion


# region inverse transform
def pointwise_mel_to_audio(x):
    return mel_to_audio(x,
                        sr=melspectrogram_transform_parameters["sample_rate"],
                        n_fft=melspectrogram_transform_parameters["n_fft"],
                        hop_length=melspectrogram_transform_parameters["hop_length"],
                        n_iter=4)


transforms_to_be_composed = [
    Lambda(lambda x: librosa.db_to_power(x.to("cpu").numpy(), ref=1.0)),
    Lambda(lambda x: np.stack([pointwise_mel_to_audio(chunk) for chunk in x])),
    ToTensor(),
    Lambda(lambda x: torch.cat((x, x)).permute(1, 0, 2))
]
if normalize_output:
    transforms_to_be_composed = \
        [Lambda(lambda x: denormalize_spectrogram_and_inverse_shift(x, **normalization_parameters))] + \
        transforms_to_be_composed
fast_inverse_transform = transforms.Compose(transforms_to_be_composed)
# endregion
