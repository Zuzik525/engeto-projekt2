# Common test configuration and fixtures
import pytest, re
from playwright.sync_api import sync_playwright, Browser

# Root site url (with trailing slash)
SITE_URL = "https://www.knihkupec.com/" 

# Create browser with settings
@pytest.fixture()
def browser():
    with sync_playwright() as pw:
        #browser = pw.chromium.launch(headless=False, slow_mo=1000)
        browser = pw.chromium.launch()
        yield browser
        browser.close()

# Create page without agreed cookies
@pytest.fixture()
def page_without_cookie(browser: Browser):
    page = browser.new_page()
    yield page
    page.close()

# Create page with cookies accepted
@pytest.fixture()
def page(browser: Browser):
    page = browser.new_page()
    page.goto(SITE_URL)
    page.locator("#cm_button_ok").click() #Accept cookies

    yield page
    page.close()
