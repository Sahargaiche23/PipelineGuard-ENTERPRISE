# 📊 PipelineGuard Enterprise - Guide Monitoring Prometheus & Grafana

## 🎯 Vue d'ensemble

Ce guide vous explique comment accéder, configurer et utiliser **Prometheus** et **Grafana** pour monitorer votre application PipelineGuard.

---

## 🚀 Étape 1 : Démarrer les Services

### Vérifier que Docker Compose est lancé

```bash
# Depuis la racine du projet
cd "/home/sahar/Bureau/Stage (Copie 2)"

# Démarrer tous les services (si pas déjà fait)
docker-compose up -d

# Vérifier que Prometheus et Grafana sont actifs
docker-compose ps | grep -E 'prometheus|grafana'
```

**Vous devriez voir** :
```
pipelineguard_prometheus   Up   9090/tcp
pipelineguard_grafana      Up   3000/tcp
```

### Si les services ne sont pas actifs

```bash
# Redémarrer uniquement Prometheus et Grafana
docker-compose restart prometheus grafana

# Voir les logs en cas de problème
docker-compose logs -f prometheus
docker-compose logs -f grafana
```

---

## 📊 Étape 2 : Accéder à Prometheus

### Ouvrir Prometheus

**URL** : http://localhost:9090

### Interface Prometheus

Prometheus vous permet de :
1. **Requêter les métriques** en temps réel
2. **Visualiser les graphes** des métriques
3. **Vérifier les targets** (services monitorés)

### Vérifier les Targets (Services Monitorés)

1. Cliquez sur **Status** → **Targets** dans le menu
2. Vous devriez voir :
   - **node-exporter** (localhost:9100) - État : UP ✅
   - **backend** (backend:8000) - État : UP ou DOWN selon si endpoint /metrics existe

### Exemples de Requêtes Prometheus

#### 1. Métriques Système (CPU)

