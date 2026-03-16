from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def handel_input_in_reading(driver):
    try:
        enter_value = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().textContains("Write answer")')
    except NoSuchElementException:
        enter_value = driver.find_element(AppiumBy.XPATH,'//android.widget.EditText[@hint="Write your answer here"]')
    for btn_name in ["Next", "Submit"]:
        try:
            next_sbmt_btm = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, btn_name)))
        except (TimeoutException, NoSuchElementException):
            try:
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiScrollable(new UiSelector().scrollable(true))'
                    f'.scrollIntoView(new UiSelector().description("{btn_name}"))')
                next_sbmt_btm = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, btn_name)))
            except (TimeoutException, NoSuchElementException):
                continue  # 🔥 important → go check Submit
        enter_value.send_keys("testuser")
        next_sbmt_btm.click()
        break  # stop once clicked

def check_radio_button_from_reading(driver):
    click_on_box = driver.find_element(AppiumBy.XPATH,'//android.widget.TextView[@text="Reading Passage"]/following-sibling::android.view.ViewGroup[1]/android.view.ViewGroup')
    for btn_name in ["Next", "Submit"]:
        try:
            next_sbmt_btm = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, btn_name)))
        except (TimeoutException, NoSuchElementException):
            try:
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiScrollable(new UiSelector().scrollable(true))'
                    f'.scrollIntoView(new UiSelector().description("{btn_name}"))')
                next_sbmt_btm = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, btn_name)))
            except (TimeoutException, NoSuchElementException):
                continue  # 🔥 important → go check Submit
        click_on_box.click()
        next_sbmt_btm.click()
        break  # stop once clicked