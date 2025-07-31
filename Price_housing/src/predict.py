import os
import joblib
import pandas as pd

def predict_price(input_data: dict):
    model_path = "saved_models/house_price_model.pkl"
    columns_path = "saved_models/expected_columns.txt"

    if not os.path.exists(model_path):
        print("❌ Modèle non trouvé.")
        return
    if not os.path.exists(columns_path):
        print("❌ Fichier des colonnes attendues manquant.")
        return

    print("✅ Chargement du modèle...")
    model = joblib.load(model_path)
    print("✅ Modèle chargé.")

    # Charger les colonnes attendues
    with open(columns_path, "r") as f:
        expected_columns = [line.strip() for line in f]

    print(f"🔍 Colonnes fournies : {list(input_data.keys())}")

    # Compléter avec les colonnes manquantes, en mettant None
    full_input = {col: input_data.get(col, None) for col in expected_columns}
    input_df = pd.DataFrame([full_input], columns=expected_columns)

    try:
        pred_log = model.predict(input_df)
        pred_price = 10 ** pred_log[0]
        print(f"💰 Prix estimé : {pred_price:,.0f} €")
        return pred_price  # ✅ AJOUTER CECI
    except Exception as e:
        print("❌ Erreur pendant la prédiction :", e)
        return None  # ✅ AJOUTER CECI AUSSI

if __name__ == "__main__":
    exemple = {
        "MS Zoning": "RL",
        "Lot Area": 8450,
        "Street": "Pave",
        "Lot Shape": "Reg",
        "Neighborhood": "CollgCr",
        "Overall Qual": 7,
        "Overall Cond": 5,
        "Year Built": 2003,
        "Year Remod/Add": 2003,
        "Gr Liv Area": 1710,
        "Full Bath": 2,
        "Half Bath": 1,
        "Bedroom AbvGr": 3,
        "Kitchen AbvGr": 1,
        "TotRms AbvGrd": 8,
        "Garage Cars": 2,
        "Garage Area": 548,
    }

    predict_price(exemple)
