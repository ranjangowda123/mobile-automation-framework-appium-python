from appium.webdriver.common.appiumby import AppiumBy


def check_for_crash_or_anr(driver):
    crash_elements = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().textContains("stopping")')
    anr_elements = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().textContains("responding")')
    if crash_elements:
        raise AssertionError("App crash detected (keeps stopping)")
    elif anr_elements:
        raise AssertionError("ANR detected (isn't responding)")
    else:
        print("No crash/ANR detected — continuing")