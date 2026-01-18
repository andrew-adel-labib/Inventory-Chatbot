# 📦 Inventory Analytics Chatbot Platform

---

## Overview

This project implements a **production-ready inventory analytics chatbot** that answers business questions in natural language and returns:

- a **human-readable answer**
- the **exact SQL query (“present query”)** the system would run

The system demonstrates **safe LLM integration, deterministic SQL reasoning, role-based access control, CI/CD, and GitOps-based Kubernetes deployment**

---

## System Architecture

The platform follows a clean separation of concerns and a GitOps deployment model.

**High-level flow:**

User → Streamlit UI → Inventory API → Azure OpenAI (intent classification only)  
GitHub → Jenkins (CI) → AWS ECR → Argo CD → Amazon EKS

---

## Core Design Principles

- LLM is used **only for intent classification**
- SQL is **never generated dynamically**
- SQL queries are **static templates** derived from the provided schema
- Centralized logging and error handling
- Environment-driven configuration
- Git as the single source of truth

---

## Request Lifecycle

1. User submits a question via Streamlit UI
2. API retrieves session context (**in-memory session store with TTL**)
3. Intent is classified using **Azure OpenAI**
4. **Role-Based Access Control (RBAC)** validates intent access
5. SQL template is selected deterministically
6. SQL is validated by a safety sandbox
7. Natural language answer + SQL query returned

---

## SQL Strategy (“Present Query”)

- All SQL queries are **predefined static templates**
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

## Local Development

### Run Backend API

```bash
python -m apps.api.src.main
```

### Run Streamlit Frontend

```bash
streamlit run app.py
```

---

## Session Memory & RBAC

- Session-based conversation memory (in-memory)
- TTL-based expiration
- Role-based authorization per intent
- Viewer / Finance / Admin separation

---

## Configuration & Secrets

Environment variables:

```
PROVIDER=openai | azure
OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_DEPLOYMENT=...
MODEL_NAME=...
```

---

## CI/CD & GitOps Workflow

```
GitHub Push
   ↓
Jenkins (Tests + Build)
   ↓
AWS ECR
   ↓
Argo CD
   ↓
Amazon EKS
```

- Jenkins tested locally
- GitHub Webhooks enabled
- Argo CD runs inside EKS
- GitOps-based deployment

---

## Testing

```bash
python -m unittest discover tests
```

Covers:
- RBAC
- Session TTL
- Intent-to-SQL mapping
- Error handling

---

## Security Considerations

- No SQL execution
- Deterministic SQL only
- JSON-only LLM output
- Secrets via environment/K8s
- Non-root containers

---

## Contact

**Andrew Adel Labib**  
AI / ML Engineer  

📍 Cairo, Egypt  

📧 andrewadellabib77@gmail.com  
📞 +20 106 376 9806 / +20 128 663 2047  

🔗 LinkedIn: https://linkedin.com/in/andrew-adel-b865b1244  
💻 GitHub: https://github.com/andrew-adel-labib