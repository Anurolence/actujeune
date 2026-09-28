"""Seed authentic updates and opportunities for Cameroonian youth."""
from app.database import get_db

SEED_POSTS = [
    {
        "title": "Silicon Mountain : Comment les jeunes développeurs de Buea révolutionnent la Tech en Afrique centrale",
        "summary": "Au pied du Mont Cameroun, la ville de Buea s'impose comme la capitale technologique des startups fondées par des jeunes de moins de 30 ans.",
        "content": """Au pied du majestueux Mont Cameroun, la ville de Buea vibre au rythme des lignes de code et des pitchs d'incubateurs. Connue sous le surnom de 'Silicon Mountain', cette communauté regroupe des centaines de jeunes développeurs, designers et data scientists camerounais.

Rencontre avec Kevin, 23 ans, co-fondateur d'une plateforme d'apprentissage bilingue :
« Nous avons commencé dans un modeste garage à Molyko avec deux laptops d'occasion. Aujourd'hui, notre solution est utilisée dans 45 lycées à travers le Cameroun. Les jeunes d'ici n'attendent plus que les opportunités viennent à eux, nous les programmons nous-mêmes. »

Les points forts de l'écosystème :
- Plus de 35 startups actives créées par des jeunes diplômés de l'Université de Buea et des instituts locaux.
- Un fort accent sur les solutions locales : paiements mobiles (MTN MoMo, Orange Money), agritech et télémédecine rurale.
- Une communauté d'entraide solidaire et ouverte où le mentorat entre pairs est la règle d'or.

Un modèle inspirant pour toute la sous-région CEMAC !""",
        "category": "Tech & Innovation",
        "region": "Sud-Ouest (Buea)",
        "author_name": "Valerie Etape",
        "author_role": "Reporter Tech Buea",
        "image_url": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1200&q=80",
        "tags": "Tech, SiliconMountain, Startups, Buea, Innovation",
        "opportunity_type": "story",
        "deadline": None,
        "remuneration_fcfa": None,
        "contact_whatsapp": "+237 677 88 99 00",
        "apply_link": "https://siliconmountain.cm",
        "likes_count": 84,
        "views_count": 520,
        "is_featured": 1
    },
    {
        "title": "Concours d'Entrée aux Grandes Écoles 2026 : Calendrier Officiel & Conseils de Préparation",
        "summary": "Retrouvez toutes les dates limites des dépôts de dossiers pour l'ENS, l'ENAM, Polytechnique Yaoundé et la FMSB pour la session 2026.",
        "content": """C'est la saison cruciale pour des dizaines de milliers de bacheliers et étudiants camerounais ! Les arrêtés ministériels fixant le calendrier des concours d'entrée dans les établissements d'enseignement supérieur sont publiés.

Établissements concernés :
1. École Normale Supérieure (ENS Yaoundé & Maroua) : Dépôt des dossiers jusqu'au 15 novembre 2026.
2. École Nationale d'Administration et de Magistrature (ENAM) : Clôture des inscriptions le 20 novembre 2026.
3. École Nationale Supérieure Polytechnique de Yaoundé (ENSPY) : Concours d'ingénieurs prévu début décembre.
4. Faculté de Médecine et des Sciences Biomédicales (FMSB Yaoundé & Douala).

Nos conseils pour réussir :
- Préparez vos pièces d'état civil et certificats médicaux dès maintenant pour éviter les files d'attente.
- Rejoignez les groupes de travail d'anciens élèves et téléchargez les épreuves des 5 dernières années.
- Partagez cette opportunité avec vos camarades via WhatsApp !""",
        "category": "Opportunités & Bourses",
        "region": "National",
        "author_name": "Dieudonné Mvogo",
        "author_role": "Conseiller Orientation Académique",
        "image_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=1200&q=80",
        "tags": "Concours, ENS, ENAM, Universite, Yaounde, Cameroun",
        "opportunity_type": "concours",
        "deadline": "2026-11-20",
        "remuneration_fcfa": "Bourse de formation & Intégration",
        "contact_whatsapp": "+237 690 11 22 33",
        "apply_link": "https://minesup.gov.cm",
        "likes_count": 128,
        "views_count": 940,
        "is_featured": 1
    },
    {
        "title": "Programme Triennal Spécial Jeunes (PTS-Jeunes) : Financements jusqu'à 5 000 000 FCFA",
        "summary": "Le Ministère de la Jeunesse et de l'Éducation Civique (MINJEC) ouvre le guichet de réarmement civique et d'insertion économique.",
        "content": """Le Fonds National d'Insertion des Jeunes (FONIJ) et le MINJEC invitent les jeunes porteurs de projets âgés de 15 à 35 ans à soumettre leurs dossiers de financement.

Secteurs prioritaires éligibles :
- Agriculture et élevage périurbain (pisciculture, aviculture, manioc, maïs, maraîchers).
- Transformation agroalimentaire locale (chips de banane plantain, farines locales, miel du Nord).
- Économie numérique et services digitaux.
- Artisanat d'art et confection textile locale.

Avantages pour les lauréats :
- Financement remboursable à taux préférentiel jusqu'à 5 millions de FCFA.
- Formation gratuite de 3 semaines au Réarmement Moral, Civique et Entrepreneurial (REAMORCE).
- Suivi personnalisé par un tuteur d'entreprise pendant 1 an.

Rendez-vous dans les Centres Multifonctionnels de Promotion des Jeunes (CMPJ) de votre arrondissement ou postulez en ligne.""",
        "category": "Entrepreneuriat",
        "region": "National",
        "author_name": "Carine Ngo",
        "author_role": "Animatrice Jeunesse & Insertion",
        "image_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80",
        "tags": "PTSJeunes, MINJEC, Financement, Entrepreneuriat, FCFA",
        "opportunity_type": "bourse",
        "deadline": "2026-12-31",
        "remuneration_fcfa": "Jusqu'à 5 000 000 FCFA",
        "contact_whatsapp": "+237 671 22 33 44",
        "apply_link": "https://minjec.gov.cm",
        "likes_count": 95,
        "views_count": 780,
        "is_featured": 1
    },
    {
        "title": "De l'idée au champ : Yannick (25 ans) lance une ferme hydroponique intelligente à Douala",
        "summary": "Ingénieur agronome de formation, Yannick produit des légumes frais en milieu urbain avec 90% moins d'eau grâce à des tours verticales automatisées.",
        "content": """À Makepe, dans le 5e arrondissement de Douala, une toiture d'immeuble cache une véritable révolution verte. Yannick Fotso, 25 ans, a transformé 200 m² de béton en une ferme hydroponique ultra-productive.

« Douala est une métropole grouillante où la terre cultivable se raréfie. Avec mon équipe, nous avons conçu des systèmes hydroponiques alimentés à l'énergie solaire et contrôlés par des capteurs IoT fabriqués localement », explique le jeune entrepreneur.

Résultats :
- Plus de 800 kg de légumes bio récoltés chaque mois.
- 90% d'économie d'eau par rapport à l'agriculture traditionnelle.
- 6 emplois directs créés pour de jeunes diplômés sans travail.

Yannick offre désormais des ateliers de formation gratuits chaque samedi pour encourager les jeunes citadins à se lancer dans l'agritech durable.""",
        "category": "Entrepreneuriat",
        "region": "Littoral (Douala)",
        "author_name": "Marcelle Kouam",
        "author_role": "Journaliste Agro & Climat",
        "image_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=1200&q=80",
        "tags": "AgriTech, Douala, Entrepreneuriat, JeunesseVerte, Innovation",
        "opportunity_type": "story",
        "deadline": None,
        "remuneration_fcfa": None,
        "contact_whatsapp": "+237 694 55 66 77",
        "apply_link": None,
        "likes_count": 62,
        "views_count": 430,
        "is_featured": 0
    },
    {
        "title": "Hackathon Innovation Mobile 237 : Prix de 3 000 000 FCFA pour le meilleur projet FinTech & MoMo",
        "summary": "48 heures de challenge intensif pour concevoir les applications de paiement mobile et d'inclusion financière adaptées aux commerçants camerounais.",
        "content": """Avis aux développeurs, UX designers et étudiants en informatique de Yaoundé, Douala, Buea et Dschang !

Le grand Hackathon Mobile 237 ouvre ses portes. L'objectif : créer des solutions concrètes simplifiant la vie des petits commerçants du marché Mfoundi, de Mokolo et de New-Bell grâce aux API Mobile Money.

Ce que l'organisation prend en charge :
- Connexion Internet fibre optique ultra-rapide et repas pendant les 48 heures.
- Mentorat par des ingénieurs seniors de grandes entreprises télécoms.
- 1er Prix : 3 000 000 FCFA de dotation + 6 mois d'incubation gratuite.
- 2e Prix : 1 500 000 FCFA.
- 3e Prix : 750 000 FCFA.

Inscriptions d'équipes de 2 à 4 personnes ouvertes jusqu'au 10 novembre 2026.""",
        "category": "Tech & Innovation",
        "region": "Littoral (Douala)",
        "author_name": "Arnaud Tchinda",
        "author_role": "Lead Hub Numérique",
        "image_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200&q=80",
        "tags": "Hackathon, FinTech, MoMo, Douala, Startup237",
        "opportunity_type": "emploi_stage",
        "deadline": "2026-11-10",
        "remuneration_fcfa": "3 000 000 FCFA de prix",
        "contact_whatsapp": "+237 675 33 44 55",
        "apply_link": "https://hackathon237.cm",
        "likes_count": 79,
        "views_count": 610,
        "is_featured": 1
    },
    {
        "title": "Innovation Solaire au Sahel : Des lycéens de Maroua fabriquent des kits d'éclairage avec des batteries recyclées",
        "summary": "Un club scientifique d'élèves du Grand Nord fabrique des kits solaires à partir de batteries d'ordinateurs récupérées pour éclairer les salles d'étude rurales.",
        "content": """À Maroua, le soleil est une ressource inépuisable. Le club 'Génie Jeune' du Lycée Classique a décidé d'en faire une solution pour pallier les coupures d'électricité qui perturbent les révisions des examens.

Menés par Aminatou, 17 ans en classe de Terminale C, ces jeunes génies collectent les cellules 18650 des vieilles batteries d'ordinateurs portables jetées, les testent et les réassemblent dans des boîtiers imprimés en 3D avec du plastique recyclé.

« Chaque kit permet d'alimenter trois ampoules LED pendant 8 heures et de recharger deux téléphones. Nous avons déjà équipé 12 foyers et 2 classes préparatoires dans les villages environnants », se réjouit Aminatou.

Le projet a reçu le Prix Spécial du Jury au Salon de l'Innovation Junior de Yaoundé.""",
        "category": "Pleins feux Jeunesse",
        "region": "Extrême-Nord (Maroua)",
        "author_name": "Ahmadou Bello",
        "author_role": "Correspondant Régional Nord",
        "image_url": "https://images.unsplash.com/photo-1509391365360-2e959784a276?auto=format&fit=crop&w=1200&q=80",
        "tags": "Solaire, Sahel, Écologie, Lycéens, Recyclage, Maroua",
        "opportunity_type": "story",
        "deadline": None,
        "remuneration_fcfa": None,
        "contact_whatsapp": "+237 698 22 11 00",
        "apply_link": None,
        "likes_count": 89,
        "views_count": 540,
        "is_featured": 0
    },
    {
        "title": "Ndop & Haute Couture : Sonia (22 ans) hisse l'artisanat des Grassfields sur les podiums internationaux",
        "summary": "La jeune styliste originaire de Bafoussam réinterprète le pagne royal traditionnel Ndop en tenues modernes prisées par la jeunesse urbaine.",
        "content": """Le tissu traditionnel Ndop, emblème séculaire des chefferies bamiléké et bamoun, s'offre une nouvelle jeunesse grâce au talent de Sonia Tagne.

À seulement 22 ans, diplômée en design textile, Sonia a fondé 'Ndop Urbain'. Elle collabore avec des tisseuses et brodeuses traditionnelles de Baham et Foumban pour créer des vestes streetwear, des sacs d'ordinateurs et des casquettes contemporaines.

« Notre patrimoine culturel est d'une richesse inouïe. Pour nous les jeunes, porter le Ndop au quotidien n'est pas seulement une question de mode : c'est une fierté d'identité et un soutien économique direct aux femmes artisanes de nos villages. »

Sa collection a récemment été présentée à la Nuit des Créateurs de Douala avec une ovation debout du public !""",
        "category": "Culture & Arts",
        "region": "Ouest (Bafoussam)",
        "author_name": "Florence Ngu",
        "author_role": "Chroniqueuse Culture & Création",
        "image_url": "https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=1200&q=80",
        "tags": "Mode, Culture, Ndop, Bafoussam, Artisanat, Heritage",
        "opportunity_type": "story",
        "deadline": None,
        "remuneration_fcfa": None,
        "contact_whatsapp": "+237 673 44 55 66",
        "apply_link": None,
        "likes_count": 51,
        "views_count": 380,
        "is_featured": 0
    }
]

