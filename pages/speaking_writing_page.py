from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException

from utils.crash_detector import check_for_crash_or_anr
from utils.safe_actions import safe_gesture_click
from utils.scroll_utils import scroll_to_description
from utils.waits import wait_for_visibility, wait_for_clickable


class SpeakingWritingPage:

    def __init__(self, driver):
        self.driver = driver

    mic_start_locator = (AppiumBy.XPATH,
                         '(//android.widget.TextView[@text="Recording will start in"]/preceding-sibling::android.view.ViewGroup[@clickable="true"])[1]')
    mic_stop_locator_length = (AppiumBy.XPATH,
                               '//android.widget.TextView[@text="QUESTION 1"]/following-sibling::android.view.ViewGroup[@clickable="true"]')
    mic_stop_locator = (AppiumBy.XPATH,
                        '//android.widget.TextView[@text="QUESTION 1"]/following-sibling::android.view.ViewGroup[@clickable="true" and @enabled="true"]')
    submit_button = (AppiumBy.ACCESSIBILITY_ID, 'Submit')


    def start_mic(self):
        try:
            mic_start = wait_for_visibility(self.driver, self.mic_start_locator)
        except (TimeoutException, NoSuchElementException):
            scroll_to_description(self.driver,"Recording will start in")
            mic_start = wait_for_visibility(self.driver, self.mic_start_locator)
            """This is an Appium mobile command.
            It tells Android:
            Perform a REAL touch gesture on this element.
            """
        safe_gesture_click(self.driver, mic_start)
        check_for_crash_or_anr(self.driver)

    def mic_stop(self):
        for _ in range(5):
            try:
                elements = self.driver.find_elements(*self.mic_stop_locator_length)
                print("Found:", len(elements))
                if elements:
                    mic_stop = elements[0]
                    safe_gesture_click(self.driver, mic_stop)
                    print("clicked.........................")
                    break
            except (StaleElementReferenceException, TimeoutException):
                continue

    def click_on_submit(self):
        try:
            submit_button = wait_for_clickable(self.driver, self.submit_button)
        except TimeoutException:
            scroll_to_description(self.driver,self.submit_button)
            submit_button = wait_for_clickable(self.driver, self.submit_button)
        submit_button.click()
