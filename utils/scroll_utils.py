from appium.webdriver.common.appiumby import AppiumBy


def scroll_to_text(driver,text):
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{text}"))')

def scroll_to_description(driver,desc):
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().description("{desc}"))')