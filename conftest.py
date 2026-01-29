import pytest #Python testing framework
from pytest_bdd import given, when, then, parsers #Pytest extension for BDD (Behavior Driven Development) using Given/When/Then
from playwright.sync_api import sync_playwright #Playwright library for browser automation. sync_playwright allows using Playwright without async/await
import allure #For test reports with screenshots and attachments
from pathlib import Path #Cleaner handling of file paths
from datetime import datetime #To generate timestamps for files like screenshots
#File/folder manipulation (delete, create, clean directories):
import shutil
import os
#Page Object Model (POM) classes --> Each class contains methods and selectors for a specific page:
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from re import sub #For replace all illegal Windows characters with _ when scheenshot name file

"""Add browser option:
If default browser not specified, Chromium is used. Allows running Pytest with a specific browser.
Text shown if you run pytest --help."""
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="chromium, firefox, webkit, edge"
    )
"""Browser fixture:
Fixture that initializes a Playwright browser based on the --browser option.
headless=False means the browser opens visibly.
yield browser gives the browser to the test, and after the test finishes, browser.close() closes it.
Supports Chromium, Firefox, WebKit, and Edge."""
@pytest.fixture(scope="function")
def browser(playwright_instance, request):
    browser_name = request.config.getoption("--browser")
    if browser_name == "chromium":
        browser = playwright_instance.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright_instance.firefox.launch(headless=False)
    elif browser_name == "webkit":
        browser = playwright_instance.webkit.launch(headless=False)
    elif browser_name == "edge":
        browser = playwright_instance.chromium.launch(channel="msedge", headless=False)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    yield browser
    browser.close()

"""Browser context and page fixtures:
context: Creates a browser context (like a new browser profile with separate cookies/storage).
page: Creates a new tab inside the context.
request.node._page = page: Stores a reference to the page for screenshots.
Closes the page after the test finishes."""
@pytest.fixture
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture
def page(context, request):
    page = context.new_page()
    request.node._page = page
    yield page
    if not page.is_closed():
        page.close()

"""Clean reports at session start --> Runs once at the very start of the test session:
Cleans old contents from reports/allure-results, reports/allure-report, and reports/screenshots (including all subfolders).
Creates the folders again if they do not exist. Ensures that reports/screenshots/steps exists for storing step screenshots."""
@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    paths = [
        "reports/allure-results",
        "reports/allure-report",
        "reports/screenshots",
    ]

    for path in paths:
        os.makedirs(path, exist_ok=True)
        #Delete all content recursively
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f"⚠️ It could not be deleted {item_path}: {e}")
        print(f"🧹 Contents completely cleaned: {path}")

    #Create subfolder for step screenshots:
    screenshots_steps_path = os.path.join("reports", "screenshots", "steps")
    os.makedirs(screenshots_steps_path, exist_ok=True)
    print(f"✅ Folder ready for screenshots of steps: {screenshots_steps_path}")

"""Take screenshot on test failure --> Triggered after each test execution, used to inspect the test result:
Checks if the test failed during setup or call. If so, takes a full-page screenshot of the current Playwright page.
Saves the screenshot to reports/screenshots with a timestamped filename. Attaches the screenshot to the Allure report.
Prints a console message with the screenshot path."""
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Only when test fails
    if report.when not in ("setup", "call"):
        return
    if not report.failed:
        return
    page = getattr(item, "_page", None)
    if not page or page.is_closed():
        return
    
    try:
        screenshots_dir = Path("reports/screenshots/steps")
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Clean test name
        test_name = sub(r'[\\/*?:"<>|]', "_", item.nodeid)
        test_name = test_name.replace("::", "_").replace("/", "_")

        screenshot_path = screenshots_dir / f"FAILED_{test_name}_{timestamp}.png"
        page.screenshot(path=str(screenshot_path), full_page=True) #Full page screenshot

        #Add to Allure
        allure.attach.file(
            str(screenshot_path),
            name=f"❌ {item.name}",
            attachment_type=allure.attachment_type.PNG
        )
        print(f"📸 Screenshot of failed test: {screenshot_path}")
    except Exception as e:
        print(f"⚠️ Error taking screenshot of failed test: {e}")

