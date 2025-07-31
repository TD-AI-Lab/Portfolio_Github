import streamlit as st
from utils.model_utils import predict_emotion, append_to_journal, read_journal, record_audio
import sounddevice as sd
from utils.config import TEMP_AUDIO_PATH
import time
import os

st.set_page_config(page_title="MiniMoodVoice", page_icon="🎙️", layout="centered")
st.title("🎙️ MiniMoodVoice")
st.markdown("Détection d’émotions à partir de votre voix.\n\nEnregistrez 5 secondes, puis laissez la magie opérer 🪄.")

# Choix du micro
st.subheader("🎧 Choisir un microphone")
devices = sd.query_devices()
input_devices = [dev["name"] for dev in devices if dev["max_input_channels"] > 0]
device_indices = {dev["name"]: i for i, dev in enumerate(devices) if dev["max_input_channels"] > 0}

default_device = sd.default.device[0]
default_name = devices[default_device]["name"] if default_device is not None else input_devices[0]
device_name = st.selectbox("Périphérique d'entrée", input_devices, index=input_devices.index(default_name))
selected_device = device_indices[device_name]

# Enregistrement
st.subheader("🎤 Enregistrement vocal (5 secondes)")
if st.button("📢 Lancer l'enregistrement"):
    with st.spinner("Enregistrement en cours..."):
        try:
            path = record_audio(seconds=5, device=selected_device)
        except Exception as e:
            st.error(f'Échec de l’enregistrement : {e}')
            st.stop()
    st.success("✅ Enregistrement terminé")

    # Prédiction
    with st.spinner("Analyse de l'émotion..."):
        emotion, confidence, scores = predict_emotion(path)

    # Affichage
    st.markdown(f"### 🧠 Émotion prédite : `{emotion}`")
    st.progress(confidence)

    st.markdown("#### 📊 Détail des scores")
    import pandas as pd
    df_scores = pd.DataFrame(scores, columns=['Émotion', 'Score'])
    st.bar_chart(df_scores.set_index("Émotion"))

    st.markdown('#### 🧾 Tableau des scores')
    st.table(df_scores)

    # Journal
    entry = f"{emotion} ({confidence:.2%})"
    append_to_journal(entry)

# Journal historique
st.subheader("📜 Historique")
journal = read_journal()
if not journal:
    st.info("Aucune analyse effectuée pour l’instant.")
else:
    for i, entry in enumerate(reversed(journal[-10:]), 1):
        st.markdown(f"**{i}.** {entry}")

# Séparateur visuel
st.markdown("---")

# Bouton de fermeture avec confirmation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        """
        <style>
        .quit-button button {
            background-color: #ff4d4d;
            color: white;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="quit-button">', unsafe_allow_html=True)
    confirm = st.checkbox("✅ Je confirme vouloir quitter l'application", key="confirm_exit")
    quit_clicked = st.button("🛑 Quitter l'application", key="quit_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    if quit_clicked:
        if confirm:
            st.warning("Fermeture de l'application...")
            time.sleep(0.5)
            os._exit(0)
        else:
            st.info("Veuillez cocher la case pour confirmer.")