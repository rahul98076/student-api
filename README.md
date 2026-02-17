# Student API (SRE Bootcamp)

This README documents the complete setup and deployment process for the Student API project, covering:
- **Milestone 7**: Kubernetes deployment with consolidated manifests
- **Milestone 8**: Helm-based deployment with External Secrets Operator integration

## Quick Start (Helm Deployment - Milestone 8)

For the complete Helm-based deployment (recommended), skip to section 13.

## Detailed Setup Steps

The following sections document both raw manifest deployment (milestone 7) and Helm deployment (milestone 8).

## 1) Prerequisites installed

- Docker
- Python 3.x
- Make
- Git
- Minikube
- kubectl
- Helm

## 2) Local setup (one-click)

```bash
make setup
```

Optional local run:

```bash
make start
```

## 3) Create a 3-node Minikube cluster

```bash
minikube start --nodes 3
```

Confirm nodes:

```bash
kubectl get nodes -o wide
```

## 4) Label the nodes

Replace node names with those from `kubectl get nodes -o wide`.

```bash
kubectl label node minikube type=application
kubectl label node minikube-m02 type=database
kubectl label node minikube-m03 type=dependent_services
```

Verify labels:

```bash
kubectl get nodes --show-labels
```

## 5) Apply Kubernetes manifests (first pass)

```bash
kubectl apply -f k8s/namespaces.yaml
kubectl apply -f k8s/vault/vault.yaml
kubectl apply -f k8s/database/database.yaml
kubectl apply -f k8s/application/application.yaml
```

Result: core resources applied, ESO resources failed because CRDs were missing.

## 6) Install External Secrets Operator (ESO)

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm repo update

kubectl create namespace external-secrets
helm install external-secrets external-secrets/external-secrets \
	-n external-secrets
```

Verify CRDs and controller:

```bash
kubectl get crd | grep external-secrets
kubectl get pods -n external-secrets
```

## 7) Re-apply app manifest (to create SecretStore/ExternalSecret)

```bash
kubectl apply -f k8s/application/application.yaml
```

## 8) Seed Vault with DB credentials

Vault runs in dev mode with root token `root`. The Vault pod name will be `vault-0` when deployed via Helm.

```bash
kubectl get pods -n vault
kubectl exec -it -n vault vault-0 -- /bin/sh -c '
	export VAULT_ADDR=http://127.0.0.1:8200
	export VAULT_TOKEN=root
	vault kv put secret/student-api/db-creds username=postgres password=password
'
```

Verify the secret:

```bash
kubectl exec -it -n vault vault-0 -- /bin/sh -c '
	export VAULT_ADDR=http://127.0.0.1:8200
	export VAULT_TOKEN=root
	vault kv get secret/student-api/db-creds
'
```

## 9) Verify ESO sync

```bash
kubectl get externalsecret -n student-api
kubectl get secret db-creds-final -n student-api -o yaml
```

## 10) Restart app deployment (if needed)

```bash
kubectl rollout restart deployment/student-api -n student-api
```

## 11) Basic cluster checks

```bash
kubectl get deploy,svc,pods -n student-api
```

## 12) API verification (Postman)

Use the included Postman collection and confirm 200 responses for:

- `/healthcheck`
- `/api/v1/students`

## 13) Helm-only deployment (milestone 8)

Deploy the full stack with Helm charts (no raw manifests):

### Chart versions used:
- External Secrets Operator: 2.0.0
- HashiCorp Vault: 0.32.0
- Bitnami PostgreSQL: 16.5.5

### Setup Helm repositories:

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Update chart dependencies:

```bash
helm dependency update ./helm/external-secrets
helm dependency update ./helm/vault
helm dependency update ./helm/postgres
helm dependency update ./helm/student-api
```

### Deploy components in order:

1. **Deploy External Secrets Operator:**

```bash
helm upgrade --install external-secrets ./helm/external-secrets \
	-n external-secrets --create-namespace
```

2. **Deploy Vault:**

```bash
helm upgrade --install vault ./helm/vault \
	-n vault --create-namespace
```

Wait for Vault to be ready:

```bash
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=vault -n vault --timeout=120s
```

3. **Seed Vault with DB credentials:**

```bash
kubectl exec -it -n vault vault-0 -- /bin/sh -c '
	export VAULT_ADDR=http://127.0.0.1:8200
	export VAULT_TOKEN=root
	vault kv put secret/student-api/db-creds username=postgres password=password
'
```

Verify the secret was stored:

```bash
kubectl exec -it -n vault vault-0 -- /bin/sh -c '
	export VAULT_ADDR=http://127.0.0.1:8200
	export VAULT_TOKEN=root
	vault kv get secret/student-api/db-creds
'
```

4. **Deploy PostgreSQL:**

> **Note:** PostgreSQL is configured with `persistence.enabled: false` to avoid PVC issues in Minikube. For production, enable persistence.

```bash
helm upgrade --install postgres ./helm/postgres \
	-n student-api --create-namespace
```

Wait for PostgreSQL to be ready:

```bash
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=postgresql -n student-api --timeout=120s
```

5. **Deploy Student API:**

> **Important:** The database hostname is configured as `postgres-postgresql` (Bitnami's service naming convention).

```bash
helm upgrade --install student-api ./helm/student-api \
	-n student-api
