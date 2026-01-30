#Import the BasePage and by inheriting from BasePage, LoginPage can use all BasePage methods (click, fill, is_visible, etc.) without redefining them:
from pages.base_page import BasePage

class LoginPage(BasePage): #LoginPage inherits from BasePage (can use all the generic methods like click and text from BasePage, and also define its own page-specific actions)
    
    #CSS selectors for elements on the login page:
    USERNAME = "#user-name" #<input class="input_error form_input" placeholder="Username" type="text" data-test="username" id="user-name" name="user-name" autocorrect="off" autocapitalize="none" value="">
    PASSWORD = "#password" #<input class="input_error form_input" placeholder="Password" type="password" data-test="password" id="password" name="password" autocorrect="off" autocapitalize="none" value="">
    LOGIN_BTN = "#login-button" #<input type="submit" class="submit-button btn_action" data-test="login-button" id="login-button" name="login-button" value="Login">
    ERROR_MSG = '[data-test="error"]' #<h3 data-test="error"><button class="error-button" data-test="error-button"><svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="times" class="svg-inline--fa fa-times fa-w-11 " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 352 512"><path fill="currentColor" d="M242.72 256l100.07-100.07c12.28-12.28 12.28-32.19 0-44.48l-22.24-22.24c-12.28-12.28-32.19-12.28-44.48 0L176 189.28 75.93 89.21c-12.28-12.28-32.19-12.28-44.48 0L9.21 111.45c-12.28 12.28-12.28 32.19 0 44.48L109.28 256 9.21 356.07c-12.28 12.28-12.28 32.19 0 44.48l22.24 22.24c12.28 12.28 32.2 12.28 44.48 0L176 322.72l100.07 100.07c12.28 12.28 32.2 12.28 44.48 0l22.24-22.24c12.28-12.28 12.28-32.19 0-44.48L242.72 256z"></path></svg></button>Epic sadface: Sorry, this user has been locked out.</h3>
    ERROR_BTN = '[data-test="error-button"]' #Same as ERROR_MSG

    #Collect login URL
    def login_url(self):
        return self.page.url

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