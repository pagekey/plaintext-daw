import os
import wave

import numpy as np


MAX_INT16 = 2**15

def wav_to_np(wav_path) -> np.ndarray:
    f = wave.open(wav_path)
    # Read metadata
    samples = f.getnframes()
    data = f.readframes(samples)
    channels = f.getnchannels()
    sample_width = f.getsampwidth()
    sample_rate = f.getframerate()
    f.close()
    # Convert to normalized np array
    audio_int16 = np.frombuffer(data, dtype=np.int16)
    audio_float32 = audio_int16.astype(np.float32)
    audio_normalized = audio_float32 / MAX_INT16
    return audio_normalized, channels, sample_width, sample_rate

def np_to_wav(song_np, channels, sample_width, sample_rate, wav_path):
    # Convert song to raw audio
    audio_raw = song_np * MAX_INT16
    audio_raw_int16 = audio_raw.astype(np.int16)
    # Write to file
    f_out = wave.open(wav_path, 'wb')
    f_out.setnchannels(channels)
    f_out.setsampwidth(sample_width)
    f_out.setframerate(sample_rate)
    f_out.writeframes(audio_raw_int16)
