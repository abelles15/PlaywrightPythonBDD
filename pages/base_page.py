class BasePage: #Methods (functions) and attributes (data).

    """Constructor Method --> __init__ is the constructor of the class. It runs automatically when an object of the class is created:
    page represents a web page object (probably a Page object from Playwright).
    self.page = page stores the page in the object so other methods can use it."""
    def __init__(self, page):
        self.page = page

    #This method clicks an element. First find the element, use the first one if there are several, wait until it becomes visible, click (forced or not) and if it fails → clear and understandable error:
    def click(self, selector: str, *, timeout: int = 5000, force: bool = False):
        locator = self.page.locator(selector).first
        try:
            locator.wait_for(state="visible", timeout=timeout)
            locator.click(force=force, timeout=timeout)
        except Exception as e:
            raise AssertionError(
                f"❌ Could not click element '{selector}'"
            ) from e

    #This method types text into a field:
    def fill(self, selector, value):
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible")
        locator.fill(value)

    #This method returns True if the element is visible, otherwise False:
    def is_visible(self, selector) -> bool:
        return self.page.locator(selector).is_visible()

    #This method returns how many elements match the selector (returns an integer):
    def count(self, selector) -> int:
        return self.page.locator(selector).count()

    #This method returns the text of an element (returns a string):
    def text(self, selector) -> str:
        return self.page.locator(selector).inner_text()