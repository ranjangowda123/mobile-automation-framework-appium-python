import subprocess

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException ,TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from utils.uploads import push_test_image
from utils.network_behaviour import disable_wifi


def test_network_drop(driver):
    email = "testuser5203@gmail.com"
    try:
        google_button = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located((AppiumBy.XPATH,
                                                               '(//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup)[6]')))
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

    WebDriverWait(driver,10).until(
        expected_conditions.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Profile'))).click()
    WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{email}")'))).click()
    subprocess.run('adb shell mkdir -p /sdcard/DCIM/Camera', shell=True)
    resultcheck = push_test_image()
    subprocess.run('adb shell touch /sdcard/DCIM/Camera/test_image.png', shell=True)
    subprocess.run('adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/DCIM/Camera/test_image.png',
                   shell=True)
    print("RETURN:", resultcheck.returncode)
    print("STDOUT:", resultcheck.stdout)
    print("STDERR:", resultcheck.stderr)
    driver.find_element(AppiumBy.XPATH,'//android.widget.TextView[@text="Upload image"]/preceding-sibling::android.view.ViewGroup').click()
    WebDriverWait(driver,10).until(
        expected_conditions.visibility_of_element_located((AppiumBy.ID,'android:id/button2'))).click()
    driver.find_element(AppiumBy.XPATH,'(//android.widget.GridView//android.widget.FrameLayout[@content-desc])[1]').click()
    disable_wifi()


    # continue the flow after implementation