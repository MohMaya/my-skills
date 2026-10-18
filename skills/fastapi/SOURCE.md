# Sources

Rewritten for this repository on 2026-10-18 from `fastapi-expert` in [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) (MIT, per the upstream skill's frontmatter; no separate license file ships on disk), imported in commit `40c5f7c`. Rules are rewritten, and upstream defects are not carried over: the nonexistent `from pydantic import model_config`, ORM returns declared as `response_model=UserOut`, `python-jose` and `passlib`, literal `SECRET_KEY`, an `aiosqlite` test database, patching the app's own functions, and `create_all` at startup.

Checked on 2026-10-18 against FastAPI 0.146.0, Pydantic 2.14.1, and pydantic-settings 2.16.0:

- [Response model and return type](https://fastapi.tiangolo.com/tutorial/response-model/)
- [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/), [dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/), [SQL databases (session per request)](https://fastapi.tiangolo.com/tutorial/sql-databases/), [bigger applications (router dependencies)](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Settings and environment variables](https://fastapi.tiangolo.com/advanced/settings/) (`BaseSettings`, `lru_cache`)
- [Lifespan events](https://fastapi.tiangolo.com/advanced/events/)
- [Async and `def`](https://fastapi.tiangolo.com/async/)
- [Handling errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Numeric validations (`Query(ge, le)`)](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/)
- [OAuth2 with JWT (PyJWT, pwdlib)](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [Async tests](https://fastapi.tiangolo.com/advanced/async-tests/) (`AsyncClient`, `ASGITransport`, lifespan caveat) and [testing dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Migrating from Pydantic v1](https://fastapi.tiangolo.com/how-to/migrate-from-pydantic-v1-to-pydantic-v2/) (FastAPI 0.128.0 and later require Pydantic v2)
- [Pydantic models and `from_attributes`](https://pydantic.dev/docs/validation/latest/concepts/models/), [config](https://pydantic.dev/docs/validation/latest/concepts/config/), [migration guide](https://pydantic.dev/docs/validation/latest/migration/)
- [Ruff `ASYNC` rules](https://docs.astral.sh/ruff/rules/#flake8-async-async)

`PydanticDeprecatedSince20` and its pytest `filterwarnings` spelling were run against Pydantic 2.14.1: the class lives in `pydantic.warnings`, and `.dict()` and `@validator` raise under the filter.
