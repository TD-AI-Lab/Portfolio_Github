import os
import joblib
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from data_loader import load_data

def train_and_save_model():
    preprocessor, X_train, X_test, y_train, y_test = load_data()

    svr_model = SVR(kernel="rbf", C=100.0, epsilon=0.1)
    model_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("svr", svr_model)
    ])

    model_pipeline.fit(X_train, y_train)
    y_pred = model_pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"MAE : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R² : {r2:.4f}")

    if r2 < 0.5:
        print("Performance insuffisante, modèle non sauvegardé.")
        return

    os.makedirs("saved_models", exist_ok=True)
    joblib.dump(model_pipeline, "saved_models/house_price_model.pkl")
    print("Modèle sauvegardé avec succès.")

    with open("saved_models/expected_columns.txt", "w") as f:
        for col in X_train.columns:
            f.write(col + "\n")

if __name__ == "__main__":
    train_and_save_model()