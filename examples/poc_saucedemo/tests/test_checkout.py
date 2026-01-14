import pytest
import time
from qa_framework.core.data.readers import JSONReader
from examples.poc_saucedemo.pages.login_page import LoginPage
from examples.poc_saucedemo.pages.inventory_page import InventoryPage

# Load Test Data
data_reader = JSONReader("examples/poc_saucedemo/data/test_data.json")
test_data = data_reader.read()

class TestSauceDemoCheckout:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.inventory_page = InventoryPage(driver)

    def test_e2e_purchase_flow(self):
        """
        Validates the End-to-End purchase flow: Login -> Add to Cart -> Verify Cart.
        """
        user = test_data['valid_user']
        
        # 1. Login
        self.login_page.navigate()
        self.login_page.login(user['username'], user['password'])
        
        # 2. Verify Inventory Page
        assert "PRODUCTS" in self.inventory_page.get_title().upper()
        
        # 3. Add Item to Cart
        self.inventory_page.add_backpack_to_cart()
        
        # 4. Verify Cart Badge
        assert self.inventory_page.get_cart_count() == "1"
        
        # 5. Go to Cart (Optional visual check)
        self.inventory_page.go_to_cart()
        
    def test_locked_out_user(self):
        """
        Validates error handling for locked out users.
        """
        user = test_data['locked_user']
        
        self.login_page.navigate()
        self.login_page.login(user['username'], user['password'])
        
        error = self.login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error
