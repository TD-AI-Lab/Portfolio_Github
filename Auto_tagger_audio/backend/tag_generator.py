import os
import logging
from typing import Dict, Union
import numpy as np
from backend import audio_analysis
from backend.model_wrapper import HeuristicTagger
from musicnn.extractor import extractor

def generate_audio_tags(filepath: str, model_mode: str = "musicnn", return_probabilities: bool = False, top_n: int = 10) -> Dict[str, Union[float, str]]:
    try:
        waveform, sr = audio_analysis.load_audio(filepath)
    except Exception as e:
        logging.error(f"Erreur lors du chargement de l'audio : {e}")
        raise

    bpm = audio_analysis.get_bpm(waveform, sr)
    duration = audio_analysis.get_duration(waveform, sr)
    rms = audio_analysis.get_rms(waveform)
    mfcc = audio_analysis.extract_mfcc(waveform, sr)
    chroma = audio_analysis.get_chroma(waveform, sr)
    silence = audio_analysis.detect_silence(waveform, sr)

    features = {
        'bpm': bpm,
        'duration': duration,
        'rms': rms,
        'mfcc': mfcc.tolist(),
        'chroma': chroma.tolist(),
        'silence': silence
    }

    if model_mode == "musicnn":
        tmp_wav = filepath
        if not filepath.lower().endswith(".wav"):
            import librosa
            import soundfile as sf
            y, sr = librosa.load(filepath, sr=16000, mono=True)
            tmp_wav = filepath.replace(".", "_converted.", 1) + ".wav"
            sf.write(tmp_wav, y, sr)

        try:
            taggram, tags = extractor(tmp_wav, extract_features=False)
            averaged_scores = np.mean(taggram, axis=0)
            sorted_tags_scores = sorted(zip(tags, averaged_scores), key=lambda x: x[1], reverse=True)
            top_tags = sorted_tags_scores[:top_n]

            if return_probabilities:
                return {tag: float(score) for tag, score in top_tags}
            else:
                return {tag: True for tag, _ in top_tags}

        except Exception as e:
            logging.error(f"Erreur lors du traitement des résultats musicnn : {e}")
            raise

    elif model_mode == "heuristique":
        try:
            model = HeuristicTagger("config/thresholds.json")
            return model.generate_tags(features)
        except Exception as e:
            logging.error(f"Erreur dans HeuristicTagger : {e}")
            raise

    else:
        raise ValueError(f"Mode de modèle inconnu : {model_mode}")