#Import the BasePage and by inheriting from BasePage, LoginPage can use all BasePage methods (click, fill, is_visible, etc.) without redefining them:
from pages.base_page import BasePage

class LoginPage(BasePage): #LoginPage inherits from BasePage (can use all the generic methods like click and text from BasePage, and also define its own page-specific actions)
    
    #CSS selectors for elements on the login page:
    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"
    ERROR_MSG = '[data-test="error"]'

    #Fill username and password, then click the login button:
    def login(self, user, password):
        self.page.wait_for_selector("#user-name") #Waits until the username field is present on the page, preventing timing issues
        self.fill(self.USERNAME, user) #Fills in the username using the fill method from BasePage
        self.fill(self.PASSWORD, password) #Fills in the password
        self.click(self.LOGIN_BTN) #Clicks the login button using the inherited click method from BasePage