def seed_database():
    """Populates the database with initial posts if empty."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM posts")
        row = cursor.fetchone()
        if row and row["count"] == 0:
            for p in SEED_POSTS:
                cursor.execute("""
                INSERT INTO posts (
                    title, summary, content, category, region, author_name, author_role,
                    image_url, tags, opportunity_type, deadline, remuneration_fcfa,
                    contact_whatsapp, apply_link, likes_count, views_count, is_featured, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    p["title"], p["summary"], p["content"], p["category"], p["region"],
                    p["author_name"], p["author_role"], p["image_url"], p["tags"],
                    p["opportunity_type"], p["deadline"], p["remuneration_fcfa"],
                    p["contact_whatsapp"], p["apply_link"],
                    p["likes_count"], p["views_count"], p["is_featured"], "published"
                ))
            
            # Add seed comments
            cursor.execute("SELECT id FROM posts WHERE id = 1")
            first_post = cursor.fetchone()
            if first_post:
                cursor.execute("""
                INSERT INTO comments (post_id, author_name, content)
                VALUES (1, 'Junior (Buea)', 'Silicon Mountain is rising! Proud to be coding here in Molyko 🇨🇲💻')
                """)
                cursor.execute("""
                INSERT INTO comments (post_id, author_name, content)
                VALUES (1, 'Samuel (Douala)', 'Le Cameroun a du génie. Continuons à partager ces opportunités !')
                """)
            conn.commit()
            print("Seed database refreshed with rich Cameroonian opportunities!")
