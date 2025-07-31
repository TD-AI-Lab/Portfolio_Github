import numpy as np
import librosa
import soundfile as sf
from utils.config import SAMPLE_RATE, TEMP_AUDIO_PATH, N_MFCC, MAX_LEN
import traceback

def compute_enriched_features(mfccs, pitch_series, rms_series, audio, sr):
    # 1. Normalisation de la prosodie avant dérivées
    pitch_series = (pitch_series - np.mean(pitch_series)) / (np.std(pitch_series) + 1e-8)
    rms_series = (rms_series - np.mean(rms_series)) / (np.std(rms_series) + 1e-8)

    # 1ère et 2e dérivées MFCC
    dx = mfccs[1:] - mfccs[:-1]
    d2x = dx[1:] - dx[:-1]
    dx = (dx - dx.mean(axis=0)) / (dx.std(axis=0) + 1e-8)
    d2x = (d2x - d2x.mean(axis=0)) / (d2x.std(axis=0) + 1e-8)

    # Prosodie dérivée
    delta_pitch = pitch_series[1:] - pitch_series[:-1]
    d2_pitch = delta_pitch[1:] - delta_pitch[:-1]
    delta_pitch = (delta_pitch - np.mean(delta_pitch)) / (np.std(delta_pitch) + 1e-8)
    d2_pitch = (d2_pitch - np.mean(d2_pitch)) / (np.std(d2_pitch) + 1e-8)

    delta_rms = rms_series[1:] - rms_series[:-1]
    d2_rms = delta_rms[1:] - delta_rms[:-1]
    delta_rms = (delta_rms - np.mean(delta_rms)) / (np.std(delta_rms) + 1e-8)
    d2_rms = (d2_rms - np.mean(d2_rms)) / (np.std(d2_rms) + 1e-8)

    # HNR (via harmonicity proxy)
    hnr = librosa.effects.harmonic(audio)
    hnr_env = librosa.feature.rms(y=hnr).squeeze()
    d_hnr = np.diff(hnr_env)
    d2_hnr = np.diff(d_hnr)
    d_hnr = (d_hnr - d_hnr.mean()) / (d_hnr.std() + 1e-8)
    d2_hnr = (d2_hnr - d2_hnr.mean()) / (d2_hnr.std() + 1e-8)

    # Spectral centroid
    centroid = librosa.feature.spectral_centroid(y=audio, sr=sr).squeeze()
    d_centroid = np.diff(centroid)
    d2_centroid = np.diff(d_centroid)
    d_centroid = (d_centroid - d_centroid.mean()) / (d_centroid.std() + 1e-8)
    d2_centroid = (d2_centroid - d2_centroid.mean()) / (d2_centroid.std() + 1e-8)

    # Spectral flatness
    flat = librosa.feature.spectral_flatness(y=audio).squeeze()
    d_flat = np.diff(flat)
    d2_flat = np.diff(d_flat)
    d_flat = (d_flat - d_flat.mean()) / (d_flat.std() + 1e-8)
    d2_flat = (d2_flat - d2_flat.mean()) / (d2_flat.std() + 1e-8)

    # Jitter via pitch instabilité
    dpitch_instab = np.diff(pitch_series)
    d2pitch_instab = np.diff(dpitch_instab)
    djitter = (dpitch_instab - dpitch_instab.mean()) / (dpitch_instab.std() + 1e-8)
    d2jitter = (d2pitch_instab - d2pitch_instab.mean()) / (d2pitch_instab.std() + 1e-8)

    # Formant proxy via envelope
    S = np.abs(librosa.stft(audio, n_fft=1024))
    envelope = librosa.feature.melspectrogram(S=S, sr=sr, n_mels=5).mean(axis=0)
    d_env = np.diff(envelope)
    d2_env = np.diff(d_env)
    dformant1 = (d_env - d_env.mean()) / (d_env.std() + 1e-8)
    d2formant1 = (d2_env - d2_env.mean()) / (d2_env.std() + 1e-8)

    # Silence ratio variation
    energy = librosa.feature.rms(y=audio).squeeze()
    silence = (energy < 0.01).astype(float)
    d_sil = np.diff(silence)
    d2_sil = np.diff(d_sil)
    dsil = (d_sil - d_sil.mean()) / (d_sil.std() + 1e-8)
    d2sil = (d2_sil - d2_sil.mean()) / (d2_sil.std() + 1e-8)

    # Alignement général
    min_T = min(
        len(dx), len(d2x), len(delta_pitch), len(d2_pitch), len(delta_rms), len(d2_rms),
        len(d_hnr), len(d2_hnr), len(d_centroid), len(d2_centroid),
        len(d_flat), len(d2_flat), len(djitter), len(d2jitter),
        len(dformant1), len(d2formant1), len(dsil), len(d2sil),
        len(pitch_series), len(rms_series)
    )

    dx = dx[:min_T]
    d2x = d2x[:min_T]
    enriched = np.stack([
        delta_pitch[:min_T], d2_pitch[:min_T],
        delta_rms[:min_T], d2_rms[:min_T],
        d_hnr[:min_T], d2_hnr[:min_T],
        d_centroid[:min_T], d2_centroid[:min_T],
        d_flat[:min_T], d2_flat[:min_T],
        djitter[:min_T], d2jitter[:min_T],
        dformant1[:min_T], d2formant1[:min_T],
        dsil[:min_T], d2sil[:min_T],
        pitch_series[:min_T], rms_series[:min_T]  # ⬅️ ajout prosodie brute
    ], axis=-1)

    return dx, d2x, enriched

