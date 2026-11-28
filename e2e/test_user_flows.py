# FILE:        e2e/test_user_flows.py
# PURPOSE:     Selenium end-to-end tests covering sign-in, Role Map case view, backend 403
#              enforcement for cover colleagues, and sign-out across the real React + FastAPI stack.
# OWNER:       Nazha (Rules & Quality)
# DEPENDS ON:  e2e/conftest.py, frontend/src/pages/*.tsx (data-testid hooks), backend/app/seed.py
# USED BY:     Local E2E verification (`python -m pytest e2e -v`)
# STATUS:      REAL
# DATA:        Synthetic demo accounts only (u-nusrat, u-tania, u-farhana).
# AI NOTE:     Relies on Tonni's data-testid attributes (demo-<userId>, sign-in-submit,
#              signed-in-name, case-card-<id>, case-page, duty-<id>, case-forbidden, sign-out).

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _sign_in_as_demo(driver: WebDriver, base_url: str, user_id: str) -> None:
    """Open /sign-in, click a synthetic demo account button, and submit the form."""
    wait = WebDriverWait(driver, 10)
    driver.get(f"{base_url}/sign-in")
    demo_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="demo-{user_id}"]')))
    demo_btn.click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="signed-in-name"]')))


def test_employee_signs_in_and_opens_role_map_case(driver: WebDriver, app_servers: str) -> None:
    """Nusrat Jahan signs in, sees case-1 in her list, and opens its Role Map duties."""
    wait = WebDriverWait(driver, 10)
    _sign_in_as_demo(driver, app_servers, "u-nusrat")

    signed_in_name = driver.find_element(By.CSS_SELECTOR, '[data-testid="signed-in-name"]').text
    assert "Nusrat Jahan" in signed_in_name

    case_card = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="case-card-case-1"]')))
    case_card.click()

    case_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="case-page"]')))
    assert case_page.is_displayed()

    duty_1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="duty-duty-1"]')))
    duty_2 = driver.find_element(By.CSS_SELECTOR, '[data-testid="duty-duty-2"]')
    assert duty_1.get_attribute("data-evidence") == "documented"
    assert duty_2.get_attribute("data-evidence") == "said"
    assert "Monthly portfolio report" in duty_1.text
    assert "Tuesday credit meeting" in duty_2.text


def test_colleague_sees_empty_list_and_gets_forbidden_on_case_url(driver: WebDriver, app_servers: str) -> None:
    """Tania Akter (cover colleague) sees an empty list and gets 403 forbidden on /cases/case-1."""
    wait = WebDriverWait(driver, 10)
    _sign_in_as_demo(driver, app_servers, "u-tania")

    empty_banner = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="cases-empty"]')))
    assert empty_banner.is_displayed()

    driver.get(f"{app_servers}/cases/case-1")
    forbidden_panel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="case-forbidden"]')))
    assert "You cannot open this case" in forbidden_panel.text


def test_hr_can_view_all_cases_and_sign_out(driver: WebDriver, app_servers: str) -> None:
    """Farhana Islam (HR) sees both seeded cases and returns to /sign-in on sign-out."""
    wait = WebDriverWait(driver, 10)
    _sign_in_as_demo(driver, app_servers, "u-farhana")

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="case-card-case-1"]')))
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="case-card-case-2"]').is_displayed()

    sign_out_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="sign-out"]')))
    sign_out_btn.click()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="sign-in-submit"]')))
    assert "/sign-in" in driver.current_url

def test_unauthenticated_case_url_redirects_to_sign_in(driver: WebDriver, app_servers: str) -> None:
    """Visiting a protected case URL without a session redirects to /sign-in."""
    wait = WebDriverWait(driver, 10)
    driver.get(f"{app_servers}/cases/case-1")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="sign-in-submit"]')))
    assert "/sign-in" in driver.current_url


def test_unknown_case_shows_not_found_panel(driver: WebDriver, app_servers: str) -> None:
    """Opening a non-existent case ID renders the 404 case-not-found panel."""
    wait = WebDriverWait(driver, 10)
    _sign_in_as_demo(driver, app_servers, "u-farhana")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="case-card-case-1"]')))

    driver.get(f"{app_servers}/cases/does-not-exist")
    not_found = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="case-not-found"]')))
    assert "does-not-exist" in not_found.text
