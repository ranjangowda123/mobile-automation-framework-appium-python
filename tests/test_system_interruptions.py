import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException ,TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def test_system_interruptions(driver):
    # Trigger Notificaton interruption
    email = "testuser5203@gmail.com"
    try:
        google_button = WebDriverWait(driver,10).until(
            expected_conditions.visibility_of_element_located((AppiumBy.XPATH,'(//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup)[6]')))
        google_button.click()
    except (TimeoutException, NoSuchElementException):
        driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiScrollable(new UiSelector().scrollable(true))'
                '.scrollIntoView(new UiSelector().text("By clicking continue I agree to the"))')
        WebDriverWait(driver,20).until(
            expected_conditions.element_to_be_clickable((AppiumBy.XPATH,'//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup[@clickable="true" and @enabled="true"]'))).click()
    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located((AppiumBy.ID, "com.google.android.gms:id/main_title")))
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{email}")').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Profile').click()
    driver.open_notifications()
    time.sleep(2)
    driver.press_keycode(4)  # Android back button
    verify_email = WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{email}")')))
    assert verify_email.text == email
