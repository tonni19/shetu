# FILE:        e2e/conftest.py
# PURPOSE:     Starts a seeded temporary FastAPI backend and the Vite dev server, and provides
#              a Selenium WebDriver fixture for full-stack browser tests.
# OWNER:       Nazha (Rules & Quality)
# DEPENDS ON:  backend/app/main.py, backend/app/seed.py, frontend/vite.config.ts, Google Chrome
# USED BY:     e2e/test_user_flows.py
# STATUS:      REAL
# DATA:        Synthetic only. Uses a throwaway SQLite file seeded with demo accounts.
# AI NOTE:     Vite proxies /api and /healthz on localhost:5173 to 127.0.0.1:8000, so the
#              browser must open http://localhost:5173 (never 127.0.0.1:8000 directly) for the
#              session cookie to work as configured in frontend/vite.config.ts.

from __future__ import annotations

import socket

import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"
BASE_URL = os.environ.get("SHETU_E2E_URL", "http://localhost:5173").rstrip("/")


def _assert_port_free(port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if sock.connect_ex(("127.0.0.1", port)) == 0:
            raise RuntimeError(
                f"Port {port} is already in use. Stop any running dev server before running `pytest e2e`."
            )


def _wait_for_http(url: str, timeout: float = 25.0) -> None:
    """Poll a URL until it answers with HTTP 200 or raise TimeoutError."""
    deadline = time.monotonic() + timeout
    last_err: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2.0) as resp:
                if resp.status == 200:
                    return
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            time.sleep(0.3)
    raise TimeoutError(f"Timed out waiting for {url} (last error: {last_err})")


@pytest.fixture(scope="session")
def app_servers(tmp_path_factory: pytest.TempPathFactory) -> str:
    """Start backend (on a fresh seeded DB) and Vite frontend for the E2E session."""
    if os.environ.get("SHETU_E2E_URL"):
        _wait_for_http(f"{BASE_URL}/healthz", timeout=10.0)
        yield BASE_URL
        return

    db_dir = tmp_path_factory.mktemp("shetu_e2e_db")
    db_path = db_dir / "e2e.db"
    backend_env = {
        **os.environ,
        "SHETU_DATABASE_URL": f"sqlite:///{db_path}",
    }

    subprocess.run(
        [sys.executable, "-m", "app.seed"],
        cwd=str(BACKEND_DIR),
        env=backend_env,
        check=True,
    )

    _assert_port_free(8000)
    _assert_port_free(5173)

    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=str(BACKEND_DIR),
        env=backend_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev", "--", "--host", "localhost", "--port", "5173", "--strictPort"],
        cwd=str(FRONTEND_DIR),
        env=os.environ.copy(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    try:
        _wait_for_http("http://127.0.0.1:8000/healthz", timeout=20.0)
        _wait_for_http(f"{BASE_URL}/healthz", timeout=25.0)
        yield BASE_URL
    finally:
        for proc in (frontend_proc, backend_proc):
            proc.terminate()
            try:
                proc.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                proc.kill()


@pytest.fixture
def driver(app_servers: str):
    """Provide a clean Chrome WebDriver instance per test (fresh cookies/storage)."""
    options = Options()
    if os.environ.get("SHETU_E2E_HEADFUL") != "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(2)
    try:
        yield browser
    finally:
        browser.quit()
