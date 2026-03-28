import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.app_config import PlatformName,DeviceName,AutomationName,AppPackage,AppActivity,SessionTimeout


class DriverFactory:

    @staticmethod
    def create_driver(platform, appium_url, retries=3):
        for attempt in range(retries):
            try:
                if platform.lower() == "android":
                    options = UiAutomator2Options()
                    options.platform_name = PlatformName
                    options.device_name = DeviceName
                    options.automation_name = AutomationName
                    options.app_package = AppPackage
                    options.app_activity = AppActivity
                    options.no_reset = False   # 👉 App will reset data
                    options.full_reset = False # 👉 App will NOT uninstall
                    options.new_command_timeout = SessionTimeout
                    options.auto_grant_permissions = True

                    driver = webdriver.Remote(appium_url, options=options)
                    return driver

                else:
                    raise Exception("Unsupported platform")
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(2)
        raise RuntimeError("Driver creation failed")