def extract_features(filepath):
    try:
        audio, _ = librosa.load(filepath, sr=SAMPLE_RATE)
        if audio is None or len(audio) == 0:
            raise ValueError("Audio vide ou corrompu")
        if len(audio) < 1024:
            raise ValueError("Signal trop court pour l’analyse")

        mfccs = librosa.feature.mfcc(y=audio, sr=SAMPLE_RATE, n_mfcc=N_MFCC).T
        pitch = librosa.yin(audio, fmin=50, fmax=500, sr=SAMPLE_RATE)
        rms = librosa.feature.rms(y=audio).T.squeeze()

        T_init = MAX_LEN + 2
        min_len = min(mfccs.shape[0], len(pitch), len(rms))

        mfccs = mfccs[:min_len]
        pitch = pitch[:min_len]
        rms = rms[:min_len]

        if min_len < T_init:
            pad_len = T_init - min_len
            mfccs = np.pad(mfccs, ((0, pad_len), (0, 0)), mode='constant')
            pitch = np.pad(pitch, (0, pad_len), mode='constant')
            rms = np.pad(rms, (0, pad_len), mode='constant')
        else:
            mfccs = mfccs[:T_init]
            pitch = pitch[:T_init]
            rms = rms[:T_init]

        mfccs = (mfccs - mfccs.mean(axis=0)) / (mfccs.std(axis=0) + 1e-8)

        dx, d2x, enriched = compute_enriched_features(mfccs, pitch, rms, audio, SAMPLE_RATE)

        min_T = min(dx.shape[0], d2x.shape[0], enriched.shape[0])
        dx = dx[:min_T]
        d2x = d2x[:min_T]
        enriched = enriched[:min_T]
        mfccs_trunc = mfccs[:min_T]

        raw_features = np.concatenate([mfccs_trunc, dx, d2x, enriched], axis=-1).astype(np.float32)
        raw_features = raw_features[:MAX_LEN]

        if raw_features.shape[0] < MAX_LEN:
            pad_len = MAX_LEN - raw_features.shape[0]
            raw_features = np.pad(raw_features, ((0, pad_len), (0, 0)), mode='constant')

        feature_dim = raw_features.shape[1]
        assert raw_features.shape == (MAX_LEN, feature_dim), f"Expected ({MAX_LEN}, {feature_dim}), got {raw_features.shape}"
        assert np.isfinite(raw_features).all(), "NaN ou inf détecté dans les features"

        return raw_features

    except Exception as e:
        print(f"❌ Erreur lors de l'extraction de {filepath} : {type(e).__name__} - {str(e)}")
        traceback.print_exc()
        return None