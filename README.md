# 🚀 AI News Summary System (News AI)

An enterprise-grade, containerized news aggregation and summarization platform. The system automatically fetches real-time articles using *FreeNewsApi.io*, filters the data through a clean formatting layer, and utilizes Large Language Models (LLMs) via the **Groq SDK** to generate structured, relevant AI summaries for the user.

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Pydantic, Uvicorn
* **Frontend:** Streamlit, Requests
* **AI / LLM:** Groq SDK (e.g., Llama-3 / Mixtral models)
* **DevOps & Infrastructure:** Docker, Docker-Compose, GitHub Actions (CI/CD Pipeline), Pytest (Mock testing)

## 🏛️ Architecture & Design Patterns

The project is built following strict clean code principles and industrial software design patterns:
* **Clean Architecture:** Strictly separated Router, Orchestrator, and Worker layers to maximize modularity and maintainability.
* **Factory Pattern & Static Utility Classes:** The AI client instantiation and message/prompt structure generation are decoupled into specialized, stateless factories.
* **Data Transfer Object (DTO) / Formatting Layer:** Raw API JSON payloads are automatically transformed into validated Pydantic data models (`Article`) before entering the business logic.
* **Resilience & Observability:** Centralized global exception handling (emergency brake) combined with automated, real-time file logging (`app.log`) exposed via Docker volumes.
