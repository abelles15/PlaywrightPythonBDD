#Import the BasePage and by inheriting from BasePage, CartPage can use all BasePage methods (click, fill, is_visible, etc.) without redefining them:
from pages.base_page import BasePage

class CartPage(BasePage): #CartPage inherits from BasePage (can use all the generic methods like click and text from BasePage, and also define its own page-specific actions)

    URL = "https://www.saucedemo.com/cart.html" #URL of the cart page
    CART_ITEMS = ".cart_item" #CSS selector for items in the cart
    CHECKOUT_BTN = "#checkout" #CSS selector for the checkout button.

    #Navigates the browser to the cart page URL:
    def open(self):
        self.page.goto(self.URL) #Playwright method to open a webpage

    #Returns the number of products in the cart (returns an integer):
    def product_count(self) -> int:
        return self.page.locator(self.CART_ITEMS).count() #Selects all elements that match .cart_item and counts how many elements exist

    def go_to_checkout(self):
        self.click(self.CHECKOUT_BTN) #Clicks the checkout button using the inherited click() method from BasePage
        self.page.wait_for_url("**/checkout-step-one.html") #Waits until the URL changes to the first step of checkout (**/checkout-step-one.html is a pattern that matches the URL regardless of domain or protocol)