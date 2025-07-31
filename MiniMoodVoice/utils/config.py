# config.py — Paramètres globaux

# Modèle et label map
MODEL_PATH = "model/emotion_model.keras"
LABEL_MAP_PATH = "model/label_map.json"

# Extraction audio
SAMPLE_RATE = 16000
N_MFCC = 13
MAX_LEN = 160

# Journal
JOURNAL_PATH = "journal.txt"

# Enregistrement audio temporaire
TEMP_AUDIO_PATH = "temp_audio.wav"

NUM_CLASSES = 5