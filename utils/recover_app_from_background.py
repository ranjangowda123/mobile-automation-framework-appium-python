from config.app_config import AppPackage


def handle_app_from_recovery(driver):
    app_state = driver.query_app_state(AppPackage)
    if app_state != 4:
        driver.activate_app(AppPackage)
    else:
        print("App is in Foreground State")