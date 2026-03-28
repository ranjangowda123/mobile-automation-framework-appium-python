from appium.webdriver.common.appiumby import AppiumBy

from utils.scroll_utils import scroll_to_description
from utils.waits import wait_for_visibility


class HomePage:


    def __init__(self, driver):
        self.driver = driver

    wait_for_overall_score_page = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OVERALL SCORE")')
    home_button = (AppiumBy.ACCESSIBILITY_ID, "Go To Home")
    verify_home_page = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Let\'s start your learning journey")')


    def wait_for_score_page(self):
        wait_for_visibility(self.driver,self.wait_for_overall_score_page)

    def scroll_till_home_btn_click(self):
        scroll_to_description(self.driver,self.home_button)
        self.driver.find_element(*self.home_button).click()

    def verify_new_registration(self):
        wait_for_visibility(self.driver,self.verify_home_page)
        home_page = self.driver.find_element(*self.verify_home_page).text
        assert "Let's start your learning journey" in home_page