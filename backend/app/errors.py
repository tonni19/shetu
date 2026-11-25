# FILE:        backend/app/errors.py
# PURPOSE:     Makes every error the API returns look the same: {"code": ..., "detail": ...}.
#              The frontend can then show any error with one piece of code.
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  docs/API-CONTRACT.md, "Error"
# USED BY:     app/main.py registers the handlers; routes raise ApiError
# STATUS:      REAL
# AI NOTE:     Raise ApiError(status, code, detail) in routes instead of returning error dicts.
#              Status codes from the contract: 401 not signed in, 403 not allowed, 404 not found,
#              409 a rule failed, 422 the request body has the wrong shape.

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class ApiError(Exception):
    """An error we expect and want to explain to the caller."""

    def __init__(self, status: int, code: str, detail: str):
        self.status = status
        self.code = code
        self.detail = detail


def _body(code: str, detail: str) -> dict:
    return {"code": code, "detail": detail}


def register_error_handlers(app: FastAPI) -> None:
    """Attach the three handlers that turn errors into the contract's error shape."""

    @app.exception_handler(ApiError)
    async def _api_error(_: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(status_code=exc.status, content=_body(exc.code, exc.detail))

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        # For example an unknown URL (404) or a wrong method (405).
        return JSONResponse(status_code=exc.status_code, content=_body(f"http_{exc.status_code}", str(exc.detail)))

    @app.exception_handler(RequestValidationError)
    async def _bad_request(_: Request, exc: RequestValidationError) -> JSONResponse:
        # The body did not match the Pydantic model, for example a missing field.
        first = exc.errors()[0] if exc.errors() else {}
        where = ".".join(str(p) for p in first.get("loc", []))
        return JSONResponse(status_code=422, content=_body("invalid_request", f"{where}: {first.get('msg', 'invalid')}"))
