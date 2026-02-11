---

# Student API (SRE Bootcamp)

A production-grade REST API for managing student records. This project is built to be "cloud-native," transitioning from local development to a distributed Kubernetes architecture managed via Helm.

## Kubernetes (Production Deployment)

This is the current "Production" state of the project, simulating a real-world distributed environment using a three-node Minikube cluster. All resources are managed through Helm charts for consistency and scalability.

### Architecture Highlights

* **Multi-Node Isolation:** Workloads are distributed across labeled nodes (Application, Database, and Dependent Services) to ensure resource separation.
* **Package Management:** The entire stack is deployed using Helm charts, allowing for versioned releases and templated configurations.
* **Zero-Trust Secrets:** Sensitive credentials are never stored in plain text. We use the **External Secrets Operator (ESO)** to fetch secrets from a **HashiCorp Vault** instance.
* **Automated Migrations:** Database schema changes are handled by an **Init Container** (`run-migrations`) within the Helm deployment that must succeed before the API pod starts.
* **High Availability:** The API is deployed with multiple replicas in the `student-api` namespace for resilience.

### Deployment Steps

1. **Label your nodes** (if not already done):

```bash
kubectl label nodes sre-bootcamp type=application
kubectl label nodes sre-bootcamp-m02 type=database
kubectl label nodes sre-bootcamp-m03 type=dependent-services

```

2. **Update Dependencies:**
Navigate to each chart directory in `helm/` and ensure community dependencies are updated:

```bash
helm dependency update ./helm/vault
helm dependency update ./helm/postgres
helm dependency update ./helm/external-secrets

```

3. **Deploy the Stack via Helm:**
Install the components in the following order to ensure dependencies are available:

```bash
# 1. External Secrets Operator
helm upgrade --install external-secrets ./helm/external-secrets -n external-secrets --create-namespace

# 2. Vault and Database
helm upgrade --install vault ./helm/vault -n vault --create-namespace
helm upgrade --install database ./helm/postgres -n student-api

# 3. Student API
helm upgrade --install student-api ./helm/student-api -n student-api

```

4. **Verify Secrets Sync:**

```bash
kubectl get externalsecret -n student-api

```

5. **Access the API:**

```bash
kubectl port-forward svc/student-api 8082:8080 -n student-api

```

---

## Tech Stack

* **Orchestration:** Kubernetes (Minikube), Helm v3, Docker Compose
* **Secrets:** HashiCorp Vault & External Secrets Operator
* **Language:** Python 3.14 (Flask)
* **Database:** PostgreSQL 15 (Bitnami Helm Chart)
* **CI/CD:** GitHub Actions with Self-Hosted Runners

---

## Local Development (Docker Compose)

The repository still supports a one-click local environment for rapid feature development.

### Prerequisites

* Docker & Docker Compose
* GNU `make`

### Quick Start

```bash
make setup   # Install tools
make start   # Start API + DB and apply migrations

```

**Common Make Targets:**
| Command | Description |
| :--- | :--- |
| `make up` | Start services in detached mode |
| `make down` | Stop services |
| `make migrate` | Run manual migrations inside the container |
| `make test` | Run unit tests with pytest |

---

## API Endpoints

All endpoints support versioning (e.g., `/api/v1/<resource>`).

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/healthcheck` | Service health status |
| GET | `/api/v1/students` | Get all students |
| POST | `/api/v1/students` | Create a new student |
| GET | `/api/v1/students/<id>` | Get specific student |
| PUT | `/api/v1/students/<id>` | Update student details |
| DELETE | `/api/v1/students/<id>` | Delete a student record |

---

## Testing & Logging

* **Unit Tests:** Run `make test` to execute the pytest suite.
* **Structured Logs:** The API emits logs with appropriate levels (INFO/DEBUG) to ensure observability.

---

## Student Model

The `Student` model includes:

* `id` (Primary Key)
* `first_name`, `last_name`, `grade`, `email` (Unique)

---
