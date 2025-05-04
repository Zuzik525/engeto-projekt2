# Tests around HTTP/cookies functionality
from playwright.sync_api import Page, expect
from conftest import SITE_URL

# HTTP requests should be automatically redirected to HTTPS
def test_redirect_to_https(page_without_cookie):
    page = page_without_cookie
    site_url_insecure = SITE_URL.replace("https", "http")
    page.goto(site_url_insecure)
    assert page.url == SITE_URL

# Tests cookies accept dialog
# Should be shown at first visit, and after each reload until accepted/rejected
def test_cookie_message(page_without_cookie : Page):
    page = page_without_cookie
    page.goto(SITE_URL)
    expect(page.locator("#cookies_management")).to_be_visible() #dialog is shown
    expect(page.locator("#cookies_management")).not_to_be_empty() #dialog is not empty
    page.locator("#cookies_management .cm_close").click() #Only close dialog without agreement
    expect(page.locator("#cookies_management")).to_be_hidden() #dialog is hidden
    
    page.goto(SITE_URL)#reload site
    expect(page.locator("#cookies_management")).to_be_visible()#dialog is shown
    page.locator("#cookies_management #cm_button_ok").click()#Accept cookies
    expect(page.locator("#cookies_management")).to_be_hidden()#dialog is hidden

    page.goto(SITE_URL)#reload site
    expect(page.locator("#cookies_management")).to_be_hidden()#dialog is hidden after agreement

