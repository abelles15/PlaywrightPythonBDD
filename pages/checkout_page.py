#Import the BasePage and by inheriting from BasePage, CheckoutPage can use all BasePage methods (click, fill, is_visible, etc.) without redefining them:
from pages.base_page import BasePage

class CheckoutPage(BasePage): #CheckoutPage inherits from BasePage (can use all the generic methods like click and text from BasePage, and also define its own page-specific actions)

    #CSS Selectors for elements on the checkout page:
    FIRST_NAME = "#first-name"
    LAST_NAME = "#last-name"
    POSTAL_CODE = "#postal-code"
    CONTINUE_BTN = "#continue"
    FINISH_BTN = "#finish"
    COMPLETE_HEADER = ".complete-header"

    #Fill in checkout form and finalize purchase:
    def complete_checkout(self, first, last, postal_code):
        self.fill(self.FIRST_NAME, first) #Fill first name using self.fill() from BasePage
        self.fill(self.LAST_NAME, last) #Fill last name
        self.fill(self.POSTAL_CODE, postal_code) #Fill postal code
        self.click(self.CONTINUE_BTN) #Click the Continue button using self.click() from BasePage
        self.click(self.FINISH_BTN) #Click the Finish button to complete checkout

    #Get the success message displayed after checkout (returns a string):
    def get_success_message(self) -> str:
        return self.page.locator(self.COMPLETE_HEADER).inner_text() #Finds the element and inner_text() extracts the text