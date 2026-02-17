

# Student API (SRE Bootcamp)

A production-grade REST API for managing student records. This project is cloud-native and can be run locally (Docker Compose) or deployed to Kubernetes using Helm and ArgoCD.

## Table of contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick start (local)](#quick-start-local)
- [GitOps (ArgoCD)](#gitops-argocd)
- [Manual Helm deploy](#manual-helm-deploy)
- [Observability](#observability)
- [API Endpoints](#api-endpoints)
- [Testing & Logging](#testing--logging)
- [Student model](#student-model)

## Overview

This repository contains a sample Student API used in the [SRE Bootcamp by One2N](https://one2n.io/sre-bootcamp). It demonstrates a full delivery lifecycle from local development to Kubernetes deployments managed with Helm and ArgoCD.

## Prerequisites

- Docker & Docker Compose (for local development)
- Python 3.9+ (development), GNU `make`
- A Kubernetes cluster (Minikube or cloud) with `kubectl` and `helm` (for cluster deployments)

## Quick start (local)

Start a lightweight development environment with Docker Compose.

Run these commands:

```bash
make setup
make start
```

What they do:

- `make setup` — install helpers and prerequisites
- `make start` — start API, DB, and apply migrations

Useful targets:

- `make up` — Start services in detached mode
- `make down` — Stop services
- `make migrate` — Run DB migrations inside the container
- `make test` — Run unit tests with pytest

## GitOps (ArgoCD)

ArgoCD is the recommended continuous delivery method. To install and access ArgoCD, run:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Get the initial admin password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

Port-forward the server to access the UI locally:

```bash
kubectl port-forward svc/argocd-server -n argocd 8085:443
```

Open https://localhost:8085 and deploy the application manifests, for example:

```bash
kubectl apply -f helm/argocd/applications.yaml
```

ArgoCD will sync the repository state and manage your cluster deployments.

## Manual Helm deploy

Use Helm when you prefer manual control or for debugging. Typical deploy order:

1. Update chart dependencies:

```bash
helm dependency update ./helm/vault
helm dependency update ./helm/postgres
helm dependency update ./helm/external-secrets
```

2. Install supporting components and infrastructure (example):

Install the External Secrets Operator:

```bash
helm upgrade --install external-secrets ./helm/external-secrets -n external-secrets --create-namespace
```

Install Vault and Postgres:

```bash
helm upgrade --install vault ./helm/vault -n vault --create-namespace
helm upgrade --install database ./helm/postgres -n student-api
```

Install the Student API chart:

```bash
helm upgrade --install student-api ./helm/student-api -n student-api
```

3. Verify resources:

```bash
kubectl get externalsecret -n student-api
kubectl get pods -n student-api
```

Port-forward the API for local access:

```bash
kubectl port-forward svc/student-api 8082:8080 -n student-api
```

## Observability

The observability stack is managed via ArgoCD and includes:
- **Prometheus** (kube-prometheus-stack v61.3.0) - Metrics collection and alerting
- **Grafana** - Visualization and dashboards
- **Loki** (SingleBinary mode) - Log aggregation
- **Promtail** - Log shipping
- **Postgres Exporter** - Database metrics
- **Blackbox Exporter** - Endpoint monitoring

### Deployment

The observability stack is deployed as a single ArgoCD application:

```bash
kubectl apply -f k8s/argocd/apps/observability.yaml
```

**Key Configuration Details:**
- Uses `ServerSideApply=true` to handle large CRD annotations (known issue with kube-prometheus-stack)
- Loki configured with SingleBinary deployment mode for simplicity
- Includes emptyDir volumes for transient storage (suitable for testing/dev)
- All components use `nodeSelector: type: dependent_services` for node placement

### Access Grafana

Port-forward to access Grafana UI:

```bash
kubectl port-forward -n observability svc/prometheus-stack-grafana 3000:80
```

Default credentials: `admin / admin`

Grafana comes pre-configured with:
- Prometheus data source: `http://prometheus-stack-kube-prom-prometheus:9090`
- Loki data source: `http://loki:3100`

### Known Issues & Fixes

**CRD Annotation Size Limit:**
The kube-prometheus-stack chart v60.x and earlier has an issue where CRD annotations exceed Kubernetes' 256KB limit. This is fixed by:
1. Upgrading to v61.3.0+
2. Using `ServerSideApply=true` sync option in ArgoCD

**Loki Filesystem Storage:**
Loki requires writable storage for `/var/loki`. The configuration includes:
```yaml
extraVolumes:
  - name: data
    emptyDir: {}
extraVolumeMounts:
  - name: data
    mountPath: /var/loki
```

## API Endpoints

All endpoints are versioned under `/api/v1`.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/healthcheck` | Service health status |
| GET | `/api/v1/students` | List all students |
| POST | `/api/v1/students` | Create a new student |
| GET | `/api/v1/students/<id>` | Retrieve a student by ID |
| PUT | `/api/v1/students/<id>` | Update a student's details |
| DELETE | `/api/v1/students/<id>` | Delete a student record |

## Testing & Logging

- Unit tests: `make test` (pytest)
- Logging: structured logs (INFO/DEBUG) for observability and troubleshooting

## Student model

The `Student` model contains the following fields:

- `id` (primary key)
- `first_name`, `last_name`
- `grade`
- `email` (unique)
