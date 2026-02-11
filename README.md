# Student API (SRE Bootcamp)

A production-grade REST API for managing student records. This project is built to be "cloud-native," transitioning from local development to a distributed Kubernetes architecture.

##  Kubernetes (Production Deployment)

This is the current "Production" state of the project, simulating a real-world distributed environment using a three-node Minikube cluster.

### Architecture Highlights

* 
**Multi-Node Isolation:** Workloads are distributed across labeled nodes (Application, Database, and Dependent Services) to ensure resource separation.


* **Zero-Trust Secrets:** Sensitive credentials are never stored in plain text. We use the **External Secrets Operator (ESO)** to fetch secrets from a **HashiCorp Vault** instance.


* 
**Automated Migrations:** Database schema changes are handled by an **Init Container** (`run-migrations`) that must succeed before the API pod starts.


* 
**High Availability:** The API is deployed with multiple replicas in the `student-api` namespace for resilience.



### Deployment Steps

1. **Label your nodes** (if not already done):
```bash
kubectl label nodes sre-bootcamp type=application
kubectl label nodes sre-bootcamp-m02 type=database

```


2. **Deploy the Stack:**
```bash
kubectl apply -f database.yml
kubectl apply -f application.yml

```


3. **Verify Secrets Sync:**
```bash
kubectl get externalsecret -n student-api

```


4. **Access the API:**
```bash
kubectl port-forward svc/student-api 8082:8080 -n student-api

```



---

##  Tech Stack

* 
**Orchestration:** Kubernetes (Minikube), Docker Compose 


* 
**Secrets:** HashiCorp Vault & External Secrets Operator 


* **Language:** Python 3.14 (Flask)
* 
**Database:** PostgreSQL 15 


* 
**CI/CD:** GitHub Actions with Self-Hosted Runners 



---

##  Local Development (Docker Compose)

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

##  API Endpoints

All endpoints support versioning (e.g., `/api/v1/<resource>`).

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/healthcheck` | Service health status 

 |
| GET | `/api/v1/students` | Get all students 

 |
| POST | `/api/v1/students` | Create a new student 

 |
| GET | `/api/v1/students/<id>` | Get specific student 

 |
| PUT | `/api/v1/students/<id>` | Update student details 

 |
| DELETE | `/api/v1/students/<id>` | Delete a student record 

 |

---

##  Testing & Logging

* 
**Unit Tests:** Run `make test` to execute the pytest suite.


* 
**Structured Logs:** The API emits logs with appropriate levels (INFO/DEBUG) to ensure observability.



---

## Student Model

The `Student` model includes:

* `id` (Primary Key)
* `first_name`, `last_name`, `grade`, `email` (Unique)

---


