from selenium import webdriver
from test_lib import (
    wait_click,
    wait_write,
    wait_read,
    styled_error,
    styled_success,
    styled_warning,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# --- GLOBAL SETTINGS ---
keyword = "Yoda"
url = "https://www.lego.com" + "/en-us"


# --- TESTING OBJECTS ---
class Driver(webdriver.Chrome):
    def __init__(self, headless=True, window_size=(1920, 995)):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")

        super().__init__(options=options)
        self.set_window_size(*window_size)


class Counter:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def total(self):
        return self.passed + self.failed

    def pass_test(self):
        self.passed += 1

    def fail_test(self):
        self.failed += 1

    def is_all_passed(self):
        return not self.failed


# --- HELPER FUNCTIONS ---
def data_test(value):
    return f"[data-test='{value}']"


# --- PRINTING FUNCTIONS ---
def print_critical_msg(error):
    print(styled_error("Test failed because of a blocker!"))
    print(styled_error("Error: " + error))


def print_suite_success_msg(counter=Counter()):
    print("\n")
    if counter.passed:
        print(
            test_status_template(
                counter.passed, counter.total(), "PASSED", styled_success
            )
        )
    if counter.failed:
        print(
            test_status_template(
                counter.failed, counter.total(), "FAILED", styled_error
            )
        )
    print("\n")

    if counter.is_all_passed():
        print(suite_status_template("PASS", styled_success))
    elif counter.passed:
        print(suite_status_template("PARTIALLY PASSED", styled_warning))
    else:
        print(suite_status_template("FAIL", styled_error))


# --- TEMPLATE FUNCTIONS ---
def test_status_template(count, total, status, style):
    return style(
        f"================== {count} out of {total} tests {status} =================="
    )


def suite_status_template(status, style):
    return style(f"================== SUITE STATUS: {status} ==================")


# --- ASSERTION FUNCTIONS ---
def test(assertion, name, counter=Counter()):
    if assertion:
        print(styled_success(f"Test passed: ") + name)
        counter.pass_test()
    else:
        print(styled_error("Test failed: ") + name)
        counter.fail_test()


# --- PAGE OBJECTS ---
class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def navigate(self, url):
        self.driver.get(url)

    def accept_cookies_and_age_gate(self):
        wait_click(self.driver, self._grownUpBtn_selector)
        wait_click(self.driver, self._cookieAcptBtn_selector)

    def search_for_keyword(self, keyword):
        wait_click(self.driver, self._searchBtn_selector)
        wait_write(self.driver, self._searchInpt_selector, keyword)
        wait_write(self.driver, self._searchInpt_selector, Keys.ENTER)

    _grownUpBtn_selector = data_test("age-gate-grown-up-cta")
    _cookieAcptBtn_selector = data_test("cookie-accept-all")
    _searchBtn_selector = data_test("search-input-button")
    _searchInpt_selector = data_test("search-input")


class SearchResultsPage:
    def __init__(self, driver):
        self.driver = driver

    def get_search_title(self):
        return wait_read(self.driver, self._listingSummary_selector)

    def get_number_of_results(self):
        number_of_results_element = self.driver.find_element(
            By.CSS_SELECTOR, self._resultCount_selector
        )
        return int(number_of_results_element.get_attribute("data-value"))

    def add_first_product_to_cart(self):
        wait_click(self.driver, self._addToCartBtn_selector)
        wait_click(self.driver, self._modalCloseBtn_selector)

    def get_product_title(self):
        product_leaf = self.driver.find_element(
            By.CSS_SELECTOR, self._productLeaf_selector
        )
        return wait_read(product_leaf, self._productLeafTitle_selector)

    _listingSummary_selector = data_test("listing-summary") + " span span"
    _resultCount_selector = data_test("result-count")
    _addToCartBtn_selector = data_test("add-to-cart-skroll-cta")
    _modalCloseBtn_selector = data_test("modal-close")
    _productLeaf_selector = data_test("product-leaf")
    _productLeafTitle_selector = data_test("product-leaf-title")


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_cart(self):
        wait_click(self.driver, self._cartBtn_selector)

    def get_cart_product_title(self):
        return wait_read(self.driver, self._productTitle_selector)

    _cartBtn_selector = data_test("util-bar-cart")
    _productTitle_selector = data_test("product-title")


# --- TEST FLOW ---
def test_flow():
    counter = Counter()
    driver = Driver()

    home_page = HomePage(driver)
    search_page = SearchResultsPage(driver)
    cart_page = CartPage(driver)
    try:
        home_page.navigate(url)
        home_page.accept_cookies_and_age_gate()
        home_page.search_for_keyword(keyword)

        test(
            keyword == search_page.get_search_title(),
            f"The search title is {keyword}",
            counter,
        )
        test(
            search_page.get_number_of_results() > 1,
            f"There are more than 1 result",
            counter,
        )

        search_page.add_first_product_to_cart()
        product_title = search_page.get_product_title()

        cart_page.navigate_to_cart()
        cart_product_title = cart_page.get_cart_product_title()

        test(
            cart_product_title == product_title,
            "The product was succesfully added to cart",
            counter,
        )

        return print_suite_success_msg(counter)
    except Exception as e:
        return print_critical_msg(e)
    finally:
        driver.quit()


if __name__ == "__main__":
    test_flow()
