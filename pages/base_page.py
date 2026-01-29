class BasePage: #Methods (functions) and attributes (data).

    """Constructor Method --> __init__ is the constructor of the class. It runs automatically when an object of the class is created:
    page represents a web page object (probably a Page object from Playwright).
    self.page = page stores the page in the object so other methods can use it."""
    def __init__(self, page):
        self.page = page

    #This method clicks an element after waiting for it to be visible:
    def click(self, selector):
        locator = self.page.locator(selector)
        locator.wait_for(state="visible")
        locator.wait_for(state="attached")
        locator.click()

    #This method types text into a field:
    def fill(self, selector, value):
        self.page.locator(selector).fill(value)

    #This method returns True if the element is visible, otherwise False:
    def is_visible(self, selector) -> bool:
        return self.page.locator(selector).is_visible()

    #This method returns how many elements match the selector (returns an integer):
    def count(self, selector) -> int:
        return self.page.locator(selector).count()

    #This returns the text of an element (returns a string):
    def text(self, selector) -> str:
        return self.page.locator(selector).inner_text()