import os
import json
import numpy as np
import librosa
import sounddevice as sd
import soundfile as sf
from tensorflow.keras.models import load_model
from utils.config import *
from utils.audio_utils import compute_enriched_features, extract_features

def load_label_map():
    with open(LABEL_MAP_PATH, encoding="utf-8") as f:
        return json.load(f)

def predict_emotion(filepath):
    print("🔍 Étape 1 : Chargement du modèle...")
    model = load_model(MODEL_PATH)

    print("🎧 Étape 2 : Extraction des caractéristiques...")
    features = extract_features(filepath)
    if features is None:
        raise ValueError("Échec de l'extraction des features.")

    print("Shape of features:", features.shape)
    X = np.expand_dims(features, axis=0)  # (1, 160, 57)

    print("🤖 Étape 3 : Prédiction...")
    prediction = model.predict(X)[0]

    label_map = load_label_map()
    idx_to_label = {v: k for k, v in label_map.items()}

    predicted_index = int(np.argmax(prediction))
    predicted_label = idx_to_label[predicted_index]
    confidence = float(np.max(prediction))

    emotion = predicted_label.upper()
    sorted_scores = sorted(
        ((idx_to_label[i], float(score)) for i, score in enumerate(prediction)),
        key=lambda x: x[1],
        reverse=True
    )

    return emotion, confidence, sorted_scores

def append_to_journal(entry):
    with open(JOURNAL_PATH, "a", encoding="utf-8") as f:
        f.write(entry.strip() + "\n")

def read_journal():
    if not os.path.exists(JOURNAL_PATH):
        return []
    with open(JOURNAL_PATH, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def record_audio(seconds=5, device=None):
    audio = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, device=device)
    sd.wait()
    sf.write(TEMP_AUDIO_PATH, audio, SAMPLE_RATE)
    return TEMP_AUDIO_PATH