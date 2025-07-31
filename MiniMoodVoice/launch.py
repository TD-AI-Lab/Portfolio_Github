import subprocess
import os
import sys  # pour récupérer l'environnement Python courant

if __name__ == "__main__":
    script_path = os.path.join(os.path.dirname(__file__), "frontend", "app.py")
    subprocess.run([
        sys.executable,  # utilise l'interpréteur de l'environnement actif
        "-m", "streamlit", "run", script_path
    ], shell=True)