"""Screenshot after each BDD step --> Triggered after each BDD step (Given/When/Then):
Checks if the Playwright page is open. Takes a full-page screenshot of the current step.
Saves the screenshot to reports/screenshots/steps with a filename including scenario name, step keyword, step name, and timestamp.
Attaches the screenshot to the Allure report. Prints a console message showing the screenshot path."""
@pytest.hookimpl()
def pytest_bdd_after_step(request, scenario, step):
    page = getattr(request.node, "_page", None)
    if not page or page.is_closed():
        return

    screenshots_dir = Path("reports/screenshots/steps")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Clean scenario and steps name
    safe_scenario = sub(r'[\\/*?:"<>|]', "_", scenario.name.replace(" ", "_"))
    safe_step = sub(r'[\\/*?:"<>|]', "_", step.name.replace(" ", "_").replace("/", "_").replace('"', ""))

    filename = f"{safe_scenario}_{step.keyword}_{safe_step}_{timestamp}.png"
    screenshot_path = screenshots_dir / filename

    try:
        page.screenshot(path=str(screenshot_path), full_page=True)

        #Add to Allure
        allure.attach.file(
            str(screenshot_path),
            name=f"{step.keyword} {step.name}",
            attachment_type=allure.attachment_type.PNG
        )
        print(f"📸 Screenshot of step: {screenshot_path}")
    except Exception as e:
        print(f"⚠️ Error taking screenshot of step: {e}")

"""Obtain latest browser launched in the HTML report (inside every test)"""
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    browser_name = item.config.getoption("--browser", "chromium")
    allure.dynamic.parameter("Browser", browser_name)

"""Playwright session fixture --> Initializes Playwright once per test session (scope="session"):
with sync_playwright() as p: starts Playwright and automatically closes it at the end.
Returns the Playwright instance p."""
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

#Page-specific fixtures --> Returns a ProductsPage object, giving access to its methods and selectors.
@pytest.fixture
def products_page(page):
    return ProductsPage(page)

# ---------- GIVEN ----------
@given("the user is on the login page", target_fixture="login_page")
def go_to_login(page):
    page.goto("https://www.saucedemo.com")
    page.wait_for_load_state("networkidle")
    return LoginPage(page)

@given("tiene un producto en el carrito", target_fixture="cart_page")
def product_in_cart(products_page):
    products_page.add_first_product_to_cart()
    products_page.page.locator(".shopping_cart_link").click()
    products_page.page.wait_for_url("**/cart.html")
    cart = CartPage(products_page.page)
    assert cart.product_count() == 1
    return cart

# ---------- WHEN ----------
@when(parsers.parse("the user logs in with {username} and {password}")) #'parsers.parse' allows capturing {username} and {password} from the login.feature and passing them as arguments to the step function.
def valid_login(login_page, username, password):
    login_page.login(username, password)

@when("agrega un producto al carrito")
def add_product(products_page):
    products_page.add_first_product_to_cart()

@when("completa el checkout", target_fixture="checkout_page")
def complete_checkout(cart_page):
    cart_page.go_to_checkout()
    checkout = CheckoutPage(cart_page.page)
    checkout.complete_checkout("Alexis", "Perez", "08020")
    return checkout

# ---------- THEN ----------
@then("access the system")
def access_system(page):
    assert "inventory" in page.url

@then(parsers.parse("an error message {message} is shown"))
def error_login_message(login_page, message): #login_page is the LoginPage instance that has the ERROR_BTN selector
    login_page.page.wait_for_selector(LoginPage.ERROR_MSG, timeout=5000) #Wait until error message is shown
    error_text = login_page.page.text_content(LoginPage.ERROR_MSG)
    assert message in error_text, f"Expected '{message}' in '{error_text}'"

@then("tap on Error button of error message")
def error_button_login(login_page):
    login_page.login_error_button()
    assert not login_page.page.locator(LoginPage.ERROR_BTN).is_visible()

@then("should be able to see the products list")
def see_products(products_page):
    assert products_page.has_products()

@then("el carrito debe tener 1 producto")
def verify_cart(products_page):
    assert products_page.cart_badge_count() == 1

@then("debe ver el mensaje de confirmación")
def checkout_success(checkout_page):
    assert "Thank you" in checkout_page.get_success_message()