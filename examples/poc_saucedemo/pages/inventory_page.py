from .base_page import BasePage

class InventoryPage(BasePage):
    # Selectors
    HEADER_TITLE = "css=.title"
    INVENTORY_LIST = "css=.inventory_list"
    CART_BADGE = "css=.shopping_cart_badge"
    ADD_TO_CART_BACKPACK = "id=add-to-cart-sauce-labs-backpack"
    CART_LINK = "css=.shopping_cart_link"

    def get_title(self):
        return self.driver.get_text(self.HEADER_TITLE)

    def add_backpack_to_cart(self):
        self.driver.click(self.ADD_TO_CART_BACKPACK)

    def get_cart_count(self):
        return self.driver.get_text(self.CART_BADGE)
        
    def go_to_cart(self):
        self.driver.click(self.CART_LINK)
