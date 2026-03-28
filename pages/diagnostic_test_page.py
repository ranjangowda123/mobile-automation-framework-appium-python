from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException, TimeoutException
from utils.scroll_utils import scroll_to_text
from utils.waits import wait_for_visibility


class DiagnosticTestPage:

    def __init__(self, driver):
        self.driver = driver

    wait_for_quick_diagonstic_test = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Quick 10 min Diagnostic test")')
    speaking_writing = (AppiumBy.ACCESSIBILITY_ID, 'Speaking & Writing, 4 mins')
    wait_for_diagonstic_write = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Diagnostic test - writing")')
    answer1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Write your answer here")')
    wait_for_diagonstic_speak = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Diagnostic test - Speaking")')
    select_technology = (AppiumBy.ACCESSIBILITY_ID, 'Technology')

    def wait_for_quick_diagnostic_test_page(self):
        wait_for_visibility(self.driver,self.wait_for_quick_diagonstic_test)

    def click_on_speak_and_write(self):
        self.driver.find_element(*self.speaking_writing).click()

    def wait_for_diagnostic_write_page(self):
        wait_for_visibility(self.driver,self.wait_for_diagonstic_write)

    def enter_answers(self,profile_details_page):
        for _ in range(2):
            try:
                diagnostic_write = wait_for_visibility(self.driver,self.answer1)
            except(NoSuchElementException, TimeoutException):
                scroll_to_text(self.driver,"Write your answer here")
                diagnostic_write = wait_for_visibility(self.driver,self.answer1)
            diagnostic_write.send_keys("test")
            profile_details_page.click_on_next_button()

    def wait_for_diagnostic_speaking(self):
        wait_for_visibility(self.driver,self.wait_for_diagonstic_speak)
        self.driver.find_element(*self.select_technology).click()
        wait_for_visibility(self.driver,self.wait_for_diagonstic_speak)
