# 🏡 Estimation du Prix de votre Maison - PRICE_HOUSING

Ce projet est une application complète d'estimation du prix d'une maison basée sur le jeu de données [**Ames Housing**](https://www.kaggle.com/datasets/prevek18/ames-housing-dataset).  
L'utilisateur peut renseigner les caractéristiques de son bien via une interface graphique intuitive pour obtenir un prix approximatif.  
Un modèle de Machine Learning (**SVR - Support Vector Regressor**) a été entraîné pour fournir ces prédictions.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.46.1-red)
![Statut](https://img.shields.io/badge/Statut-Fonctionnel-brightgreen)

---

📦 Pour cloner uniquement ce projet :

```bash
git clone --filter=blob:none --sparse https://github.com/TD-AI-Lab/Portfolio_Github.git
cd Portfolio_Github
git sparse-checkout set Price_housing
```

---

## 📁 Structure du projet

```
PRICE_HOUSING/
├── datas/
│   └── AmesHousing.csv               # Jeu de données original
├── frontend/
│   └── app.py                        # Interface graphique Streamlit
├── saved_models/
│   ├── house_price_model.pkl         # Modèle de régression sauvegardé
│   └── expected_columns.txt          # Colonnes attendues par le modèle
├── src/
│   ├── data_loader.py                # Chargement et prétraitement des données
│   ├── evaluate_model.py             # Évaluation (R², MAE, RMSE...)
│   ├── predict.py                    # Fonction de prédiction à partir d’un input utilisateur
│   └── train_model.py                # Entraînement du modèle (SVR)
```

---

## 🚀 Installation

### 1. Créer un environnement virtuel (optionnel mais recommandé)
```bash
python -m venv venv
source venv/bin/activate  # Sous Linux/Mac
venv\Scripts\activate     # Sous Windows
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

---

## 🧠 Entraîner le modèle

Le modèle présent dans le dossier **saved_models** (**house_price_model.pkl**) est déjà entrainé.
Mais si vous souhaitez le réentrainer, vous pouvez lancez l’entraînement du modèle avec :

```bash
python src/train_model.py
```

Vous pouvez ensuite évaluer sa performance avec :

```bash
python src/evaluate_model.py
```

---

## 🖥️ Lancer l'application

Démarrez l’interface graphique (Streamlit) avec :

```bash
streamlit run frontend/app.py
```

Vous pourrez alors renseigner les informations de la maison et obtenir une estimation du prix.

---

## 🖼️ Aperçu de l’application

<h3 align="center">Interface principale</h3>
<p align="center">
  <img src="images/Interface_principale.png" style="max-width:500px; height:auto;" alt="Interface principale">
</p>

<h3 align="center">Prediction du prix</h3>
<p align="center">
  <img src="images/Interface_principale_2.png" style="max-width:500px; height:auto;" alt="Prediction du prix">
</p>

---

## 🛑 Fermeture de l'application & comportement de Streamlit

L'application utilise **Streamlit** comme moteur d'interface graphique.  
Par défaut, Streamlit fonctionne comme un **serveur local**, et reste actif tant qu'il n’est pas fermé manuellement.

### 🧠 Ce qu’il faut savoir :

- **Fermer simplement l’onglet du navigateur ne stoppe pas le processus Python.**
- Si vous quittez l’application sans fermer le terminal, un **processus Python peut rester actif en arrière-plan**.

### ✅ Solution intégrée : bouton "Quitter l’application"

Un **bouton rouge "🛑 Quitter l'application"** a été ajouté en bas de l’interface, avec confirmation, pour permettre aux utilisateurs :
- de fermer l’application proprement,
- d’éviter de laisser des scripts tourner inutilement,
- et de simplifier l’usage pour les personnes non techniques.

> Ce bouton appelle une fermeture immédiate du processus pour garantir qu’aucune ressource ne reste utilisée.

---

## 📈 Performance

- Modèle : **SVR (Support Vector Regressor)**
- R² sur les données de test : **0.8625**
- MAE : **20 919.11 $**
- RMSE : **33 205.49 $**
- Évaluation via `evaluate_model.py`

---

## ⚠️ Limites du modèle

Bien que le modèle d’estimation fonctionne bien (R² = 0.889), il présente certaines **limites** importantes à connaître :

- **Erreur moyenne notable :**  
  Le modèle se trompe en moyenne de **20 919 $** par estimation, et certaines erreurs peuvent dépasser **30 000 $**. Ces écarts sont acceptables pour une première évaluation, mais à ne pas confondre avec une expertise immobilière.

- **Pas de prise en compte du contexte réel :**  
  L’algorithme ne connaît **ni l’état réel du bien**, ni la **demande locale**, ni les **travaux récents** ou **l’environnement immédiat** (proximité des écoles, nuisances, etc.).

- **Simplicité du modèle :**  
  Le modèle utilisé est un SVR (Support Vector Regressor) avec des paramètres standards. Il n’intègre pas de techniques avancées comme le boosting, l’analyse temporelle ou la vision par ordinateur.

- **Encodage statique des variables :**  
  Les transformations appliquées aux données sont basées sur l’entraînement initial. Toute donnée trop éloignée de celles du jeu AmesHousing peut produire une **estimation incohérente**.

- **Pas de bornes de confiance :**  
  Le modèle fournit une estimation unique, **sans indiquer de fourchette** autour du prix estimé. Il peut donc donner un faux sentiment de précision.

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Vous pouvez :
- ouvrir une issue pour signaler un bug ou suggérer une amélioration
- forker ce repo et proposer une pull request

---

## 📄 Licence

Projet open-source libre d’utilisation, modification et diffusion. Merci de mentionner l’auteur original si réutilisé.

---

## 📌 Auteurs

Projet développé par TD:AI (Florian Pigot) afin de démontrer les compétences de l'entreprise dans le cadre de missions freelance.

Pour toute mission ou besoin similaire : **contactez-moi via mon profil !**

---

## ©️ Droits d'auteur

Ce modèle et le logiciel qui l'entoure sont mis à disposition gratuitement pour un usage personnel, non commercial et éducatif.

Toute utilisation par une entreprise, dans un cadre commercial, ou intégrée à un produit payant nécessite une licence commerciale préalable, à obtenir auprès de l’auteur.

Contact : tdai.flo@gmail.com

Modification, redistribution ou hébergement du code à des fins commerciales sans accord explicite sont strictement interdits.

---

## 📬 Contact

📧 tdai.flo@gmail.com  
🐦 [@TD_AI_Lab](https://x.com/TD_AI_Lab)
