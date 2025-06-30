# Projet Amis Communs - PySpark

## Objectifs
Ce projet utilise Apache Spark avec PySpark pour analyser un réseau social et identifier les amis communs entre différents utilisateurs.  
L'objectif principal est de trouver les amis partagés entre deux utilisateurs spécifiques : **Sidi (ID=1)** et **Mohamed (ID=2)**.

## Jeu de Données

### Format des données  
Chaque ligne représente un utilisateur avec ses amis selon le format suivant :  
`<user_id> <nom> <friend_id1>,<friend_id2>,...`

### Exemple de données  
1 Sidi 2,3,4
2 Mohamed 1,3,5
3 Amine 1,2,5
4 Sara 1
5 Salma 2,3

### Description du réseau  
- Sidi (ID=1) : ami avec Mohamed(2), Amine(3), Sara(4)  
- Mohamed (ID=2) : ami avec Sidi(1), Amine(3), Salma(5)  
- Amine (ID=3) : ami avec Sidi(1), Mohamed(2), Salma(5)  
- Sara (ID=4) : amie avec Sidi(1)  
- Salma (ID=5) : amie avec Mohamed(2), Amine(3)  

## Étapes d'Exécution

### Prérequis
- Python 3.7+  
- Java 11 ou supérieur  
- Apache Spark 3.4.1  
- PySpark  

### Installation des dépendances
```bash
pip install -r requirements.txt

Exécution locale
python main.py

Exécution dans Google Colab
 1-Ouvrir Google Colab
 2-Copier le contenu de main.py
 3-Exécuter les cellules dans l'ordre
 4-Installer les dépendances si nécessaire :
!pip install pyspark findspark

## Structure du Projet
mutual-friends-pyspark/
│
├── main.py              # Code principal du projet
├── requirements.txt     # Dépendances Python
├── README.md            # Documentation du projet
├── tests
└── results/
    └── output_example.txt  # Exemple de sortie


## Algorithme
Étape 1 : Analyse des données
Parsing de chaque ligne pour extraire l'ID utilisateur, le nom et la liste d'amis
Création d'un mapping ID → Nom pour l'affichage

Étape 2 : Génération des paires
Pour chaque utilisateur, création de paires (utilisateur, ami)
Génération des ensembles d'amis potentiellement communs

Étape 3 : Calcul des amis communs
Utilisation de reduceByKey pour trouver l'intersection des ensembles d'amis
Filtrage des paires ayant au moins un ami commun

Étape 4 : Extraction du résultat
Filtrage spécifique pour la paire Sidi-Mohamed
Affichage au format demandé

### Résultats Attendus
### Sortie complète
Tous les amis communs :
 1(Sidi) et 2(Mohamed): [3]
 1(Sidi) et 3(Amine): [2]
 2(Mohamed) et 3(Amine): [5]
### Résultat spécifique - Amis communs entre Sidi et Mohamed:
1<Sidi>2<Mohamed>[3]
### Interprétation
Le résultat 1<Sidi>2<Mohamed>[3] signifie qu'Amine (ID=3) est l'ami commun entre Sidi et Mohamed.

## Tests
Pour exécuter les tests :
python -m pytest tests/
Les tests vérifient :
Le parsing correct des données
La logique de calcul des amis communs
Les cas limites (utilisateurs sans amis, etc.)

## Développeur
Mekfoula El Bechir

## Licence
Ce projet est développé dans un cadre éducatif.

## Technologies Utilisées
Apache Spark : Framework de traitement distribué
PySpark : API Python pour Spark
Python : Langage de programmation principal

