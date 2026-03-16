from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def check_radio_from_listening(driver):
    click_on_box = driver.find_element(AppiumBy.XPATH,'//android.widget.TextView[@text="Listen to the audio below"]/following-sibling::android.view.ViewGroup[4]/android.view.ViewGroup')
    try:
        next_button = WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Next")))
    except (TimeoutException, NoSuchElementException):
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector().description("Next"))')
        next_button = WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Next")))
    click_on_box.click()
    next_button.click()

def handel_input_in_listening(driver):
    enter_value = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Write your answer here")')
    try:
        next_button = WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Next")))
    except (TimeoutException, NoSuchElementException):
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector().description("Next"))')
        next_button = WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Next")))
    enter_value.send_keys("testuser")
    next_button.click()