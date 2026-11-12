# 🏦 TP Docker - Application Bancaire Simple

Ce projet est une application web bancaire simple développée en Python (Flask) et conteneurisée avec Docker. Il permet de gérer des comptes bancaires et d'effectuer des transactions basiques via une base de données SQLite intégrée.

## 📁 Arborescence du projet

- `app.py` : Code source du serveur web et logique de l'API bancaire.
- `requirements.txt` : Dépendances du projet (Flask).
- `Dockerfile` : Instructions pour la création de l'image Docker.
- `docker-compose.yml` : Configuration pour lancer l'application facilement.

---

## 🧠 Concepts et Justifications des Choix Techniques (Question II)

### Le concept et l'importance d'un conteneur
Un conteneur est une unité logicielle standardisée qui regroupe le code d'une application ainsi que toutes ses dépendances. Contrairement aux machines virtuelles, les conteneurs partagent le noyau (kernel) du système d'exploitation hôte. 
**Avantages principaux :**
1. **Portabilité :** Un conteneur s'exécutera exactement de la même manière sur n'importe quel environnement ("Build once, run anywhere").
2. **Légèreté :** Démarrage en quelques millisecondes et faible consommation de ressources.
3. **Isolation :** Chaque conteneur est isolé des autres et du système hôte.

### Choix technologiques
*   **Python & Flask :** Nous avons fait le choix d'utiliser Flask, un micro-framework Web qui intègre son propre serveur Web. Cela nous permet d'avoir une "application simple" et légère, sans avoir besoin de configurer un serveur lourd comme Apache ou Nginx.
*   **SQLite :** Nous avons décidé d'utiliser SQLite car c'est une base de données embarquée fonctionnant avec un simple fichier local (`banque.db`). Cela nous évite d'avoir à configurer un deuxième conteneur séparé, gardant ainsi notre application 100% autonome.
*   **Image Docker `python:3.9-slim` :** Nous avons sélectionné cette image allégée pour réduire le temps de construction, la consommation de ressources et la surface d'attaque potentielle.

---

## 🚀 Lancement du Conteneur (Étape 1 - Local)

Pour exécuter l'application sur votre machine de développement, assurez-vous que Docker est démarré et que vous êtes dans le dossier contenant le `Dockerfile`.

**1. Construire l'image :**
```bash
docker build -t mon-app-banque .
```

**2. Démarrer le conteneur :**
```bash
docker run -d -p 5000:5000 --name banque_container mon-app-banque
```
*L'application est désormais accessible sur `http://localhost:5000`.*

---

## ☁️ Copier / Transférer le Conteneur (Étape 2 - Docker Hub)

**Étape A : Pousser l'image sur Docker Hub (depuis la machine source)**
1. Se connecter : `docker login`
2. Créer une étiquette : `docker tag mon-app-banque <VOTRE_NOM_UTILISATEUR>/mon-app-banque:v1`
3. Pousser l'image : `docker push <VOTRE_NOM_UTILISATEUR>/mon-app-banque:v1`

**Étape B : Récupérer et lancer sur une nouvelle machine**
```bash
docker run -p 5000:5000 <VOTRE_NOM_UTILISATEUR>/mon-app-banque:v1
```

---

## 🛠️ Utilisation de l'Application (Guide de l'API)

Vous pouvez tester les fonctions en utilisant `curl` dans votre terminal ou un outil comme **Postman**.

### ➕ 1. Créer un compte (POST)
```bash
curl -X POST http://localhost:5000/creer -H "Content-Type: application/json" -d '{"nom":"Jean Dupont", "solde_initial": 150.0}'
```

### 🔍 2. Consulter un compte (GET)
```bash
curl http://localhost:5000/consulter/1
```
*(Remplacez `1` par l'ID du compte. Testable aussi dans un navigateur).*

### 💵 3. Déposer de l'argent (POST)
```bash
curl -X POST http://localhost:5000/deposer/1 -H "Content-Type: application/json" -d '{"montant": 50.0}'
```

### 💸 4. Retirer de l'argent (POST)
```bash
curl -X POST http://localhost:5000/retirer/1 -H "Content-Type: application/json" -d '{"montant": 25.0}'
```

### ❌ 5. Effacer un compte (DELETE)
```bash
curl -X DELETE http://localhost:5000/effacer/1
```