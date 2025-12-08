#!/bin/bash

echo "🚀 Démarrage de PipelineGuard Enterprise"
echo "========================================"
echo ""

# Vérifier si Kafka et Zookeeper sont en cours d'exécution
echo "📦 Vérification des services Docker..."
if ! docker ps | grep -q "zookeeper"; then
    echo "⚠️  Zookeeper n'est pas en cours d'exécution. Démarrage..."
    docker start zookeeper
    sleep 3
fi

if ! docker ps | grep -q "kafka"; then
    echo "⚠️  Kafka n'est pas en cours d'exécution. Démarrage..."
    docker start kafka
    sleep 5
fi

echo "✅ Services Docker démarrés"
echo ""

# Initialiser la base de données
echo "🗄️  Initialisation de la base de données..."
cd backend
python init_db.py

echo ""
echo "✅ Configuration terminée!"
echo ""
echo "📋 Instructions pour démarrer l'application:"
echo ""
echo "1️⃣  Backend (nouveau terminal):"
echo "   cd backend"
echo "   uvicorn main:app --reload"
echo ""
echo "2️⃣  Frontend (nouveau terminal):"
echo "   cd front/projet"
echo "   ng serve"
echo ""
echo "3️⃣  Ouvrir http://localhost:4200 dans votre navigateur"
echo ""
echo "🎉 Prêt à démarrer!"
