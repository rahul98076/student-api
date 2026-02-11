```markdown
# Student API (SRE Bootcamp)

A production-grade REST API for managing student records. This project is built to be "cloud-native," transitioning from local development to a distributed Kubernetes architecture managed via Helm and ArgoCD.

## GitOps Deployment (ArgoCD)

We use ArgoCD for continuous delivery. This is the preferred method for deploying the stack.

### Prerequisites

* Minikube cluster running.
* `kubectl` and `helm` installed.

### Setup Instructions

1. **Install ArgoCD:**

   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```
# Student API (SRE Bootcamp)

A production-grade REST API for managing student records. Designed to be cloud-native and deployable via Helm and ArgoCD.

<!-- TOC -->
- [Overview](#overview)
- [GitOps Deployment (ArgoCD)](#gitops-deployment-argocd)
- [Manual Kubernetes Deployment (Helm)](#manual-kubernetes-deployment-helm)
- [Observability Stack Setup](#observability-stack-setup)
- [Tech Stack](#tech-stack)
- [Local Development (Docker Compose)](#local-development-docker-compose)
- [API Endpoints](#api-endpoints)
- [Testing & Logging](#testing--logging)
- [Student Model](#student-model)
- [Contributing](#contributing)

## Overview

This repository contains a sample Student API used in the SRE Bootcamp. It demonstrates a full delivery lifecycle from local development (Docker Compose) to production-like Kubernetes deployments managed with Helm and ArgoCD.

## GitOps Deployment (ArgoCD)

ArgoCD is the recommended deployment method for continuous delivery.

### Prerequisites

- A running Kubernetes cluster (Minikube or a cloud provider)
- `kubectl` and `helm` installed locally

### Quick Setup

1. Install ArgoCD:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

2. Access the UI:

```bash
# Get the initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

# Port forward the server
kubectl port-forward svc/argocd-server -n argocd 8085:443
```

Open https://localhost:8085 in your browser.

3. Deploy the application manifests (example):

```bash
kubectl apply -f helm/argocd/applications.yaml
```

After this, ArgoCD will sync the desired state from the Git repository and deploy the stack.

## Manual Kubernetes Deployment (Helm)

This path is useful for debugging or when you prefer manual control.

### Architecture Highlights

- Multi-node separation (application, database, dependent services)
- Helm charts for package management and versioned releases
- Secrets managed via External Secrets Operator with HashiCorp Vault
- DB schema migrations run as an init container before the API pod starts
- The API runs with multiple replicas for availability

### Deployment Steps (summary)

1. Label nodes (optional):

```bash
kubectl label nodes sre-bootcamp type=application
kubectl label nodes sre-bootcamp-m02 type=database
kubectl label nodes sre-bootcamp-m03 type=dependent-services
```

2. Update Helm dependencies:

```bash
helm dependency update ./helm/vault
helm dependency update ./helm/postgres
helm dependency update ./helm/external-secrets
```

3. Install components in order:

```bash
# External Secrets Operator
helm upgrade --install external-secrets ./helm/external-secrets -n external-secrets --create-namespace

# Vault and Postgres
helm upgrade --install vault ./helm/vault -n vault --create-namespace
helm upgrade --install database ./helm/postgres -n student-api

# Student API
helm upgrade --install student-api ./helm/student-api -n student-api
```

4. Verify secrets and services:

```bash
kubectl get externalsecret -n student-api
kubectl get pods -n student-api
```

5. Port-forward API for local access:

```bash
kubectl port-forward svc/student-api 8082:8080 -n student-api
```

## Observability Stack Setup

### Components Overview

**Prometheus & Grafana**: Deployed via kube-prometheus-stack to collect metrics and visualize system health.

**Loki & Promtail**: PLG stack for log aggregation. Promtail is configured via pipeline stages to drop all logs except those from the student-api namespace.

**Postgres Exporter**: Bridges PostgreSQL internal stats to Prometheus metrics.

**Blackbox Exporter**: Monitors endpoint probes (uptime/latency) for the REST API and internal services.

### Deployment Instructions

1. Add required Helm repositories:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

2. Deploy the observability stack to the dedicated node (dependent_services):

```bash
helm install monitoring prometheus-community/kube-prometheus-stack -n observability -f helm/observability-values.yaml
helm install loki grafana/loki-stack -n observability -f helm/observability-values.yaml
helm install db-exporter prometheus-community/prometheus-postgres-exporter -n observability -f helm/observability-values.yaml
helm install blackbox prometheus-community/prometheus-blackbox-exporter -n observability -f helm/observability-values.yaml
```

### Verification & Access

**Check Scrape Targets**: Access the Prometheus UI to verify kube-state-metrics, node-exporter, and postgres-exporter are being scraped.

**Access Grafana**:

```bash
kubectl port-forward -n observability deployment/monitoring-grafana 3000:3000
```

Then open http://localhost:3000 in your browser.

**Data Sources**: Verify that both Loki (URL: `http://loki:3100`) and Prometheus (URL: `http://monitoring-kube-prometheus-prometheus:9090`) are configured as default data sources.

## Tech Stack

- Orchestration: Kubernetes (Minikube), Helm v3
- Local: Docker & Docker Compose
- CD / GitOps: ArgoCD
- Secrets: HashiCorp Vault & External Secrets Operator
- Language: Python 3.14 (Flask)
- Database: PostgreSQL 15 (Bitnami Helm Chart)
- CI: GitHub Actions (self-hosted runners optional)

## Local Development (Docker Compose)

Run a lightweight local environment for fast iteration.

### Prerequisites

- Docker & Docker Compose
- GNU `make`

### Quick Start

```bash
make setup   # install helpers and prerequisites
make start   # start API, DB, and apply migrations
```

Common make targets:

| Command | Description |
| :--- | :--- |
| `make up` | Start services in detached mode |
| `make down` | Stop services |
| `make migrate` | Run DB migrations inside the container |
| `make test` | Run unit tests with pytest |

## API Endpoints

All endpoints are versioned under `/api/v1`.

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/healthcheck` | Service health status |
| GET | `/api/v1/students` | List all students |
| POST | `/api/v1/students` | Create a new student |
| GET | `/api/v1/students/<id>` | Retrieve a student by ID |
| PUT | `/api/v1/students/<id>` | Update a student's details |
| DELETE | `/api/v1/students/<id>` | Delete a student record |

## Testing & Logging

- Unit tests: `make test` (pytest)
- Logging: structured logs (INFO/DEBUG) for observability and troubleshooting

## Student Model

The `Student` model contains the following fields:

- `id` (primary key)
- `first_name`, `last_name`
- `grade`
- `email` (unique)


