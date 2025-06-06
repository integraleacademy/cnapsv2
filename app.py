import os
import shutil

# Chemin vers la base sur le disque persistant
db_path = '/persistent/cnaps.db'
default_db_path = 'cnaps.db'

# Si on est sur Render ET que le fichier n'existe pas encore dans /persistent
if os.path.exists('/persistent') and not os.path.exists(db_path):
    if os.path.exists(default_db_path):
        shutil.move(default_db_path, db_path)


from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import os
from datetime import datetime
from docx import Document
from docx.shared import Inches

import os
import shutil
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Gestion disque persistant
db_path = '/persistent/cnaps.db' if os.path.exists('/persistent') else 'cnaps.db'
default_db_path = 'cnaps.db'

if os.path.exists('/persistent') and not os.path.exists(db_path):
    if os.path.exists(default_db_path):
        shutil.move(default_db_path, db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Vérifier si la table "dossiers" existe, sinon la créer
with app.app_context():
    inspector = inspect(db.engine)
    if 'dossiers' not in inspector.get_table_names():
        print("⚠️ Table 'dossiers' absente, initialisation de la base...")
        class Dossier(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            nom = db.Column(db.String(100))
            prenom = db.Column(db.String(100))
            date_naissance = db.Column(db.String(20))
            statut = db.Column(db.String(50))
            commentaire = db.Column(db.Text)
            complet = db.Column(db.String(20))

        db.create_all()
