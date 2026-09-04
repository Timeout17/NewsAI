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


Gane and Sarson's data flow diagram
graph TD
    %% Külső Entitások és Adattárak stílusai
    classDef entity fill:#f9f,stroke:#333,stroke-width:2px;
    classDef datastore fill:#fff,stroke:#333,stroke-width:2px;
    classDef process fill:#cef,stroke:#333,stroke-width:2px,stroke-dasharray: 0;

    %% Külső Entitások és Adattárak definíciója
    User["[User (Streamlit Frontend)]"]:::entity
    FreeNews["[[FreeNewsApi.io Cloud Endpoints]]"]:::entity
    Groq["[[Groq Cloud API Infrastructure]]"]:::entity
    
    D1["D1 / Application Logs (app.log)"]:::datastore
    D2["D2 / Environment Config (.env)"]:::datastore
    D3["D3 / Prompt Config (prompts.json)"]:::datastore

    %% Folyamatok definíciója (Gane & Sarson stílusban)
    P1["1.0 / Read & Log Request<br><b>NewsRouter</b>"]:::process
    P2["2.0 / Fetch Raw News Payload<br><b>NewsApiClient</b>"]:::process
    P3["3.0 / Parse & Build DTOs<br><b>NewsDataFormatter</b>"]:::process
    P4["4.0 / Assemble AI Input<br><b>CreateMessageClass</b>"]:::process
    P5["5.0 / Dispatch LLM Task<br><b>LLMServiceClass</b>"]:::process

    %% Adatfolyam nyilak feliratokkal
    User -- "category, language, limit (Plain text)" --> P1
    P1 -- "log_message" --> D1
    
    P1 -- "category, language, limit (Validated)" --> P2
    D2 -- "API Keys" --> P2
    P2 -- "HTTP GET Request (Bearer Token)" --> FreeNews
    FreeNews -- "Raw API JSON Response" --> P2
    
    P2 -- "List[dict] (Raw JSON)" --> P3
    P3 -- "List[Article] (Pydantic objects)" --> P4
    D3 -- "System Instructions" --> P4
    
    P4 -- "Structured Message Payload (dict list)" --> P5
    D2 -- "Groq API Key" --> P5
    P5 -- "Chat Completions Request" --> Groq
    Groq -- "Groq API Response Object" --> P5
    
    P5 -- "ai_summary_text (Markdown)" --> P1
    P1 -- "HTTP 200 OK JSON (ai_answer)" --> User
