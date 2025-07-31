import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os

def load_audio(filepath, sr=22050):
    """
    Charge un fichier audio de manière robuste (PySoundFile + audioread fallback).
    """
    try:
        y, sr = librosa.load(filepath, sr=sr, mono=True)
        return y, sr
    except Exception:
        # Fallback manuel si PySoundFile et audioread échouent
        import audioread
        try:
            with audioread.audio_open(filepath) as f:
                sr = f.samplerate
                channels = f.channels
                data = b''.join([buf for buf in f])
                y = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                if channels == 2:
                    y = y.reshape((-1, 2)).mean(axis=1)
                return y, sr
        except Exception as e:
            raise RuntimeError(f"Échec complet du chargement audio (fallback audioread) : {e}")

def get_bpm(y, sr):
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo

def get_duration(y, sr):
    return len(y) / sr

def get_rms(y):
    return float(np.sqrt(np.mean(np.square(y))))

def extract_mfcc(y, sr, n_mfcc=13):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfcc.mean(axis=1)

def get_chroma(y, sr):
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    return chroma.mean(axis=1)

def detect_silence(y, sr, threshold=0.01):
    rms = librosa.feature.rms(y=y)[0]
    silence_ratio = np.sum(rms < threshold) / len(rms)
    return silence_ratio > 0.5

def generate_waveform_plot(y, sr, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if len(y) == 0:
        return False
    plt.figure(figsize=(10, 4))
    librosa.display.waveplot(y, sr=sr)
    plt.title("Waveform")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return True