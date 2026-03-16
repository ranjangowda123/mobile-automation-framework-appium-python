import subprocess
import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException ,TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from utils.safe_actions import safe_click
from utils.uploads import push_test_pdf


def test_background_notificaiton_sync(driver):
    email = "testuser5203@gmail.com"
    try:
        google_button = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located((AppiumBy.XPATH,'//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup[6]')))
        google_button.click()
    except (TimeoutException, NoSuchElementException):
        driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiScrollable(new UiSelector().scrollable(true))'
                            '.scrollIntoView(new UiSelector().text("By clicking continue I agree to the"))')
        WebDriverWait(driver, 20).until(
            expected_conditions.element_to_be_clickable((AppiumBy.XPATH,
                                                         '//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup[@clickable="true" and @enabled="true"]'))).click()
    WebDriverWait(driver, 20).until(
        expected_conditions.visibility_of_element_located((AppiumBy.ID, "com.google.android.gms:id/main_title")))
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{email}")').click()
    WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((
                    AppiumBy.ACCESSIBILITY_ID,"AI Tutor"))).click()
    resultcheck,filename = push_test_pdf()
    subprocess.run(
        f'adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Download/{filename}',
        shell=True)
    safe_click(driver, (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Upload Document")'))
    WebDriverWait(driver, 20).until(
        expected_conditions.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Downloads").instance(1)')))
    try:
        click_doc = WebDriverWait(driver,10).until(
            expected_conditions.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,f'new UiSelector().text("{filename}")')))
        print("element id",click_doc)
    except NoSuchElementException:
        click_doc = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                            f'new UiScrollable(new UiSelector().scrollable(true))'
                            f'.scrollIntoView(new UiSelector().text("{filename}"))')
    print("clckinggggggggggg")
    click_doc.click()
    print("Clicked on doc..............")
    time.sleep(1)
    driver.background_app(5)
    verify_text = WebDriverWait(driver, 20).until(
        expected_conditions.visibility_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Choose Your Tutor")'))).text
    assert "Choose Your Tutor" in verify_text
