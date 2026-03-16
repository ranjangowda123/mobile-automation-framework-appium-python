from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def handel_launch_stability(driver):
    WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login or create an account")')))



