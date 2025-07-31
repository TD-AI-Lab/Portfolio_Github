import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def load_data(csv_path="datas/AmesHousing.csv"):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Le fichier '{csv_path}' est introuvable.")

    df = pd.read_csv(csv_path)

    # Supprimer colonnes inutiles
    df.drop(columns=["Order", "PID"], inplace=True, errors="ignore")

    # Supprimer colonnes avec trop de NaN
    seuil_nan = 0.15
    df = df.loc[:, df.isnull().mean() < seuil_nan]

    if "SalePrice" not in df.columns:
        raise ValueError("'SalePrice' est manquant dans le jeu de données.")

    y = np.log10(df["SalePrice"])
    X = df.drop(columns=["SalePrice"])

    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numeric_cols),
        ("cat", categorical_pipeline, categorical_cols)
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return preprocessor, X_train, X_test, y_train, y_test