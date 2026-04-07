# <System Name>

## 1. Summary
- Purpose:
- Primary users/consumers:
- Main capabilities:
- Tech stack:
- External integrations:

## 2. Description
Short 1-3 paragraph explanation of what the system does, its boundaries, and how requests move through it.

## 3. Endpoint Details

| Endpoint | Method | Purpose | Auth | Request | Response | Dependencies | Notes |
|---|---|---|---|---|---|---|---|
| /api/... | GET/POST | ... | ... | ... | ... | ... | ... |

## 4. Architecture Diagram
```mermaid
flowchart LR
    Client --> API
    API --> Service
    Service --> DB
    Service --> ExternalSystem
```

## 5. Subsystem Details

| Subsystem | Responsibility | Key Modules/Files | Inputs | Outputs | Dependencies |
|---|---|---|---|---|---|
| API Layer | Accepts requests | routes/, controllers/ | HTTP requests | DTO/commands | Service layer |

## 6. Journey Flow – <Endpoint or Use Case Name>
```mermaid
flowchart TD
    A[Request received] --> B[Validate input]
    B --> C[Authorize]
    C --> D[Call service]
    D --> E{Success?}
    E -->|Yes| F[Return response]
    E -->|No| G[Return error]
```

## 7. Sequence Diagram – <Endpoint or Use Case Name>
```mermaid
sequenceDiagram
    actor Client
    participant API
    participant Service
    participant DB
    participant External

    Client->>API: HTTP request
    API->>API: Validate + authorize
    API->>Service: Execute use case
    Service->>DB: Read/write data
    Service->>External: Optional external call
    DB-->>Service: Data
    External-->>Service: Result
    Service-->>API: Response model
    API-->>Client: HTTP response
```
