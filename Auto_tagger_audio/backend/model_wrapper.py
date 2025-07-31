import json

class HeuristicTagger:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            self.thresholds = json.load(f)

    def generate_tags(self, features: dict) -> dict:
        tags = {}

        # --- BPM
        bpm = features['bpm']
        bpm_thresh = self.thresholds.get("bpm", {})
        tempo_tag = None
        for label, threshold in sorted(bpm_thresh.items(), key=lambda x: x[1]):
            if bpm <= threshold:
                tempo_tag = label
                break
        if tempo_tag is None:
            tempo_tag = max(bpm_thresh, key=bpm_thresh.get)
        tags["tempo"] = tempo_tag

        # --- RMS
        rms = features['rms']
        rms_thresh = self.thresholds.get("rms", {})
        dynamic_tag = None
        for label, threshold in sorted(rms_thresh.items(), key=lambda x: x[1]):
            if rms <= threshold:
                dynamic_tag = label
                break
        if dynamic_tag is None:
            dynamic_tag = max(rms_thresh, key=rms_thresh.get)
        tags["dynamics"] = dynamic_tag

        # --- Energy from MFCC
        mfcc = features['mfcc']
        brightness = mfcc[0] if isinstance(mfcc, list) else mfcc[0]
        mfcc_thresh = self.thresholds.get("mfcc", {})
        if brightness > mfcc_thresh.get("brightness_threshold", 30):
            tags["ambiance"] = "bright"
        elif brightness < mfcc_thresh.get("darkness_threshold", 15):
            tags["ambiance"] = "dark"
        else:
            tags["ambiance"] = "balanced"

        # --- Silence
        silence = features['silence']
        silence_thresh = self.thresholds.get("silence", {}).get("ratio_threshold", 0.5)
        tags["silence"] = "yes" if silence else "no"

        # --- Ajout des tags personnalisés
        tag_set = []

        tempo_map = self.thresholds.get("tags", {}).get("tempo", {})
        if tempo_tag in tempo_map:
            tag_set.extend(tempo_map[tempo_tag])

        dynamics_map = self.thresholds.get("tags", {}).get("dynamics", {})
        if dynamic_tag in dynamics_map:
            tag_set.extend(dynamics_map[dynamic_tag])

        energy_map = self.thresholds.get("tags", {}).get("energy", {})
        if dynamic_tag in energy_map:
            tag_set.extend(energy_map[dynamic_tag])

        if tag_set:
            tags["additional"] = ", ".join(sorted(set(tag_set)))

        return tags