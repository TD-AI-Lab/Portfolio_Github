import streamlit as st
import sys
import os
import time

# Ajouter src/ au path pour pouvoir importer predict.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from predict import predict_price

st.set_page_config(
    page_title="Estimation Prix Immobilier",
    page_icon="🏠",
    layout="centered"
)

st.title("🏠 Estimation du Prix de votre Maison à Ames (Iowa)")
st.markdown("Remplissez les informations ci-dessous pour obtenir une estimation approximative du prix de votre maison.")

with st.form("estimation_form"):
    st.subheader("📍 Localisation")
    neighborhood = st.selectbox("Quartier (Neighborhood)", [
        "CollgCr", "Veenker", "Crawfor", "NoRidge", "Mitchel", "Somerst",
        "NWAmes", "OldTown", "BrkSide", "Sawyer", "NridgHt", "NAmes",
        "SawyerW", "IDOTRR", "MeadowV", "Edwards", "Timber", "Gilbert",
        "StoneBr", "ClearCr", "NPkVill", "Blmngtn", "BrDale", "SWISU",
        "Blueste"
    ], index=0)

    st.subheader("📐 Superficie et agencement")
    gr_liv_area = st.number_input("Surface habitable (Gr Liv Area, en pieds²)", value=1710, min_value=200)
    lot_area = st.number_input("Surface du terrain (Lot Area, en pieds²)", value=8450, min_value=500)

    st.subheader("🛏️ Pièces et aménagements")
    bedroom = st.slider("Chambres (Bedroom AbvGr)", min_value=0, max_value=10, value=3)
    kitchen = st.slider("Cuisines (Kitchen AbvGr)", min_value=1, max_value=5, value=1)
    tot_rooms = st.slider("Nombre total de pièces (TotRms AbvGrd)", min_value=1, max_value=20, value=8)
    full_bath = st.slider("Salles de bain complètes (Full Bath)", min_value=0, max_value=5, value=2)
    half_bath = st.slider("Salles de bain avec WC uniquement (Half Bath)", min_value=0, max_value=3, value=1)

    st.subheader("🚗 Garage")
    garage_cars = st.slider("Places de garage (Garage Cars)", min_value=0, max_value=5, value=2)
    garage_area = st.number_input("Surface du garage (Garage Area, en pieds²)", value=548, min_value=0)

    st.subheader("🏗️ Qualité & Année")
    overall_qual = st.slider("Qualité globale (Overall Qual)", min_value=1, max_value=10, value=7)
    overall_cond = st.slider("État global (Overall Cond)", min_value=1, max_value=10, value=5)

    col1, col2 = st.columns(2)
    with col1:
        year_built = st.number_input("Année de construction", value=2003, min_value=1800, max_value=2025)
    with col2:
        year_remod = st.number_input("Année de rénovation", value=max(2003, year_built), min_value=year_built, max_value=2025)

    st.subheader("📑 Autres informations")
    ms_zoning = st.selectbox("Zonage (MS Zoning)", ["RL", "RM", "FV", "RH", "C (all)"], index=0)
    street = st.selectbox("Type de rue", ["Pave", "Grvl"], index=0)

    submitted = st.form_submit_button("Estimer le prix")

if submitted:
    # Sécurité backend : éviter une rénovation avant construction
    if year_remod < year_built:
        st.error("❌ L'année de rénovation ne peut pas être antérieure à l'année de construction.")
        st.stop()

    input_data = {
        "MS Zoning": ms_zoning,
        "Lot Area": lot_area,
        "Street": street,
        "Lot Shape": None,
        "Neighborhood": neighborhood,
        "Overall Qual": overall_qual,
        "Overall Cond": overall_cond,
        "Year Built": year_built,
        "Year Remod/Add": year_remod,
        "Gr Liv Area": gr_liv_area,
        "Full Bath": full_bath,
        "Half Bath": half_bath,
        "Bedroom AbvGr": bedroom,
        "Kitchen AbvGr": kitchen,
        "TotRms AbvGrd": tot_rooms,
        "Garage Cars": garage_cars,
        "Garage Area": garage_area,
    }

    with st.spinner("⏳ Prédiction en cours..."):
        try:
            prediction = predict_price(input_data)
            if isinstance(prediction, float):
                st.success(f"💰 Le prix estimé de votre maison est : **{prediction:,.0f} $**")
            else:
                st.error(f"Erreur de prédiction : {prediction}")
        except Exception as e:
            st.error(f"❌ Une erreur est survenue : {e}")

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