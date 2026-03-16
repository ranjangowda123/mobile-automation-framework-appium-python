from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def wait_for_visibility(driver, locator):
    return WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located(locator))


def wait_for_presence(driver, locator):
    return WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(locator))


def wait_for_clickable(driver, locator):
    return WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable(locator))


def wait_for_invisibility(driver, locator):
    return WebDriverWait(driver, 20).until(expected_conditions.invisibility_of_element_located(locator))