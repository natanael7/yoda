import time
from selenium.webdriver.common.by import By

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# --- PRINT FUNCTIONS ---
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def styled_msg(style, msg):
    return getattr(bcolors, style) + msg + bcolors.ENDC


def styled_error(msg):
    return styled_msg("FAIL", msg)


def styled_success(msg):
    return styled_msg("OKGREEN", msg)


def styled_warning(msg):
    return styled_msg("WARNING", msg)


def print_error(error):
    print(styled_msg("FAIL", "Error: "), styled_msg("UNDERLINE", error))


def print_action(action, target, value=None):
    if value != None:
        value_str = " - " + styled_msg("HEADER", value)
    else:
        value_str = ""
    print(
        styled_msg("OKCYAN", action)
        + ": "
        + styled_msg("UNDERLINE", target)
        + value_str
    )


def print_prompt(prompt):
    print(styled_msg("OKGREEN", "Prompt: ") + styled_msg("BOLD", prompt))


# --- WAIT FUNCTIONS ---


def wait_selector(driver, selector, xpath, timeout):
    try:
        by = By.CSS_SELECTOR
        if xpath:
            by = By.XPATH

        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((by, selector)))
        return True
    except:
        print_error("Selector {} not found".format(selector))
        return False


def wait_clickable(driver, selector, xpath, timeout):
    try:
        by = By.CSS_SELECTOR
        if xpath:
            by = By.XPATH

        wait = WebDriverWait(driver, timeout)
        wait.until(EC.element_to_be_clickable((by, selector)))
        return True
    except:
        print_error("Selector {} not clickable".format(selector))
        return False


# --- WAIT FUNCTIONS ---


# --- CRUD FUNCTIONS ---
def clear(driver, selector, xpath):
    by = By.CSS_SELECTOR
    if xpath:
        by = By.XPATH
    driver.find_element(by, selector).clear()


def write(driver, selector, input, xpath):
    by = By.CSS_SELECTOR
    if xpath:
        by = By.XPATH
    driver.find_element(by, selector).send_keys(input)


def click(driver, selector, xpath):
    by = By.CSS_SELECTOR
    if xpath:
        by = By.XPATH
    driver.find_element(by, selector).click()


def read(driver, selector, xpath):
    by = By.CSS_SELECTOR
    if xpath:
        by = By.XPATH
    return driver.find_element(by, selector).text


def read_all(driver, selector, xpath):
    by = By.CSS_SELECTOR
    if xpath:
        by = By.XPATH

    elements = driver.find_elements(by, selector)
    text_of_elements = [
        el.get_attribute("textContent")
        for el in elements
        if el.get_attribute("style").replace(" ", "").lower() != "display:none;"
    ]
    return text_of_elements


# --- CRUD FUNCTIONS - --


# --- WAIT & CRUD FUNCTIONS - --
def wait_write(driver, selector, input, xpath=False, timeout=3):
    if wait_selector(driver, selector, xpath, timeout):
        # clear(driver, selector)
        write(driver, selector, input, xpath)
        return True
    return False


def wait_click(driver, selector, xpath=False, timeout=3):
    if wait_selector(driver, selector, xpath, timeout):
        if wait_clickable(driver, selector, xpath, timeout):
            click(driver, selector, xpath)
            return True
    return False


def wait_read(driver, selector, xpath=False, timeout=3):
    if wait_selector(driver, selector, xpath, timeout):
        return read(driver, selector, xpath)
    return False


def wait_read_all(driver, selector, xpath=False, timeout=3):
    if wait_selector(driver, selector, xpath, timeout):
        return read_all(driver, selector, xpath)
    return False


# --- WAIT & CRUD FUNCTIONS - --
