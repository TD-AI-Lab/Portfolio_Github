
# 🎙️ MiniMoodVoice - Détecteur d'émotions vocales

Ce projet est une application complète qui permet de vous enregistrer sur un intervalle de 5 secondes et de connaître votre émotion principale par analyse de votre voix.
Cette application à interface graphique basée sur Streamlit se connecte automatiquement à votre périphérique d'enregistrement par défaut, mais vous pouvez le modifier dans un menu disponible en haut de l'interface.

Cette application prédit l'émotion vocale parmi les 5 suivantes :

- 😌 Calme
- 😠 Colère
- 😄 Joie
- 😨 Peur
- 😢 Tristesse

Le modèle utilisé afin de classifier votre audio est un réseau de neurones créé from scratch au sein de TD:AI.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.2-red)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13.0-orange)
![Statut](https://img.shields.io/badge/Statut-Fonctionnel-brightgreen)

---

📦 Pour cloner uniquement ce projet :

```bash
git clone --filter=blob:none --sparse https://github.com/TD-AI-Lab/Portfolio_Github.git
cd Portfolio_Github
git sparse-checkout set MiniMoodVoice
```

---

## 📁 Structure du projet

```
MINIMOODVOICE/
├── app.py                  # Interface Streamlit
├── journal.txt             # Historique des runs
├── environment.yml         # Environnement Conda
├── model/
│   ├── emotion_model.keras # Modèle Keras (580Ko)
│   └── label_map.json      # Mapping des classes
└── utils/
    ├── audio_utils.py      # Enregistrement & traitement audio
    ├── config.py           # Constantes globales
    └── model_utils.py      # Chargement et inférence du modèle
```

---

## ⚡ Installation

> 🎯 Requiert **Python 3.10**
> 💻 Prérequis : [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

```bash
conda env create -f environment.yml
conda activate minimoodvoice
python launch.py
```

🚀 L’interface s’ouvrira automatiquement dans votre navigateur à la suite de la commande `python`.

> **Remarque** : Le modèle est déjà entraîné et inclus (`model/emotion_model.keras`). Aucun code source du réseau n’est requis pour l’inférence.

---

## 🧠 Fonctionnalités

- 🎤 Enregistrement audio depuis un micro (5 secondes)
- ⚡ Prédiction d’émotion en quelques secondes
- 📊 Affichage graphique des scores (barres + tableau)
- 🕘 Historique des prédictions dans la session
- ✅ Fonctionne 100% hors ligne

---

## 📊 Forces et limites du modèle

MiniMoodVoice repose sur un petit modèle de détection d’émotions vocales (580 Ko seulement !) conçu pour être rapide, léger et utilisable localement.
Il a été créé de zéro au sein de TD:AI afin de tester des méthodes d'optimisation mathématique dès sa création.

Voici ce qu’il faut savoir sur ses performances :

### ✅ Points forts

- **Très bonne reconnaissance de la colère, de la joie et de la peur**.
- Le modèle fonctionne **sans connexion internet** : tout se fait localement, en quelques secondes.
- Il est capable de détecter une émotion dominante même sur des extraits courts (1 à 2 secondes).
- **Taille ultra réduite** (moins de 1 Mo), idéal pour l’intégrer dans des projets embarqués ou mobiles.

### ⚠️ Limites connues

- Le modèle a **beaucoup de mal à reconnaître l’émotion "calme"**, qu’il confond souvent avec la tristesse.  
  > Cela est dû au fait que le calme n’a pas toujours de caractéristiques vocales très tranchées, et qu'il avait peu de datas pour cette émotion lors de son entraînement.
- Il peut parfois **confondre tristesse et peur**, surtout lorsque la voix est douce ou hésitante.
- Ce modèle n’est **pas encore adapté aux voix d’enfants ou aux enregistrements très bruités**.

---

## 🖼️ Aperçu de l’application

<h3 align="center">Interface principale avant analyse</h3>
<p align="center">
  <img src="images/Interface_1.png" style="max-width:500px; height:auto;" alt="Interface principale avant analyse">
</p>

<h3 align="center">Interface principale après analyse</h3>
<p align="center">
  <img src="images/Interface_2.png" style="max-width:500px; height:auto;" alt="Interface principale après analyse">
</p>

<h3 align="center">Tableau de probabilités et journal</h3>
<p align="center">
  <img src="images/Interface_3.png" style="max-width:500px; height:auto;" alt="Tableau de probabilités et journal">
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

## 🤝 Contribuer

Les contributions sont les bienvenues ! Vous pouvez :
- ouvrir une issue pour signaler un bug ou suggérer une amélioration
- forker ce repo et proposer une pull request

---

## 📄 Licence

Projet open-source libre d’utilisation, modification et diffusion. Merci de mentionner l’auteur original si réutilisé.

---

## 📌 Auteur

Projet développé par TD:AI (Florian Pigot) afin de démontrer les compétences de l'entreprise dans le cadre de la création de modèles d'intelligence artificielles légers et rapides.

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
