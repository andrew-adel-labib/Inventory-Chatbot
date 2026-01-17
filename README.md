# 📦 Inventory Analytics Chatbot Platform

---

## Overview

This project implements a **production‑ready inventory analytics chatbot** that answers business questions in natural language and returns:

- a **human‑readable answer**
- the **exact SQL query (“present query”)** the system would run

The system demonstrates **safe LLM integration, deterministic SQL reasoning, role‑based access control, CI/CD, and GitOps‑based Kubernetes deployment**, while intentionally avoiding unnecessary complexity.

---

## System Architecture

The platform follows a clean separation of concerns and a GitOps deployment model.

**High‑level flow:**

User → Streamlit UI → Inventory API → Azure OpenAI (intent classification only)  
GitHub → Jenkins (CI) → AWS ECR → Argo CD → Amazon EKS

---

## Core Design Principles

- LLM is used **only for intent classification**
- SQL is **never generated dynamically**
- SQL queries are **static templates** derived from the provided schema
- No database execution (queries are presented only)
- Centralized logging and error handling
- Environment‑driven configuration
- Git as the single source of truth

---

## Request Lifecycle

1. User submits a question via Streamlit UI
2. API retrieves session context (TTL‑based)
3. Intent is classified using Azure OpenAI
4. RBAC validates intent access
5. SQL template is selected deterministically
6. SQL is validated by a safety sandbox
7. Natural language answer + SQL query returned

---

## SQL Strategy

- All SQL queries are predefined templates
- Fully aligned with the provided SQL Server schema
- No string interpolation from user input
- No execution, no side effects

This guarantees:
- Zero SQL injection risk
- No LLM hallucinated SQL
- Full auditability

---

## Technology Stack

| Layer | Technology |
|-----|-----------|
| UI | Streamlit |
| API | Python (standard library + pydantic) |
| LLM | Azure OpenAI |
| Containers | Docker |
| Orchestration | Kubernetes (Amazon EKS) |
| CI | Jenkins |
| CD | Argo CD (GitOps) |
| Registry | AWS ECR |

---

## Configuration & Secrets

- Local development uses a lightweight `.env` loader
- Production secrets are injected via Kubernetes Secrets
- No credentials are committed to the repository
- Containers run as non‑root users

---

## CI/CD Flow

```
GitHub Push
   ↓
Jenkins (Tests + Build)
   ↓
AWS ECR (Images)
   ↓
Argo CD (GitOps)
   ↓
Amazon EKS
```

- Jenkins handles **CI only**
- Argo CD handles **deployment**
- No kubectl or Helm in CI pipelines

---

## Testing

Run all unit tests:

```bash
python -m unittest discover tests
```

Coverage includes:
- Role‑based access control
- Session TTL eviction
- SQL intent completeness

---

## Logging & Error Handling

- Logging configured once at application startup
- Consistent structured logging across all layers
- Domain and infrastructure layers raise exceptions
- HTTP layer translates exceptions to responses

---

## Security Considerations

- No SQL execution
- Deterministic SQL templates only
- LLM constrained to JSON output
- Secrets injected at runtime
- Non‑root containers
- No external exposure by default

---

## Contact

**Andrew Adel Labib**  
AI / ML Engineer 

📍 Cairo, Egypt  

📧 Email: andrewadellabib77@gmail.com  
📞 Phone: +20 106 376 9806 / +20 128 663 2047  

🔗 LinkedIn: https://linkedin.com/in/andrew-adel-b865b1244  
💻 GitHub: https://github.com/andrew-adel-labib