import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import WebDriverException


def handle_permissions(driver):
        permission_for_record = [
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button"),
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_one_time_button"),
        ]

        retry_count = 5
        while retry_count > 0:
            clicked_any = False
            for locator in permission_for_record:
                try:
                    elements = driver.find_elements(*locator)
                    if elements:
                        elements[0].click()
                        clicked_any = True
                        break
                except WebDriverException:
                    return  # session dead → safely exit
            if not clicked_any:
                # popup not visible yet → try again next loop
                retry_count -= 1
                time.sleep(1)
                continue
            retry_count -= 1