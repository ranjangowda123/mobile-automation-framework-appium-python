from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException

from utils.scroll_utils import scroll_to_description
from utils.waits import wait_for_visibility


class PersonalizeExperiencePage:

    def __init__(self, driver):
        self.driver = driver
        self.country_dropdown = None

    personalize_screen = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("personalise your experience?")')
    select_country = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Choose a country")')
    country_options = (AppiumBy.CLASS_NAME, "android.widget.TextView")
    select_week = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select")')
    week_options = (AppiumBy.CLASS_NAME, "android.widget.TextView")
    previous_exam = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("No")')
    previous_score = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.widget.EditText")')
    continue_button = (AppiumBy.ACCESSIBILITY_ID, 'Continue')

    def wait_for_personalize_screen(self):
        wait_for_visibility(self.driver,self.personalize_screen)

    def select_country_button(self):
        self.country_dropdown = wait_for_visibility(self.driver,self.select_country)
        self.country_dropdown.click()

    def choose_country_and_week(self):
        start_y = self.country_dropdown.location['y']
        options = self.driver.find_elements(*self.country_options)
        visible = [o for o in options if o.is_displayed() and o.location['y'] > start_y]
        visible[0].click()
        week_dropdown = self.driver.find_element(*self.select_week)
        week_dropdown.click()
        start_y = week_dropdown.location['y']
        options = self.driver.find_elements(*self.week_options)
        visible = [o for o in options if o.is_displayed() and o.location['y'] > start_y]
        visible[3].click()

    def previously_attended_and_desired_score(self,score):
        self.driver.find_element(*self.previous_exam).click()
        self.driver.find_element(*self.previous_score).send_keys(score)

    def click_on_continue_button(self):
        try:
            continue_button = wait_for_visibility(self.driver,self.continue_button)
        except(TimeoutException, NoSuchElementException):
            scroll_to_description(self.driver,self.continue_button)
            continue_button = wait_for_visibility(self.driver,self.continue_button)
        continue_button.click()