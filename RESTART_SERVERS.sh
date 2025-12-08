#!/bin/bash

echo "🔄 Redémarrage de PipelineGuard Enterprise"
echo "=========================================="
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Vérifier Docker
echo "📦 Vérification Docker..."
if ! docker ps &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas démarré${NC}"
    exit 1
fi

# 2. Redémarrer Kafka et Zookeeper
echo "🔄 Redémarrage Kafka et Zookeeper..."
docker restart zookeeper 2>/dev/null || docker start zookeeper
sleep 3
docker restart kafka2 2>/dev/null || docker start kafka2
sleep 5

# Vérifier que les conteneurs tournent
if docker ps | grep -q "zookeeper" && docker ps | grep -q "kafka2"; then
    echo -e "${GREEN}✅ Docker containers OK${NC}"
else
    echo -e "${RED}❌ Problème avec Docker containers${NC}"
    exit 1
fi

# 3. Arrêter les anciens processus backend/frontend
echo "🛑 Arrêt des anciens processus..."
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "ng serve" 2>/dev/null
sleep 2

# 4. Nettoyer et réinitialiser
echo "🧹 Nettoyage..."
cd backend
rm -f pipelineguard.db 2>/dev/null
rm -rf __pycache__ 2>/dev/null

# 5. Réinitialiser la base de données
echo "🗄️  Réinitialisation de la base de données..."
python3 init_db.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Base de données initialisée${NC}"
else
    echo -e "${RED}❌ Erreur initialisation DB${NC}"
    exit 1
fi

cd ..

echo ""
echo -e "${GREEN}✅ Préparation terminée!${NC}"
echo ""
echo "📋 Maintenant, dans 2 terminaux séparés:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd front/projet"
echo "  ng serve --port 4200"
echo ""
echo "Puis ouvrez: http://localhost:4200"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT: Utilisez des subreddits VALIDES pour les tests:${NC}"
echo "  ✅ python, angular, fastapi, programming, webdev"
echo "  ❌ facebook, instagram (ce ne sont PAS des subreddits!)"
