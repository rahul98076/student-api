

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

The repo includes Helm values for monitoring (Prometheus, Grafana), logging (Loki), and exporters.

Add required Helm repos and install the stack (example):

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack -n observability -f helm/observability-values.yaml
helm install loki grafana/loki-stack -n observability -f helm/observability-values.yaml
helm install db-exporter prometheus-community/prometheus-postgres-exporter -n observability -f helm/observability-values.yaml
helm install blackbox prometheus-community/prometheus-blackbox-exporter -n observability -f helm/observability-values.yaml
```

Port-forward Grafana:

```bash
kubectl port-forward -n observability deployment/monitoring-grafana 3000:3000
```

Grafana data sources in this setup typically point to Prometheus and Loki.

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
