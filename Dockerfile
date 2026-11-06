# Utiliser une image Python officielle légère
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requis
COPY requirements.txt requirements.txt
COPY app.py app.py

# Installer les dépendances
RUN pip install -r requirements.txt

# Exposer le port du serveur web
EXPOSE 5000

# Commande pour démarrer l'application
CMD ["python", "app.py"]