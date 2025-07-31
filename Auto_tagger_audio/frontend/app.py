import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import tempfile
import json
import shutil
import uuid
import pandas as pd
from backend.tag_generator import generate_audio_tags
from backend.audio_analysis import load_audio, generate_waveform_plot

# -- Juste après tous les imports --
if "exit_requested" in st.session_state and st.session_state.exit_requested:
    st.warning("Fermeture de l'application...")
    time.sleep(0.5)
    os._exit(0)
    st.stop()

# Sidebar
st.sidebar.header("⚙️ Options")
st.sidebar.markdown("Choisissez le mode d'analyse et les options d'affichage/export.")

model_mode = st.sidebar.selectbox("Mode de génération de tags", ["musicnn", "heuristique"])
show_scores = st.sidebar.checkbox("Afficher les scores (si disponibles)", value=True)

if model_mode == "musicnn":
    top_k = st.sidebar.slider("Nombre de tags à afficher", min_value=1, max_value=50, value=10)
else:
    top_k = None  # non utilisé en heuristique

export_json = st.sidebar.checkbox("Exporter les tags en JSON", value=False)
export_csv = st.sidebar.checkbox("Exporter les tags en CSV", value=False)

uploaded_file = st.file_uploader("Choisissez un fichier audio (MP3, WAV, etc.)", type=["mp3", "wav", "flac"])

if uploaded_file:
    TMP_DIR = tempfile.mkdtemp()
    unique_id = str(uuid.uuid4())
    file_path = os.path.join(TMP_DIR, f"{unique_id}_{uploaded_file.name}")

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.audio(file_path)

    waveform_path = None
    try:
        waveform, sr = load_audio(file_path)
        EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")
        os.makedirs(EXPORT_DIR, exist_ok=True)
        waveform_path = os.path.join(EXPORT_DIR, f"waveform_{unique_id}.png")
        generate_waveform_plot(waveform, sr, waveform_path)
    except Exception as e:
        st.warning(f"Impossible d'afficher le waveform : {e}")

    with st.spinner("Analyse en cours..."):
        try:
            tags = generate_audio_tags(file_path, model_mode=model_mode, return_probabilities=show_scores, top_n=top_k or 999)
            st.success("Analyse terminée")
        except Exception as e:
            st.error(f"Erreur lors de l'analyse : {e}")
            tags = {}

    if tags and isinstance(tags, dict):
        st.subheader("🎯 Tags générés")

        try:
            # Mode heuristique (valeurs = str ou list ou bool)
            if model_mode == "heuristique":
                df = pd.DataFrame(
                    [{"Tag": k, "Descriptif": ", ".join(v) if isinstance(v, list) else str(v)} for k, v in tags.items()]
                )

                # Affichage HTML avec style responsive
                html_table = """
<style>
table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px;
    word-wrap: break-word;
    vertical-align: top;
}
th {
    background-color: #444;
    color: white;
    font-weight: bold;
    text-align: left;
}
</style>
<table>
    <thead>
        <tr>
            <th>Tag</th>
            <th>Descriptif</th>
        </tr>
    </thead>
    <tbody>
                """

                for _, row in df.iterrows():
                    html_table += f"""
<tr>
    <td>{row['Tag']}</td>
    <td>{row['Descriptif']}</td>
</tr>
                    """

                html_table += "</tbody></table>"

                st.markdown(html_table, unsafe_allow_html=True)


            else:
                # Mode musicnn
                sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
                df = pd.DataFrame(sorted_tags[:top_k], columns=["Tag", "Score" if show_scores else "Présent"])
                st.dataframe(df)

        except Exception as e:
            st.warning(f"Affichage brut en JSON (erreur DataFrame) : {e}")
            st.json(tags)

        EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")
        os.makedirs(EXPORT_DIR, exist_ok=True)

        if export_json:
            json_path = os.path.join(EXPORT_DIR, f"tags_{unique_id}.json")
            try:
                with open(json_path, "w") as f:
                    json.dump(tags, f, indent=2)
                st.success(f"📁 Fichier JSON exporté dans : {json_path}")
            except Exception as e:
                st.warning(f"Erreur lors de l'export JSON : {e}")

        if export_csv:
            csv_path = os.path.join(EXPORT_DIR, f"tags_{unique_id}.csv")
            try:
                df.to_csv(csv_path, index=False)
                st.success(f"📁 Fichier CSV exporté dans : {csv_path}")
            except Exception as e:
                st.warning(f"Erreur lors de l'export CSV : {e}")
    else:
        st.warning("Aucun tag n'a été généré ou le format des données est invalide.")

    st.markdown("---")
    st.subheader("🔎 Informations audio")
    try:
        duration = len(waveform) / sr
        rms = (waveform ** 2).mean() ** 0.5
        st.info(f"Durée : {round(duration, 2)}s  \nVolume RMS : {round(rms, 4)}")
    except:
        pass

    if waveform_path and os.path.exists(waveform_path):
        st.image(waveform_path, caption="Waveform", use_column_width=True)
        os.remove(waveform_path)
    else:
        st.warning("Aucun waveform disponible à afficher.")

else:
    st.info("Veuillez téléverser un fichier pour commencer l'analyse.")

# Ligne de séparation visuelle
st.markdown("---")

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
        """, unsafe_allow_html=True
    )

    with st.container():
        if st.button("🛑 Quitter l'application"):
            uploaded_file = None
            st.session_state.exit_requested = True
            st.experimental_rerun()