📜​ | Alpha est un générateur de wordlists basées sur les informations dont vous disposez sur quelqu'un. Votre mot de passe n'est pas dans rockyou et vous pensez que vous êtes protégé ? Alpha est là pour vous faire vous poser des questions sur votre sécurité sur Internet ;).
Car oui, aussi bête que cela puisse paraître, la majorité des gens mettent des détails open source dans leur mot de passe comme leur prénom, leur pseudo, leur date de naissance ou autre information personnelle. Grâce à Alpha, le peu d'informations dont vous disposez sur quelqu'un peut s'avérer cacher un mot de passe.

Alpha propose 4 niveau de création de wordlists : 
- Niveau 1 (avec le flag "-1") : Basique : mots simples, aucune mutation
- Niveau 2 (avec le flag "-2") : Mutations simples, suffixes
- Niveau 3 (avec le flag "-3") : Leet speak, mutations avancées
- Niveau MAX (avec le flag -max) : Tout activé (leet, permutations, mix...)

### **Cet outil s'utilise sur linux de préférence.**

# Installation sous linux

## ✅ Prérequis
1. Avoir Python 3 installé, sur Kali c’est déjà le cas. Sinon :
`sudo apt install python3 python3-venv`

## 🔧 Étapes d’installation

### 📁 1. Créer un environnement virtuel pour les dépendances

`python3 -m venv ~/alpha-env`
`source ~/alpha-env/bin/activate`

### 📦 2. Installer les bibliothèques nécessaires

`pip install rich tqdm`

### 📝 3. Créer le script Python

Crée un fichier appelé `alpha_script.py` :

`nano ~/alpha-env/alpha_script.py`

Colle le script python > Ctrl + O > Entrée > Ctrl + X

### 🚀 4. Créer un exécutable système

1. Crée un fichier appelé `alpha` :
    
`sudo nano /usr/local/bin/alpha`

2. Colle dedans ce petit **lanceur** :
    
`#!/bin/bash source ~/alpha-env/bin/activate python ~/alpha-env/alpha_script.py "$@"`

3. Rends-le exécutable :
    
`sudo chmod +x /usr/local/bin/alpha`



Maintenant, tu peux lancer le tool avec `alpha -h` pour voir  le help

# Utiliser alpha sous Windows

Pour utiliser Alpha sous Linux, vous devez faire le commande suivante (vérifiez que l'installation ci-dessu à bien été effectuée) : `python alpha -<flag(s)>` 

# Utiliser alpha sous Windows

Pour utiliser Alpha sous Windows, vous devez faire le commande suivante : `python alpha.py -<flag(s)>` 
