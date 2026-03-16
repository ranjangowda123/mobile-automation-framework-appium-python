from appium.webdriver.common.appiumby import AppiumBy
from utils.waits import wait_for_visibility


class ProfileDetailsPage:

    def __init__(self, driver):
        self.driver = driver

    first_name = (AppiumBy.XPATH, '//android.widget.TextView[@text="First name"]/following-sibling::android.widget.EditText[1]')
    last_name = (AppiumBy.XPATH, '//android.widget.TextView[@text="Last name"]/following-sibling::android.widget.EditText[1]')
    click_on_calender = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.widget.ImageView")')
    wait_for_calender_visible = (AppiumBy.ID, "android:id/date_picker_header_year")
    choose_date = (AppiumBy.ACCESSIBILITY_ID, "13 February 2026")
    confirm_date = (AppiumBy.ID, "android:id/button1")
    language = (AppiumBy.XPATH,'//android.widget.TextView[@text="Your native language"]/following-sibling::android.widget.EditText[1]')
    next_button = (AppiumBy.ACCESSIBILITY_ID, "Next")

    def enter_first_name(self,firstname):
        self.driver.find_element(*self.first_name).send_keys(firstname)

    def enter_last_name(self,lastname):
        self.driver.find_element(*self.last_name).send_keys(lastname)

    def click_on_calender_btn(self):
        self.driver.find_element(*self.click_on_calender).click()
        wait_for_visibility(self.driver,self.wait_for_calender_visible)

    def select_date(self):
        self.driver.find_element(*self.choose_date).click()
        self.driver.find_element(*self.confirm_date).click()

    def enter_language(self,language):
        wait_for_visibility(self.driver,self.language).send_keys(language)

    def click_on_next_button(self):
        wait_for_visibility(self.driver,self.next_button).click()