#Import the BasePage and by inheriting from BasePage, ProductsPage can use all BasePage methods (click, fill, is_visible, etc.) without redefining them:
from pages.base_page import BasePage

class ProductsPage(BasePage): #ProductsPage inherits from BasePage (can use all the generic methods like click and text from BasePage, and also define its own page-specific actions)

    #CSS selectors for elements on the products page:
    INVENTORY_ITEMS = ".inventory_item"
    ADD_TO_CART_BTN = ".inventory_item button"
    CART_LINK = ".shopping_cart_link"
    CART_BADGE = ".shopping_cart_badge"

    #Checks if there are products on the page (returns True if there is at least one product on the page, otherwise False):
    def has_products(self) -> bool:
        return self.count(self.INVENTORY_ITEMS) > 0 #Counts elements matching the INVENTORY_ITEMS selector

    #Adds the first product to the shopping cart:
    def add_first_product_to_cart(self):
        self.page.locator(self.ADD_TO_CART_BTN).first.click() #self.page.locator(self.ADD_TO_CART_BTN).first selects the first "Add to Cart" button and click() method inherited clicks it

    #Opens the shopping cart page:
    def open_cart(self):
        self.click(self.CART_LINK) #Uses the click() method inherited from BasePage

    #Returns the number of items in the cart badge:
    def cart_badge_count(self) -> int:
        if self.page.locator(self.CART_BADGE).is_visible(): #Checks if the cart badge is visible inherited from BasePage
            return int(self.text(self.CART_BADGE)) #If visible, gets its text with text() (also from BasePage) and converts it to an integer
        return 0 #If not visible, returns 0