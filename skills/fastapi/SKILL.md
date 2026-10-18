---
name: fastapi
description: FastAPI handler-layer conventions - thin handlers, Pydantic v2 schemas, dependencies, settings, lifespan, async safety, error mapping, auth wiring, and the API test client. Use before writing or changing any FastAPI route, dependency, schema, app startup, or API test.
---

# FastAPI

A handler adapts HTTP to a service call and back; logic lives in services. Neighbouring owners: wire contract (errors, pagination, idempotency) is `api-design`; auth design is `security`; sessions, queries, and migrations are `postgres` ([sqlalchemy.md](../postgres/references/sqlalchemy.md)); test discipline is `tdd`. Check version-sensitive behaviour against the installed FastAPI and Pydantic.

## Handler

```python
SessionDep = Annotated[AsyncSession, Depends(get_session)]

@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, session: SessionDep) -> UserOut:
    user = await users.create(session, payload)
    return UserOut.model_validate(user)
```

- Parse the body into a Pydantic model, call one service, return a response schema instance. ORM objects stay inside services; the handler maps them with `model_validate`.
- Declare `status_code` on the decorator. The return annotation is the response model; add `response_model=` only when the returned value is not that type.
- Services raise domain exceptions; handlers hold no `try/except`. One `app.exception_handler` per exception family renders the `api-design` error format.
- Bound every list endpoint: `limit: Annotated[int, Query(ge=1, le=MAX_LIMIT)] = DEFAULT_LIMIT`.
- Register a `RequestValidationError` handler that renders the `api-design` problem+json body with status `400`, overriding FastAPI's default `422`.

## Pydantic v2

- Config is `model_config = ConfigDict(...)`; validators are `field_validator` and `model_validator`; serialisation is `model_dump` and `model_validate`; response schemas that read ORM rows set `from_attributes=True`.
- Pydantic v1 spellings (`class Config`, `@validator`, `.dict()`) warn with `PydanticDeprecatedSince20`. Turn the warning into a test failure:

```toml
[tool.pytest.ini_options]
filterwarnings = ["error::pydantic.warnings.PydanticDeprecatedSince20"]
```

## Dependencies

- Declare each as `Annotated[T, Depends(fn)]` and name the alias once (`SessionDep`, `CurrentUser`) next to `fn`.
- The database session comes from a `yield` dependency that opens one session per request; no module-global session.
- A router-wide requirement (auth) goes in `APIRouter(dependencies=[...])`, not in each handler.

## Settings

- One `pydantic_settings.BaseSettings` subclass reads the environment. A `@lru_cache` `get_settings()` builds it once, and handlers and dependencies receive it through `Depends(get_settings)`.
- Secrets, URLs, and keys come from settings; no literals in source.

## Lifespan

- Startup and shutdown resources (engine, HTTP clients) live in one `@asynccontextmanager` `lifespan` passed as `FastAPI(lifespan=...)`. `on_event` is deprecated, and FastAPI ignores it once `lifespan` is set.
- The schema comes from Alembic. `Base.metadata.create_all` appears only in tests.

## Async

- `async def` handlers and dependencies run on the event loop; every call inside them is awaitable or non-blocking. A blocking library (sync DB driver, file or network IO, `time.sleep`) belongs in a plain `def` handler, which FastAPI runs in a threadpool, or behind `await anyio.to_thread.run_sync(fn, *args)`.
- Enable ruff `ASYNC` so blocking calls (`ASYNC210`, `ASYNC230`, `ASYNC251`) fail lint.

## Auth wiring

- One dependency, `CurrentUser = Annotated[Principal, Depends(authenticate)]`, verifies the bearer token with the verifier `security` names for the project's auth provider and returns the `Principal`; a failed verification raises the domain's unauthenticated exception, which the exception handler maps to 401. The checks inside the verifier belong to `security`.

## Tests

- Drive the app through `httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test")` against a real Postgres database whose schema Alembic built.
- `AsyncClient` skips lifespan; wrap the app in `asgi_lifespan.LifespanManager` when a test needs lifespan resources.
- `app.dependency_overrides` replaces true IO edges only (a payment client, an email sender, the clock). The session, services, and settings stay real, with settings pointed at the test database.

## Tooling

`uv` manages dependencies. `ruff check` (with `ASYNC`), the repository's strict type checker (`pyright` or `mypy`), and `pytest` run clean.

**Done when** every handler matches the shape above, `ruff`, the type checker, and `pytest` pass, and the `PydanticDeprecatedSince20` filter is in the pytest config.
