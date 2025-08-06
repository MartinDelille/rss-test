#!/bin/bash

# Setup script for Liberation.fr RSS Feed GitHub Pages deployment

echo "🗞️  Configuration du flux RSS Benjamin Delille pour GitHub Pages"
echo "=================================================================="

# Get GitHub username
read -p "Entrez votre nom d'utilisateur GitHub: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Nom d'utilisateur requis!"
    exit 1
fi

REPO_NAME="liberation-rss-benjamin-delille"
GITHUB_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
PAGES_URL="https://${GITHUB_USERNAME}.github.io/${REPO_NAME}"

echo ""
echo "📝 Configuration:"
echo "   Repository: $REPO_NAME"
echo "   GitHub URL: $GITHUB_URL" 
echo "   Pages URL: $PAGES_URL"
echo ""

# Update URLs in files
echo "🔧 Mise à jour des URLs dans les fichiers..."

# Update index.html
sed -i.bak "s|\[votre-username\]|$GITHUB_USERNAME|g" index.html
rm index.html.bak

# Update README_GITHUB.md
sed -i.bak "s|\[votre-username\]|$GITHUB_USERNAME|g" README_GITHUB.md
rm README_GITHUB.md.bak

echo "✅ URLs mises à jour"

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "🔄 Initialisation du repository Git..."
    git init
    git branch -M main
    echo "✅ Git initialisé"
fi

# Add all files
echo "📦 Ajout des fichiers..."
git add .
git commit -m "Initial commit: Liberation.fr RSS feed for Benjamin Delille"

echo ""
echo "🚀 Étapes suivantes:"
echo ""
echo "1. Créez le repository sur GitHub:"
echo "   https://github.com/new"
echo "   Nom: $REPO_NAME"
echo "   Public ✅"
echo "   N'ajoutez pas de README, .gitignore ou licence"
echo ""
echo "2. Connectez ce dossier au repository:"
echo "   git remote add origin $GITHUB_URL.git"
echo "   git push -u origin main"
echo ""
echo "3. Activez GitHub Pages:"
echo "   Allez dans Settings > Pages"
echo "   Source: GitHub Actions"
echo ""
echo "4. Configurez les permissions:"
echo "   Settings > Actions > General"
echo "   ✅ Read and write permissions"
echo "   ✅ Allow GitHub Actions to create and approve pull requests"
echo ""
echo "5. Votre flux RSS sera disponible à:"
echo "   $PAGES_URL/benjamin_delille_rss.xml"
echo ""
echo "🎉 Configuration terminée!"
echo ""
echo "💡 Commandes utiles:"
echo "   git remote add origin $GITHUB_URL.git"
echo "   git push -u origin main"
