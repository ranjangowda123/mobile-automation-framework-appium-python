from appium.webdriver.common.appiumby import AppiumBy

from utils.waits import wait_for_visibility


class ChooseExamPage:

    def __init__(self, driver):
        self.driver = driver

    wait_for_select_exam =  (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Choose the exam you\'re preparing for ?")')
    select_exam = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("PTE")')
    choose_exam = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("PTE Acedmic")')


    def wait_for_selecting_exam(self):
        wait_for_visibility(self.driver,self.wait_for_select_exam)

    def selecting_exam(self):
        self.driver.find_element(*self.select_exam).click()

    def choosing_exam(self):
        self.driver.find_element(*self.choose_exam).click()