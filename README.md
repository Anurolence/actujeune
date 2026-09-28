# Acujeune 🇨🇲

> **Le pouls de la jeunesse camerounaise : opportunités, concours, bourses & innovations.**  
> *The heartbeat of Cameroonian youth: opportunities, competitive exams, scholarships & innovations.*

---

## 🌟 Présentation / Overview

**Acujeune** est une plateforme web moderne et citoyenne spécialement conçue pour répondre aux réalités, aux défis et aux aspirations de la jeunesse du Cameroun.

En adéquation avec les besoins concrets des jeunes camerounais (bacheliers, étudiants universitaires, jeunes diplômés, créateurs de startups et entrepreneurs agro-pastoraux), Acujeune centralise l'accès à l'information fiable, aux concours nationaux, aux bourses et aux opportunités réparties sur les dix régions du territoire national.

---

## 🇨🇲 Fonctionnalités Dédiées à la Jeunesse Camerounaise

### 1. 💬 Partage Direct WhatsApp & Contact Rapide
- Au Cameroun, WhatsApp est le canal privilégié d'échanges dans les groupes d'étudiants, d'anciens élèves et de recherche d'emploi.
- Chaque publication dispose d'un bouton direct **« Partager sur WhatsApp »** formatant automatiquement le titre, le résumé, l'émoticône 🇨🇲 et le lien de l'article pour diffusion dans les statuts et groupes.
- Les opportunités comportent un lien direct vers le numéro WhatsApp du recruteur ou de l'organisation (`+237...`).

### 2. 📶 Mode Éco Données (Mo) pour Connexions Mobiles
- Conçu pour les utilisateurs disposant de forfaits internet mobiles (Orange, MTN, Camtel).
- Un commutateur **« Mode Éco (Mo) »** dans la barre de navigation permet de réduire la consommation de données en désactivant le chargement des images lourdes au profit de vignettes légères.

### 3. 🎓 Suivi des Concours d'Entrée aux Grandes Écoles
- Module dédié aux arrêtés de concours (ENS, ENAM, Polytechnique Yaoundé/Douala, FMSB, IRIC, ENSET, etc.).
- Affichage clair des dates limites d'inscription et des conditions de diplômes.

### 4. 💰 Bourses, Subventions & Financements en FCFA
- Informations adaptées aux monnaies et aides locales (Franc CFA - XAF).
- Visibilité sur les dispositifs d'insertion des jeunes comme le **Programme Triennal Spécial Jeunes (PTS-Jeunes)** du MINJEC, le FONIJ, et les bourses AUF.

### 5. 🗺️ Couverture Intégrale des 10 Régions du Cameroun
- Filtre rapide par région :
  - **Centre** (Yaoundé, Ngoa-Ekellé, SOA)
  - **Littoral** (Douala, Makepe, Bonanjo)
  - **Sud-Ouest** (Buea / Silicon Mountain, Limbe)
  - **Ouest** (Bafoussam, Dschang, Foumban)
  - **Nord** (Garoua)
  - **Extrême-Nord** (Maroua, Kousseri)
  - **Adamaoua** (Ngaoundéré)
  - **Nord-Ouest** (Bamenda)
  - **Sud** (Ebolowa, Kribi)
  - **Est** (Bertoua)
  - **National** (Tout le Cameroun)

### 6. 🌐 Bilinguisme Officiel (Français & English)
- Commutateur de langue instantané sans rechargement de page, honorant le caractère bilingue unique du Cameroun.

### 7. 📞 Intégration des Services & Numéros Verts
- Rappel du **Numéro Vert MINJEC Jeunesse : 1515** (appel gratuit pour orientation civique et soutien aux projets de jeunes).

---

## 🚀 Démarrage Rapide

### 1. Lancement du serveur

```bash
cd /home/sir-creed/.gemini/antigravity/scratch/acujeune
./run.sh
```

Ou directement avec l'environnement virtuel Python :

```bash
cd /home/sir-creed/.gemini/antigravity/scratch/acujeune
source .venv/bin/activate
python run.py
```

Le serveur sera immédiatement disponible sur :
- **Application Web** : 👉 [http://localhost:8000](http://localhost:8000)
- **Documentation API Interactive (Swagger)** : 👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Tests Automatisés

Une suite de tests complète valide toutes les fonctionnalités et spécificités camerounaises :

```bash
.venv/bin/python tests/test_api.py
```

Résultats :
```text
✓ Home page renders successfully
✓ Metadata & opportunity statistics working
✓ Retrieved concours posts from API
✓ Created Cameroonian opportunity post ID
✓ Retrieved single post
✓ Detail HTML page renders with FCFA and WhatsApp info
✓ Updated post
✓ Like & unlike working
✓ Added comment
✓ Deleted post and verified 404
🎉 ALL CAMEROONIAN ENHANCEMENT TESTS PASSED SUCCESSFULLY!
```

---

## 📁 Structure du Projet

```text
acujeune/
├── .venv/                   # Environnement virtuel Python
├── app/
│   ├── __init__.py          # Package Python
│   ├── main.py              # Serveur FastAPI, routes web & API REST
│   ├── database.py          # SQLite et migrations automatiques
│   ├── models.py            # Modèles Pydantic avec champs d'opportunités
│   ├── crud.py              # Logique métier et filtres régionaux/concours
│   ├── seed_data.py         # Données réelles sur la jeunesse camerounaise
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Palette tricolore, boutons WhatsApp, mode éco
│   │   ├── js/
│   │   │   ├── app.js       # Logique client, WhatsApp direct, filtres, CRUD
│   │   │   └── i18n.js      # Dictionnaire bilingue (Français / English)
│   │   └── uploads/         # Répertoire des images uploadées
│   └── templates/
│       ├── index.html       # Page principale responsive avec filtres
│       └── post_detail.html # Page détaillée avec contacts WhatsApp & FCFA
├── tests/
│   └── test_api.py          # Suite de tests d'intégration
├── requirements.txt         # Dépendances Python
├── run.py                   # Point d'entrée Python
├── run.sh                   # Script bash de démarrage rapide
└── README.md                # Guide du projet
```