```promql
# Utilisation CPU en pourcentage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

**Comment utiliser** :
1. Allez dans l'onglet **Graph**
2. Collez la requête dans le champ de recherche
3. Cliquez sur **Execute**
4. Vous verrez le graphe d'utilisation CPU

#### 2. Mémoire Disponible

```promql
# Mémoire disponible en Mo
node_memory_MemAvailable_bytes / 1024 / 1024
```

#### 3. Espace Disque Disponible

```promql
# Espace disque disponible en Go
node_filesystem_avail_bytes{mountpoint="/"} / 1024 / 1024 / 1024
```

#### 4. Requêtes HTTP par seconde (si métrique existe)

```promql
# Rate de requêtes HTTP
rate(http_requests_total[5m])
```

#### 5. Latence des requêtes (si métrique existe)

```promql
# Latence moyenne en secondes
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```

### Créer des Alertes Prometheus (Optionnel)

Créez le fichier `/home/sahar/Bureau/Stage (Copie 2)/monitoring/alert.rules.yml` :

```yaml
groups:
  - name: pipelineguard_alerts
    interval: 30s
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU usage is above 80%"
          
      - alert: LowDiskSpace
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disk space is below 10%"
          
      - alert: HighMemoryUsage
        expr: (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 90
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Memory usage is above 90%"
```

---

## 📈 Étape 3 : Accéder à Grafana

### Ouvrir Grafana

**URL** : http://localhost:3000

### Première Connexion

**Identifiants par défaut** :
- **Username** : `admin`
- **Password** : `admin123`

⚠️ **Note** : Grafana vous demandera peut-être de changer le mot de passe lors de la première connexion.

---

## 🔧 Étape 4 : Configurer Grafana

### 4.1 : Ajouter Prometheus comme Data Source

1. **Cliquez sur** l'icône ⚙️ (Gear) dans le menu gauche → **Data Sources**
2. **Cliquez sur** "Add data source"
3. **Sélectionnez** "Prometheus"
4. **Configurez** :
   - **Name** : `Prometheus`
   - **URL** : `http://prometheus:9090` (nom du service Docker)
   - **Access** : `Server (default)`
5. **Cliquez sur** "Save & Test"
6. Vous devriez voir : ✅ **"Data source is working"**

### 4.2 : Créer votre Premier Dashboard

#### Option A : Dashboard Système Complet

1. Cliquez sur **+ (Plus)** → **Import**
2. Entrez l'ID du dashboard : **1860** (Node Exporter Full)
3. Cliquez sur **Load**
4. Sélectionnez **Prometheus** comme data source
5. Cliquez sur **Import**

**Résultat** : Dashboard complet avec CPU, RAM, Disque, Réseau, etc.

#### Option B : Dashboard Custom PipelineGuard

1. Cliquez sur **+ (Plus)** → **Dashboard**
2. Cliquez sur **Add new panel**

##### Panel 1 : CPU Usage

**Query** :
```promql
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

**Configuration** :
- **Panel title** : "CPU Usage (%)"
- **Visualization** : Graph ou Gauge
- **Unit** : Percent (0-100)
- **Thresholds** : 
  - 🟢 Green : 0-70%
  - 🟡 Yellow : 70-85%
  - 🔴 Red : 85-100%

##### Panel 2 : Memory Usage

**Query** :
```promql
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

**Configuration** :
- **Panel title** : "Memory Usage (%)"
- **Visualization** : Gauge
- **Unit** : Percent (0-100)

##### Panel 3 : Disk Space

**Query** :
```promql
(node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100
```

**Configuration** :
- **Panel title** : "Disk Available (%)"
- **Visualization** : Bar gauge
- **Unit** : Percent (0-100)

##### Panel 4 : Network Traffic

**Query RX (Received)** :
```promql
rate(node_network_receive_bytes_total{device!="lo"}[5m])
```

**Query TX (Transmitted)** :
```promql
rate(node_network_transmit_bytes_total{device!="lo"}[5m])
```

**Configuration** :
- **Panel title** : "Network Traffic"
- **Visualization** : Time series
- **Unit** : bytes/sec

3. **Cliquez sur** "Save dashboard"
4. **Nommez-le** : "PipelineGuard System Monitoring"

---

## 📊 Étape 5 : Métriques Application (Backend)

### Ajouter des Métriques FastAPI

Pour monitorer votre backend FastAPI, vous devez ajouter des métriques Prometheus.

#### 5.1 : Installer prometheus-fastapi-instrumentator

```bash
cd backend
source venv/bin/activate
pip install prometheus-fastapi-instrumentator
pip freeze > requirements.txt
```

#### 5.2 : Modifier main.py

Ajoutez ces lignes au début de votre `backend/main.py` :

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# ... (votre configuration CORS, etc.)

# Activer les métriques Prometheus
Instrumentator().instrument(app).expose(app)
```

**Ce que ça fait** :
- Ajoute automatiquement l'endpoint `/metrics`
- Collecte métriques HTTP : nombre de requêtes, latence, codes status
- Compatible avec Prometheus scraping

#### 5.3 : Redémarrer le Backend

```bash
# Si développement local
uvicorn main:app --reload

# Si Docker
docker-compose restart backend
```

#### 5.4 : Vérifier l'endpoint /metrics

Ouvrez : http://localhost:8000/metrics

Vous devriez voir des métriques comme :
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",path="/profile"} 42

# HELP http_request_duration_seconds HTTP request latency
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{le="0.1"} 150
```

---

## 📈 Étape 6 : Dashboards Avancés

### Dashboard Application Performance

Créez un nouveau dashboard avec ces panels :

#### Panel 1 : Requêtes par Endpoint

**Query** :
```promql
sum by (path) (rate(http_requests_total[5m]))
```

**Visualization** : Bar chart

#### Panel 2 : Latence P95

**Query** :
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

**Visualization** : Time series

#### Panel 3 : Taux d'Erreurs

**Query** :
```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100
```

**Visualization** : Stat panel avec threshold

#### Panel 4 : Requêtes Actives WebSocket

**Query** (à créer dans votre code) :
```promql
websocket_connections_active
```

---

## 🔔 Étape 7 : Alertes Grafana

### Configurer une Alerte

1. **Ouvrez un panel** existant (ex: CPU Usage)
2. **Cliquez sur** l'onglet **Alert**
3. **Cliquez sur** "Create alert rule from this panel"
4. **Configurez** :
   - **Alert name** : "High CPU Usage"
   - **Condition** : `WHEN avg() OF query(A, 5m) IS ABOVE 80`
   - **Evaluate every** : `1m`
   - **For** : `5m`
5. **Notifications** :
   - Créez un contact point (Email, Slack, etc.)
6. **Save**

---

## 🛠️ Étape 8 : Commandes Utiles

### Prometheus

```bash
# Vérifier que Prometheus est actif
curl http://localhost:9090/-/healthy

# Voir la configuration Prometheus
docker exec pipelineguard_prometheus cat /etc/prometheus/prometheus.yml

# Recharger la configuration sans redémarrer
curl -X POST http://localhost:9090/-/reload
```

### Grafana

```bash
# Réinitialiser le mot de passe admin
docker exec -it pipelineguard_grafana grafana-cli admin reset-admin-password newpassword

# Voir les logs Grafana
docker-compose logs -f grafana

# Backup des dashboards
docker exec pipelineguard_grafana tar -czf /var/lib/grafana/backup.tar.gz /var/lib/grafana/grafana.db
```

---

## 📊 Étape 9 : Exemples de Dashboards

### Dashboard 1 : Vue d'Ensemble Système

| Métrique | Query | Visualization |
|----------|-------|---------------|
| CPU | `100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` | Gauge |
| RAM | `(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100` | Gauge |
| Disk | `(node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100` | Gauge |
| Uptime | `node_time_seconds - node_boot_time_seconds` | Stat |

### Dashboard 2 : Application Backend

| Métrique | Query | Visualization |
|----------|-------|---------------|
| Requests/sec | `sum(rate(http_requests_total[5m]))` | Graph |
| Avg Latency | `rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])` | Graph |
| Error Rate | `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100` | Stat |
| Active Users | Custom counter | Stat |

---

## 🎯 Résumé des URLs

| Service | URL | Identifiants |
|---------|-----|--------------|
| **Prometheus** | http://localhost:9090 | Aucun |
| **Grafana** | http://localhost:3000 | admin/admin123 |
| **Node Exporter** | http://localhost:9100/metrics | Aucun |
| **Backend Metrics** | http://localhost:8000/metrics | Aucun (après config) |

---

## 🚨 Troubleshooting

### Prometheus ne voit pas les targets

**Problème** : Target backend en DOWN dans Prometheus

**Solution** :
```bash
# Vérifier que le backend expose /metrics
curl http://localhost:8000/metrics

# Vérifier la config Prometheus
cat monitoring/prometheus.yml
```

### Grafana : "Data source is not working"

**Solution** :
```bash
# Utiliser le nom du service Docker (pas localhost)
# URL doit être : http://prometheus:9090
```

### Pas de métriques système

**Solution** :
```bash
# Vérifier que node-exporter est actif
docker-compose ps node-exporter

# Redémarrer si besoin
docker-compose restart node-exporter
```

---

## 📚 Ressources

- **Prometheus Queries** : https://prometheus.io/docs/prometheus/latest/querying/basics/
- **Grafana Dashboards** : https://grafana.com/grafana/dashboards/
- **Node Exporter Dashboard** : ID 1860
- **FastAPI Instrumentator** : https://github.com/trallnag/prometheus-fastapi-instrumentator

---

## ✅ Checklist Finale

- [ ] Services Prometheus et Grafana démarrés
- [ ] Prometheus accessible sur :9090
- [ ] Grafana accessible sur :3000
- [ ] Data source Prometheus configuré dans Grafana
- [ ] Dashboard système importé (ID 1860)
- [ ] Métriques backend ajoutées (instrumentator)
- [ ] Endpoint /metrics accessible
- [ ] Dashboard custom créé
- [ ] Alertes configurées (optionnel)

---

**Félicitations ! Votre monitoring est opérationnel ! 🎉**
