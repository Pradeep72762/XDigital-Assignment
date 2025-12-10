import pytest
from playwright.sync_api import Browser, sync_playwright


@pytest.fixture(scope="session")
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        channel="chrome",
        headless=False,
        slow_mo=500,
    )
    yield browser
    print("\n[INFO] Test completed. Browser will remain open for manual inspection.")
    print("[INFO] Please close the browser manually when done.")


@pytest.fixture(scope="function")
def page(browser: Browser):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="en-US"
    )
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def page_mobile(browser: Browser):
    context = browser.new_context(
        viewport={"width": 375, "height": 667},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
        locale="en-US"
    )
    page = context.new_page()
    page.set_viewport_size({"width": 375, "height": 667})
    yield page
    page.close()
    context.close()

