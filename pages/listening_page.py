from appium.webdriver.common.appiumby import AppiumBy

from utils.crash_detector import check_for_crash_or_anr
from utils.handel_listening_section import check_radio_from_listening, handel_input_in_listening
from utils.waits import wait_for_visibility


class ListeningPage:


    def __init__(self, driver):
        self.driver = driver

    listen = (AppiumBy.ACCESSIBILITY_ID, 'Listening, 3 mins')
    wait_for_listen_screen = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Diagnostic test - listening")')
    input_screen = (AppiumBy.CLASS_NAME, "android.widget.EditText")

    def click_on_listen(self):
        self.driver.find_element(*self.listen).click()

    def wait_for_listening_screen(self):
        wait_for_visibility(self.driver, self.wait_for_listen_screen)

    def start_listening_section(self):
        for i in range(2):
            input_field = self.driver.find_elements(*self.input_screen)
            if input_field:
                handel_input_in_listening(self.driver)
            else:
                check_radio_from_listening(self.driver)
        check_for_crash_or_anr(self.driver)