```

### Verify the deployment:

Check all pods are running:

```bash
kubectl get pods -n vault
kubectl get pods -n external-secrets
kubectl get pods -n student-api
```

Verify ESO SecretStore and ExternalSecret:

```bash
kubectl get secretstore,externalsecret -n student-api
kubectl get secret db-creds-final -n student-api -o jsonpath='{.data.username}' | base64 -d && echo
```

Test the API:

```bash
# Get Minikube IP
minikube ip

# Test healthcheck
curl http://$(minikube ip):30001/healthcheck

# Test students endpoint
curl http://$(minikube ip):30001/api/v1/students

# Create a student
curl -X POST http://$(minikube ip):30001/api/v1/students \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "grade": "A", "email": "john@example.com"}'
```

## 14) ArgoCD one-click deployments (milestone 9)

ArgoCD is installed from a declarative manifest and bootstrapped using the app-of-apps pattern.

### Install ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -k k8s/argocd
```

Wait for ArgoCD components to be ready:

```bash
kubectl get pods -n argocd
```

### Bootstrap apps (app-of-apps)

```bash
kubectl apply -f k8s/argocd/root-app.yaml
```

This will create the following ArgoCD apps (all from Helm charts):
- External Secrets Operator
- Vault
- PostgreSQL
- Student API

> Observability app is intentionally omitted until milestone 10.

ArgoCD tracks the `ci-updates` branch for the root app and child apps so it can continuously deploy the image tag updates pushed by CI.

### CI-driven image tag updates

The GitHub Actions workflow updates the Student API chart image tag and pushes to the `ci-updates` branch on every non-tag build.

Required GitHub secrets:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

Workflow behavior:
- Tags release builds with `v*.*.*` when you push a Git tag.
- For regular pushes, the image tag is the short commit SHA.
- The workflow updates `helm/student-api/values.yaml` and pushes to `ci-updates`.

### Access ArgoCD UI (optional)

```bash
kubectl port-forward -n argocd svc/argocd-server 8081:443
```

Default username: `admin`

Get the initial password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
	-o jsonpath='{.data.password}' | base64 -d && echo
```

### Verify ArgoCD sync

```bash
kubectl get applications -n argocd
```

ArgoCD is pinned to the `dependent_services` node via `nodeSelector` in the install manifest.
The `install.yaml` file is upstream and not modified; node selectors are applied via kustomize patches in k8s/argocd/patches.

## 15) Observability stack (milestone 10)

This stack deploys Prometheus, Grafana, Loki, Promtail, blackbox exporter, and Postgres exporter in the `observability` namespace.

### Add Helm repositories

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

### Update chart dependencies

```bash
helm dependency update ./helm/observability
```

### Deploy the observability stack

```bash
helm upgrade --install observability ./helm/observability \
	-n observability --create-namespace
```

### Verify the deployment

```bash
kubectl get pods -n observability
kubectl get svc -n observability
```

### Access Grafana and Prometheus

```bash
kubectl port-forward -n observability svc/observability-grafana 3000:80
kubectl port-forward -n observability svc/observability-kube-prometheus-stack-prometheus 9090:9090
```

Grafana login:
- Username: `admin`
- Password: `admin`

### Notes

- Update Postgres credentials in [helm/observability/values.yaml](helm/observability/values.yaml) if they differ from the defaults.
- Promtail is scoped to only the `student-api` namespace and `app=student-api` pods.
- Blackbox exporter probes internal endpoints for Student API, Vault, and ArgoCD.

## 16) Dashboards & alerts (milestone 11)

Grafana dashboards and Prometheus alert rules are provisioned by the observability chart.

### Dashboards

Dashboards are created from ConfigMaps in the `observability` namespace and should appear automatically in Grafana:
- Student DB Metrics
- Student API Error Logs
- Node Metrics
- Kube-State Metrics
- Blackbox Metrics

### Alerts

Prometheus rules are created via a `PrometheusRule` resource. Verify they exist:

```bash
kubectl get prometheusrules -n observability
```

### Slack notifications

Update the Slack webhook placeholder in [helm/observability/values.yaml](helm/observability/values.yaml) and re-deploy:

```bash
helm upgrade --install observability ./helm/observability \
	-n observability
```

> The `HighRequestRate` alert assumes application request metrics are available. If you add app Prometheus metrics later, this alert will begin firing appropriately.

## Current status (Milestone 9 Complete)

✅ **All components deployed via Helm:**
- External Secrets Operator (v2.0.0) - syncing secrets from Vault
- HashiCorp Vault (v0.32.0) - dev mode with root token
- Bitnami PostgreSQL (16.5.5) - running without persistence
- Student API - running with migrations completed

✅ **ArgoCD GitOps deployment:**
- ArgoCD installed from declarative manifest
- App-of-apps bootstraps Helm-based deployments
- Auto-sync enabled for apps

✅ **Key configurations:**
- PostgreSQL persistence disabled (for Minikube compatibility)
- Database hostname: `postgres-postgresql`
- Vault token stored in Secret: `vault-backend-token`
- DB credentials synced to: `db-creds-final`
- API exposed via NodePort: 30001

### Troubleshooting:

If pods are not running, check:

```bash
# Check ESO connectivity to Vault
kubectl describe secretstore vault-backend -n student-api

# Check external secret sync status
kubectl describe externalsecret db-creds-sync -n student-api

# Check application logs
kubectl logs -n student-api deployment/student-api --tail=50

# Check database logs
kubectl logs -n student-api postgres-postgresql-0 --tail=50

# Restart ESO if needed
kubectl rollout restart deployment -n external-secrets external-secrets-external-secrets
```
