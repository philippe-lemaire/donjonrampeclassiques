w1 = [
    "Agrandissement",
    "Appel de familier",
    "Bouclier magique",
    "Charme-personne",
    "Compréhension des langues",
    "Contact glacial",
    "Corde enchantée",
    "Couleurs dansantes",
    "Détection de la magie*",
    "Feuille morte",
    "Invocation d’animaux",
    "Lecture de la magie",
    "Mains brûlantes",
    "Masque mystique d’Ekim",
    "Mur de force",
    "Nuage étouffant",
    "Pattes d’araignées",
    "Portail enchanté",
    "Projectile magique",
    "Réparer",
    "Runes des mortels",
    "Sommeil",
    "Tour de magie",
    "Ventriloquie",
    "Invoquer un patron**",
    "Lier un patron**",
    "(Sort de Patron)***",
]

w2 = [
    "Affinité arcanique",
    "Bâton de mage",
    "Bouche magique",
    "Compagnon invisible",
    "Convocation de monstre",
    "Détection du mal*",
    "Effroi",
    "Force",
    "Fracassement",
    "Image miroir",
    "Invisibilité",
    "Lévitation",
    "Localisation d’objet",
    "Manteau d’épines de Nythuul",
    "Oubli",
    "Ouverture",
    "Perception extra-sensorielle (PES)",
    "Phantasme",
    "Rayon affaiblissant",
    "Rayon brûlant",
    "Résistance au feu",
    "Toile d’araignée",
    "Voir l’invisible",
    "(Sort de Patron)***",
]

w3 = [
    "Boule de feu",
    "Bourrasque",
    "Champion éternel",
    "Concoction de potion",
    "Consulter les esprits",
    "Convocation de démon",
    "Dissipation de la magie",
    "Éclair",
    "Écriture de la magie",
    "Hâte",
    "Limier occulte",
    "Maelström entropique d’Emirikol",
    "Magie des épées",
    "Paralysie*",
    "Pétrification",
    "Phase planaire",
    "Ralentissement",
    "Respiration aquatique",
    "Rune des fées",
    "Soumission*",
    "Souffle de vie",
    "Transfert",
    "Vol",
    "(Sort de Patron)***",
]

w4 = [
    "Aide méthodique de Lokerimon",
    "Contrôle de la glace" "Contrôle du feu",
    "Métamorphose",
    "Sens de mage",
    "Transmutation de la terre",
]

w5 = [
    "Champignons féconds d’Hepsoj",
    "Chasseur infaillible de Lokerimon",
    "Duplication",
    "Purge mentale",
    "Rempart magique",
]

c1 = [
    "Bénédiction",
    "Détection de la magie",
    "Détection du mal",
    "Divination",
    "Injonction",
    "Nourriture divine",
    "Paralysie",
    "Protection contre le mal",
    "Résistance au froid ou à la chaleur",
    "Sanctuaire",
    "Ténèbres",
]

c2 = [
    "Bannissement",
    "Charme-serpent",
    "Guérison de la paralysie",
    "Malédiction",
    "Malédiction du bois",
    "Neutralisation du poison et des maladies",
    "Pierre venimeuse",
    "Restauration de la vitalité",
    "Soumission",
    "Symbole divin",
    "Transe du lotus",
]

c3 = [
    "Animation des morts",
    "Arme spirituelle",
    "Désenvoûtement",
    "Éclair divin",
    "Entretien avec les morts",
    "Exorcisme",
    "Nom secret",
]

c4 = [
    "Calamité des dieux",
    "Consacrer/ Déconsacrer",
    "Infestation",
    "Séisme",
]

c5 = [
    "Contrôle du climat",
    "Flammes du juste",
    "Tourbillon de lames",
]

wizard_spells = {k: v for k, v in zip(range(1, 6), [w1, w2, w3, w4, w5])}
cleric_spells = {k: v for k, v in zip(range(1, 6), [c1, c2, c3, c4, c5])}
