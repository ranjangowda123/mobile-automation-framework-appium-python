from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from utils.crash_detector import check_for_crash_or_anr
from utils.permission_handler import handle_permissions
from utils.recover_app_from_background import handle_app_from_recovery
import time

def safe_click(driver,locator):
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located(locator)).click()
    time.sleep(1.5)  # allow picker animation
    current_pkg = driver.current_package
    print("Current package:", current_pkg)
    SYSTEM_ALLOWED = ["documentsui","camera","photos","chrome"]
    if any(app in current_pkg.lower() for app in SYSTEM_ALLOWED):
        print("System picker detected — skipping health checks")
        return
    handle_permissions(driver)
    check_for_crash_or_anr(driver)
    handle_app_from_recovery(driver)

def safe_gesture_click(driver, element):
    driver.execute_script("mobile: clickGesture", {"elementId": element.id})
    # handle_permissions(driver)
    # check_for_crash_or_anr(driver)
    # handle_app_from_recovery(driver)