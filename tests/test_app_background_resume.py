from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException ,TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def test_app_from_background(driver):
    # 👉 Use noReset=true ✅
    # 1️⃣ Ensure app is on expected screen
    email = "testuser5203@gmail.com"
    try:
        google_button = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located((AppiumBy.XPATH,
                                                               '//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup[6]')))
        google_button.click()
    except (TimeoutException, NoSuchElementException):
        driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiScrollable(new UiSelector().scrollable(true))'
                            '.scrollIntoView(new UiSelector().text("By clicking continue I agree to the"))')
        WebDriverWait(driver, 20).until(
            expected_conditions.element_to_be_clickable((AppiumBy.XPATH,
                                                         '//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup[@clickable="true" and @enabled="true"]'))).click()
    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located((AppiumBy.ID, "com.google.android.gms:id/main_title")))
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{email}")').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Profile').click()
    WebDriverWait(driver,10).until(
        expected_conditions.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,f'new UiSelector().text("{email}")'))).click()
    driver.find_element(AppiumBy.XPATH,'//android.widget.TextView[@text="First Name"]/following-sibling::android.widget.EditText[1]').send_keys("check app in background")
    #2️⃣ Send app to background for 5 seconds
    driver.background_app(5)
    # 3️⃣ Bring app to foreground (usually automatic after timeout)
    # If needed explicitly:
    # driver.activate_app("com.konze.tutor")
    # 4️⃣ Verify correct screen still visible
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@text="First Name"]')))
    # 5️⃣ Verify no crash (anchor element still interactable)
    verify_text = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Edit Profile")')
    assert verify_text.is_displayed()