from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utils.scroll_utils import scroll_to_text
from utils.waits import wait_for_visibility, wait_for_clickable


class AccountCreationPage:

    def __init__(self,driver):
        self.driver = driver

    ggle_btn_and_acct = (AppiumBy.XPATH,'(//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup)[6]')
    wait_for_title1 = (AppiumBy.ID, "com.google.android.gms:id/main_title")
    wait_for_title2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create your account")')



    def click_on_google_button(self):
        try:
            google_button1 = wait_for_visibility(self.driver,self.ggle_btn_and_acct)
        except (TimeoutException, NoSuchElementException):
            scroll_to_text(self.driver,"By clicking continue I agree to the")
            google_button1 = wait_for_visibility(self.driver,self.ggle_btn_and_acct)
        google_button1.click()

    def wait_for_choose_account_popup(self):
        wait_for_visibility(self.driver,self.wait_for_title1)

    def choose_email_for_registration(self,email):
        email_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{email}")')
        self.driver.find_element(*email_locator).click()

    def wait_for_account_creation_page(self):
        WebDriverWait(self.driver, 20).until(
            expected_conditions.visibility_of_element_located(self.wait_for_title2))