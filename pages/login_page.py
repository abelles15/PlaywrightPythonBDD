#Import the BasePage and by inheriting from BasePage, LoginPage can use all BasePage methods (click, fill, is_visible, etc.) without redefining them:
from pages.base_page import BasePage

class LoginPage(BasePage): #LoginPage inherits from BasePage (can use all the generic methods like click and text from BasePage, and also define its own page-specific actions)
    
    #CSS selectors for elements on the login page:
    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"
    ERROR_MSG = '[data-test="error"]'
    ERROR_BTN = '[data-test="error-button"]'

    #Fill username and password, then click the login button:
    def login(self, user, password):
        self.page.wait_for_selector("#user-name") #Waits until the username field is present on the page, preventing timing issues
        self.fill(self.USERNAME, user) #Fills in the username using the fill method from BasePage
        self.fill(self.PASSWORD, password) #Fills in the password

        if user == "performance_glitch_user": #For performance_glitch_user, expect no network traffic
            self.page.wait_for_load_state("networkidle") 
        timeout = 15000 if user == "performance_glitch_user" else 5000 #Dynamic timeout depending the user (15000 for performance_glitch_user that has a delay, 5000 for the rest)

        self.click(self.LOGIN_BTN, timeout=timeout) #Clicks the login button using the inherited click method from BasePage
    
    #Clicks the error button
    def login_error_button(self):
        self.click(self.ERROR_BTN)