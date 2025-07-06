#!/bin/bash

# Script de démarrage pour PipelineGuard Enterprise
# Ce script démarre tous les services nécessaires

echo "🚀 Démarrage de PipelineGuard Enterprise..."

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier que Docker est installé et fonctionne
if ! command -v docker &> /dev/null; then
    log_error "Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

if ! docker info &> /dev/null; then
    log_error "Docker n'est pas démarré. Veuillez le démarrer avec 'sudo systemctl start docker'"
    exit 1
fi

# Arrêter les services existants s'ils tournent
log_info "Arrêt des services existants..."
sudo docker-compose -f docker-compose.local.yml down 2>/dev/null || true

# Démarrer les services de base
log_info "Démarrage des services de base (PostgreSQL, Redis, Kafka, Prometheus, Grafana)..."
sudo docker-compose -f docker-compose.local.yml up -d

# Attendre que PostgreSQL soit prêt
log_info "Attente que PostgreSQL soit prêt..."
timeout=60
while ! sudo docker exec pipelineguard_db pg_isready -U postgres &>/dev/null; do
    sleep 2
    timeout=$((timeout - 2))
    if [ $timeout -le 0 ]; then
        log_error "PostgreSQL n'a pas démarré dans les temps"
        exit 1
    fi
done
log_success "PostgreSQL est prêt"

# Démarrer le backend FastAPI
log_info "Démarrage du backend FastAPI..."
cd backend
if [ ! -d "venv" ]; then
    log_info "Création de l'environnement virtuel Python..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt &>/dev/null
export DATABASE_URL="postgresql://postgres:123@localhost:5433/redditdb"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

log_success "Backend démarré (PID: $BACKEND_PID)"

# Démarrer le frontend Angular
log_info "Démarrage du frontend Angular..."
cd front/projet
if [ ! -d "node_modules" ]; then
    log_info "Installation des dépendances Node.js..."
    npm install &>/dev/null
fi

ng serve --host 0.0.0.0 --port 4200 &
FRONTEND_PID=$!
cd ../..

log_success "Frontend démarré (PID: $FRONTEND_PID)"

# Attendre un peu puis afficher le statut
sleep 5

echo
log_success "🎉 PipelineGuard Enterprise est maintenant en cours d'exécution !"
echo
echo "📋 Services disponibles :"
echo "   🌐 Frontend Angular    : http://localhost:4200"
echo "   🔧 Backend FastAPI     : http://localhost:8000"
echo "   📊 Grafana            : http://localhost:3000 (admin/admin123)"
echo "   📈 Prometheus         : http://localhost:9090"
echo "   💾 PostgreSQL        : localhost:5433"
echo "   🔴 Redis              : localhost:6379"
echo "   📨 Kafka              : localhost:9092"
echo
echo "📖 Documentation API : http://localhost:8000/docs"
echo "📊 Métriques         : http://localhost:8000/metrics"
echo
log_info "Pour arrêter tous les services, appuyez sur Ctrl+C"

# Fonction pour nettoyer lors de l'arrêt
cleanup() {
    echo
    log_info "Arrêt des services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    sudo docker-compose -f docker-compose.local.yml down
    log_success "Tous les services ont été arrêtés"
    exit 0
}

# Trap pour nettoyer proprement
trap cleanup SIGINT SIGTERM

# Attendre indéfiniment
wait
