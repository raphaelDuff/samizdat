# Samizdat — FastAPI DDD Base Project

A production-ready backend boilerplate built with **FastAPI** and structured around **Domain-Driven Design (DDD)** principles combined with **Clean Architecture**. This project is intended as a solid foundation for building scalable, maintainable, and testable Python backends.

> **Reference:** This project is architecturally inspired by the book
> [Clean Architecture with Python: Implement scalable and maintainable applications using proven architectural principles](https://www.amazon.com.br/gp/product/B0F6C97JWL)

---

## Tech Stack

| Technology | Role |
|---|---|
| **Python 3.13+** | Language |
| **FastAPI** | Web framework |
| **Uvicorn** | ASGI server |
| **SQLModel** | ORM (SQLAlchemy + Pydantic) |
| **asyncpg** | Async PostgreSQL driver |
| **Alembic** | Database migrations |
| **Pydantic v2** | Data validation |
| **PyJWT** | JWT token handling |
| **pwdlib / Argon2** | Password hashing |
| **uv** | Dependency management |
| **Ruff** | Linting |

---

## Architecture

The project is organized in four concentric layers following Clean Architecture. Dependencies only point inward — outer layers depend on inner layers, never the reverse.

```
┌────────────────────────────────────────────────┐
│                  Interfaces                    │  ← Controllers, Presenters, ViewModels
│  ┌──────────────────────────────────────────┐  │
│  │              Application                 │  │  ← Use Cases, DTOs, Repository Interfaces
│  │  ┌────────────────────────────────────┐  │  │
│  │  │              Domain               │  │  │  ← Entities, Domain Services, Exceptions
│  │  └────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────┘  │
└────────────────────────────────────────────────┘
         ↑ Infrastructure wraps all layers ↑
   (DB, Web Framework, Security, DI Container)
```

### Layer Descriptions

#### Domain Layer (`app/domain/`)

The innermost layer. Contains pure business logic with no framework dependencies.

- **Entities** — Core business objects with identity (e.g., `UserDomain`). All entities share a base `Entity` class with a UUID primary key.
- **Domain Services** — Interfaces for cross-entity operations (e.g., `PasswordHasher` protocol).
- **Exceptions** — Domain-specific errors (`DomainError`, `UserIdNotFoundError`).

#### Application Layer (`app/application/`)

Orchestrates domain objects to fulfill use cases. No knowledge of HTTP, databases, or frameworks.

- **Use Cases** — Single-responsibility handlers for business operations (e.g., `CreateUserUseCase`, `GetUsersUserCase`).
- **DTOs** — Data Transfer Objects for input/output across layer boundaries.
- **Repository Interfaces** — Abstract contracts that the infrastructure layer must fulfill.
- **Unit of Work** — Protocol that enforces transaction boundaries and repository access.
- **Result Type** — A generic `Result[T]` monad (Either pattern) for type-safe error propagation without exceptions.

#### Infrastructure Layer (`app/infra/`)

Contains all technical implementation details. Depends on the inner layers but is never depended upon by them.

- **Persistence** — `PostgreSQLRepository` implements the abstract repository using SQLModel + asyncpg.
- **Mappers** — Translate between domain entities and ORM models (e.g., `UserMapper`).
- **Unit of Work** — `SqlAlchemyUnitOfWork` manages async SQLAlchemy sessions and transactions.
- **Security** — `PasswordService` (Argon2 hashing) and `JwtService` (JWT creation/validation).
- **Web** — FastAPI app factory with lifespan management (startup/shutdown hooks).
- **Dependencies** — FastAPI dependency injection graph wiring use cases, controllers, and repositories.
- **DI Container** — `Application` dataclass that assembles all components at startup.
- **Config** — Environment-based configuration via `pydantic-settings`.

#### Interfaces Layer (`app/interfaces/`)

Adapts application layer outputs for delivery mechanisms (in this case, HTTP).

- **Controllers** — Orchestrate use cases and delegate to presenters (e.g., `UserController`).
- **Presenters** — Format use case output into view models for the web response.
- **View Models** — Serializable response shapes decoupled from domain entities.

---

## Project Structure

```
samizdat/
└── backend/
    ├── main.py                     # Entry point — runs Uvicorn
    ├── pyproject.toml              # Dependencies and project config
    ├── alembic.ini                 # Alembic migration config
    ├── .env.example                # Environment variable template
    ├── migrations/                 # Alembic migration scripts
    └── app/
        ├── domain/
        │   ├── entities/           # Base Entity, UserDomain
        │   ├── services/           # PasswordHasher interface
        │   └── exceptions.py       # Domain exceptions
        ├── application/
        │   ├── common/             # Result type (success/failure monad)
        │   ├── dtos/               # Request/response DTOs
        │   ├── repositories/       # Abstract repository interfaces
        │   ├── use_cases/          # Business operation handlers
        │   └── uow.py              # Unit of Work protocol
        ├── infra/
        │   ├── db/
        │   │   ├── mappers/        # Domain ↔ ORM model mappers
        │   │   └── models/         # SQLModel ORM definitions
        │   ├── persistence/        # PostgreSQL repository implementation
        │   ├── security/           # JWT and password services
        │   ├── configuration/      # DI container
        │   ├── web/
        │   │   ├── app.py          # FastAPI app factory
        │   │   ├── dependencies.py # FastAPI DI graph
        │   │   ├── error_mapping.py
        │   │   └── routes/         # HTTP route definitions
        │   ├── config.py           # Database engine setup
        │   └── uow.py              # SQLAlchemy Unit of Work
        └── interfaces/
            ├── controllers/        # Request orchestration
            ├── presenters/         # Output formatters
            └── view_models/        # HTTP response shapes
```

---

## Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL running locally (or via Docker)
- [`uv`](https://docs.astral.sh/uv/) installed

### Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd samizdat/backend

# 2. Install dependencies
uv sync

# 3. Configure environment
cp .env.example .env
# Edit .env with your database credentials and JWT secret

# 4. Run database migrations
uv run alembic upgrade head

# 5. Start the development server
uv run python main.py
```

The API will be available at `http://localhost:8000`.
Interactive docs (Swagger UI): `http://localhost:8000/docs`

### Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | Async PostgreSQL connection string | `postgresql+asyncpg://user:pass@localhost:5432/samizdat` |
| `CONFIG_REPOSITORY_TYPE` | Repository implementation to use | `postgresql` |
| `DATABASE_ECHO` | Log SQL queries to stdout | `false` |
| `SECRET_KEY` | JWT signing secret | `your-secret-key` |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token lifetime | `15` |

---

## Available Endpoints

| Method | Path | Description | Status |
|---|---|---|---|
| `POST` | `/users/` | Register a new user | Done |
| `POST` | `/auth/token` | Authenticate and get JWT token | TODO |
| `GET` | `/auth/me` | Get the currently authenticated user | TODO |

---

## Key Design Patterns

- **Result Monad** — Use cases return `Result[T]` instead of raising exceptions, making error paths explicit and type-safe.
- **Unit of Work** — Transaction boundaries are managed by a protocol-based UoW, keeping use cases free of session management.
- **Mapper Pattern** — Domain entities and ORM models are completely separate; mappers handle translation between them.
- **Dependency Injection** — FastAPI's DI system is used to wire the full dependency graph per request, with no global state.
- **Presenter Pattern** — Controllers delegate formatting to presenters, keeping controllers thin and output format decoupled from business logic.

---

## Reference

> [Clean Architecture with Python: Implement scalable and maintainable applications using proven architectural principles (English Edition)](https://www.amazon.com.br/gp/product/B0F6C97JWL)
