import os
import joblib
import numpy as np
import matplotlib.pyplot as plt
from data_loader import load_data
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

def evaluate_model():
    model_path = "saved_models/house_price_model.pkl"
    if not os.path.exists(model_path):
        print("Modèle non trouvé.")
        return

    model = joblib.load(model_path)
    _, X_train, X_test, y_train, y_test = load_data()

    y_pred_log = model.predict(X_test)
    y_test_real = 10 ** y_test
    y_pred_real = 10 ** y_pred_log

    mae = mean_absolute_error(y_test_real, y_pred_real)
    rmse = root_mean_squared_error(y_test_real, y_pred_real)
    r2 = r2_score(y_test_real, y_pred_real)

    print(f"MAE : {mae:.2f} $")
    print(f"RMSE : {rmse:.2f} $")
    print(f"R² : {r2:.4f}")

    plt.figure(figsize=(8, 6))
    plt.scatter(y_test_real, y_pred_real, alpha=0.6)
    plt.plot([y_test_real.min(), y_test_real.max()],
             [y_test_real.min(), y_test_real.max()],
             "r--", label="Ligne parfaite")
    plt.xlabel("Prix réel ($)")
    plt.ylabel("Prix prédit ($)")
    plt.title("Comparaison des prix réels vs prédits")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.close()

if __name__ == "__main__":
    evaluate_model()