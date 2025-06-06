
# Déploiement Render - Outil CNAPS

Ce projet est prêt à être déployé sur [https://render.com](https://render.com) avec persistance des données grâce à un disque `/persistent`.

---

## ✅ Étapes à suivre

### 1. Créer un nouveau Web Service
- Allez sur [https://dashboard.render.com](https://dashboard.render.com)
- Cliquez sur **"New" > "Web Service"**
- Source : Importez ce dossier via GitHub ou Render CLI

### 2. Paramètres Render à configurer
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `gunicorn app:app`
- **Instance Type** : Starter (7€/mois)
- **Environment** : Python
- **Region** : Europe (Frankfurt)

### 3. Ajouter un disque persistant
- Une fois le service créé, allez dans l’onglet **"Disks"**
- Cliquez sur **"Add Disk"**
  - **Name** : `data`
  - **Mount Path** : `/persistent`
  - **Size** : `1 GB` suffit

---

## ⚙️ Fonctionnement de l'application

- La base SQLite `cnaps.db` est automatiquement déplacée dans `/persistent`
- Si elle n'existe pas, elle est créée avec la table `dossiers`
- Les données ne seront **pas perdues** au redémarrage

---

## 📁 Contenu du projet

- `app.py` : l'application Flask
- `requirements.txt` : dépendances Python
- `templates/` : fichiers HTML
- `static/` : images logo et tampon
