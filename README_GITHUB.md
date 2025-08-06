# Liberation.fr RSS Feed - Benjamin Delille

🗞️ **Flux RSS automatique pour les articles de Benjamin Delille sur Liberation.fr**

[![Update RSS Feed](https://github.com/MartinDelille/liberation-rss-benjamin-delille/actions/workflows/update-rss.yml/badge.svg)](https://github.com/MartinDelille/liberation-rss-benjamin-delille/actions/workflows/update-rss.yml)

## 📡 Accès au flux RSS

**URL du flux :** `https://MartinDelille.github.io/liberation-rss-benjamin-delille/benjamin_delille_rss.xml`

**Site web :** `https://MartinDelille.github.io/liberation-rss-benjamin-delille/`

## 🎯 Pourquoi ce projet ?

Liberation.fr ne propose pas de flux RSS par auteur. Ce projet génère automatiquement un flux RSS pour Benjamin Delille en analysant sa page d'auteur.

## ⚙️ Comment ça marche

1. **GitHub Actions** exécute quotidiennement un script Python
2. Le script analyse la page de Benjamin Delille sur Liberation.fr
3. Il extrait les derniers articles et génère un fichier RSS valide
4. **GitHub Pages** publie le flux RSS et le site web

## 🚀 Configuration

### 1. Créer le repository GitHub

```bash
# Cloner ce dossier dans un nouveau repository
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/MartinDelille/liberation-rss-benjamin-delille.git
git push -u origin main
```

### 2. Activer GitHub Pages

1. Allez dans **Settings** > **Pages**
2. Source : **GitHub Actions**
3. Le site sera accessible à `https://MartinDelille.github.io/liberation-rss-benjamin-delille/`

### 3. Permissions GitHub Actions

Dans **Settings** > **Actions** > **General** :
- Cochez "Read and write permissions"
- Cochez "Allow GitHub Actions to create and approve pull requests"

## 📁 Structure du projet

```
.
├── .github/workflows/
│   └── update-rss.yml          # GitHub Actions workflow
├── generate_author_rss_v2.py   # Script de génération RSS
├── check_liberation_rss.py     # Script de vérification
├── index.html                  # Page web du flux
├── benjamin_delille_rss.xml    # Flux RSS généré
└── README.md                   # Ce fichier
```

## 🔄 Mise à jour

Le flux est automatiquement mis à jour :
- **Quotidiennement** à 8h UTC
- **Manuellement** via l'onglet Actions sur GitHub
- **À chaque push** sur la branche main

## 📱 Utilisation

### Lecteurs RSS recommandés :
- **Feedly** - Interface web
- **Inoreader** - Fonctionnalités avancées
- **NetNewsWire** - Mac/iOS
- **FreshRSS** - Auto-hébergé

### Ajouter le flux :
1. Copiez l'URL : `https://MartinDelille.github.io/liberation-rss-benjamin-delille/benjamin_delille_rss.xml`
2. Ajoutez-la dans votre lecteur RSS

## 🛠️ Développement local

```bash
# Installer les dépendances
pip install beautifulsoup4 requests

# Générer le flux RSS
python generate_author_rss_v2.py

# Le fichier benjamin_delille_rss.xml sera créé/mis à jour
```

## 📊 Fonctionnalités

- ✅ Génération automatique quotidienne
- ✅ Flux RSS 2.0 valide
- ✅ Interface web pour visualiser le flux
- ✅ Compatible avec tous les lecteurs RSS
- ✅ Gestion d'erreurs robuste
- ✅ Hébergement gratuit via GitHub Pages

## ⚠️ Limitations

- Dépend de la structure HTML de Liberation.fr
- Maximum 10 articles récents
- Mise à jour quotidienne (pas en temps réel)

## 🔧 Personnalisation

Pour adapter ce projet à un autre auteur :

1. Modifiez `generate_author_rss_v2.py` :
   ```python
   author_url = "https://www.liberation.fr/auteur/[autre-auteur]/"
   author_name = "Nom de l'auteur"
   ```

2. Mettez à jour `index.html` avec les nouvelles informations

## 📄 Licence

MIT License - Libre d'utilisation et modification

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter des fonctionnalités

---

**Note :** Ce projet n'est pas affilié à Liberation.fr. Il s'agit d'un outil indépendant pour faciliter l'accès aux articles via RSS.
