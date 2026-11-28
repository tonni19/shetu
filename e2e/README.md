# Shetu End-to-End Browser Tests (Selenium)

Owner: Nazha (Rules & Quality). Uses Tonni's `data-testid` hooks in `frontend/src/`.

## Run the E2E suite

Make sure backend dependencies (`backend/requirements-dev.txt`), frontend packages (`frontend/node_modules`), and Selenium (`pip install -r e2e/requirements.txt`) are installed, plus Google Chrome.

From the repository root:

```bash
python -m pytest e2e -v
```

`e2e/conftest.py` starts a temporary seeded FastAPI backend on port `8000` and the Vite dev server on port `5173`, drives headless Chrome against `http://localhost:5173`, and stops both servers when finished.

To watch the browser window during a run:

```bash
SHETU_E2E_HEADFUL=1 python -m pytest e2e -v
```
