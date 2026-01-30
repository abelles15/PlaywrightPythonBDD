from pages.base_page import BasePage #Import the BasePage and by inheriting from BasePage, ProductsPage can use all BasePage methods (click, fill, is_visible, etc.) without redefining them
from pages.login_page import LoginPage

class ProductsPage(BasePage): #ProductsPage inherits from BasePage (can use all the generic methods like click and text from BasePage, and also define its own page-specific actions)

    #CSS selectors for elements on the products page:
    INVENTORY_ITEMS = ".inventory_item" #<div class="inventory_item" data-test="inventory-item"><div class="inventory_item_img"><a href="#" id="item_0_img_link" data-test="item-0-img-link"><img alt="Sauce Labs Bike Light" class="inventory_item_img" src="/static/media/bike-light-1200x1500.37c843b09a7d77409d63.jpg" data-test="inventory-item-sauce-labs-bike-light-img"></a></div><div class="inventory_item_description" data-test="inventory-item-description"><div class="inventory_item_label"><a href="#" id="item_0_title_link" data-test="item-0-title-link"><div class="inventory_item_name " data-test="inventory-item-name">Sauce Labs Bike Light</div></a><div class="inventory_item_desc" data-test="inventory-item-desc">A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.</div></div><div class="pricebar"><div class="inventory_item_price" data-test="inventory-item-price">$9.99</div><button class="btn btn_primary btn_small btn_inventory " data-test="add-to-cart-sauce-labs-bike-light" id="add-to-cart-sauce-labs-bike-light" name="add-to-cart-sauce-labs-bike-light">Add to cart</button></div></div></div>
    ADD_TO_CART_BTN = ".inventory_item button" #Same as INVENTORY_ITEMS
    CART_LINK = ".shopping_cart_link" #<a class="shopping_cart_link" data-test="shopping-cart-link"></a>
    CART_BADGE = ".shopping_cart_badge" #<span class="shopping_cart_badge" data-test="shopping-cart-badge">2</span>
    MENU_BTN = "#react-burger-menu-btn" #<button type="button" id="react-burger-menu-btn" >Open Menu</button>
    LOGOUT_MENU = "#logout_sidebar_link" #<a id="logout_sidebar_link" class="bm-item menu-item" href="#" data-test="logout-sidebar-link" style="display: block;">Logout</a>

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

    #Open menu and tap Logout   
    def logout(self):
        self.click(self.MENU_BTN)
        self.page.wait_for_selector(self.LOGOUT_MENU)
        self.click(self.LOGOUT_MENU)
        self.page.wait_for_url("https://www.saucedemo.com/")
        return LoginPage(self.page)