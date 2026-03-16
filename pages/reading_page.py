from appium.webdriver.common.appiumby import AppiumBy

from utils.handel_reading_section import handel_input_in_reading, check_radio_button_from_reading
from utils.waits import wait_for_visibility


class ReadingPage:

    def __init__(self, driver):
        self.driver = driver

    reading = (AppiumBy.ACCESSIBILITY_ID, 'Reading, 3 mins')
    check_text = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    wait_for_reading_screen  =  (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Diagnostic test - reading")')


    def click_on_reading(self):
        self.driver.find_element(*self.reading).click()

    def start_reading_section(self):
        for i in range(2):
            wait_for_visibility(self.driver,self.wait_for_reading_screen)
            edit_text = self.driver.find_elements(*self.check_text)
            if edit_text:
                handel_input_in_reading(self.driver)
            else:
                check_radio_button_from_reading(self.driver)