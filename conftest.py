""""
Driver initialization and session management.
"""
import os
import shutil
import subprocess
import time
import allure


import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.app_config import PlatformName, DeviceName, AutomationName, AppPackage, AppActivity, SessionTimeout
from utils.app_lifecycle import handel_launch_stability
from utils.crash_detector import check_for_crash_or_anr
from utils.permission_handler import handle_permissions
from utils.recover_app_from_background import handel_app_from_recovery


base_dir = os.path.dirname(__file__)
temp_logs = os.path.join(base_dir,"temp_logs")
reports = os.path.join(base_dir,"reports")
allure_results = os.path.join(base_dir, "allure-results")




@pytest.fixture(scope="session", autouse=True)
def create_environment_file(clean_report_folders):
    from config.app_config import DeviceName, PlatformName, AppPackage , AutomationName

    with open(os.path.join(allure_results,"environment.properties"), "w") as f:
        f.write(f"Device={DeviceName}\n")
        f.write(f"Platform={PlatformName}\n")
        f.write(f"AppPackage={AppPackage}\n")
        f.write(f"AutomationName={AutomationName}\n")

"""
Prepare clean report and log directories at the start of the test session for a fresh execution.
"""
@pytest.fixture(scope="session",autouse=True)
def clean_report_folders():
    folders = [temp_logs, allure_results]
    subfolders = ["log_path","screenshots","source_path"]
    for folder in folders:
        if os.path.exists(folder):
            for root, _, files in os.walk(folder):
                for f in files:
                    if f in ("environment.properties","categories.json"):
                        continue
                    os.remove(os.path.join(root, f))   # delete the file at that path
        os.makedirs(folder,exist_ok=True)
    if os.path.exists(reports):
        for root, _, files in os.walk(reports):
            for f in files:
                os.remove(os.path.join(root, f))
    else:
        os.makedirs(reports, exist_ok=True)
    for sub in subfolders:
        os.makedirs(os.path.join(reports, sub), exist_ok=True)

"""
Capture and attach test phase results (setup, call, teardown) to the test item for later failure handling and reporting.
:
👉 It creates a report object that tells whether setup succeeded or failed
👉 Then it saves that report on the test item as: item.rep_setup

"""
@pytest.hookimpl(hookwrapper=True)
# item is used to store results of the current test, including all 3 phases:
# item.rep_setup → setup result
# item.rep_call → test body result
# item.rep_teardown → teardown result

def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    # setattr lets you create attribute dynamically
    setattr(item, "rep_" + rep.when, rep)


"""
Initialize the Appium driver, manage the test session lifecycle, and start per-test log capture for debugging and recovery.
"""
@pytest.fixture(scope="function")
def driver(request):
    options = UiAutomator2Options()
    options.platform_name = PlatformName
    options.device_name = DeviceName
    options.automation_name = AutomationName
    options.app_package = AppPackage
    options.app_activity = AppActivity
    options.full_reset = False
    options.no_reset = False    # if False App data will be cleared
    options.new_command_timeout = SessionTimeout
    options.auto_grant_permissions = True


    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    allure.attach(str(driver.capabilities),name="Device Capabilities",attachment_type=allure.attachment_type.TEXT)

    log_file = os.path.join(temp_logs,f"{request.node.name}.txt")
    logcat_process = subprocess.Popen(
        ["adb", "logcat", "-v", "threadtime"],
        stdout=open(log_file, "w"),
        stderr=subprocess.STDOUT)

    # share with crash_guard
    request.node.logcat_process = logcat_process
    request.node.log_file = log_file

    handle_permissions(driver)
    handel_launch_stability(driver)

    yield driver
    if driver:
        logcat_process.terminate()
        driver.quit()

"""
Monitor each test for crashes/ANR, perform app recovery, and capture failure artifacts (logs, screenshots, page source) when needed
"""
@pytest.fixture(scope="function", autouse=True)
def crash_guard(driver, request):

    test_name = request.node.name
    log_path = os.path.join(reports, "log_path", f"{test_name}_logcat.txt")
    screenshot_path = os.path.join(reports, "screenshots", f"{test_name}_crash.png")
    source_path = os.path.join(reports, "source_path", f"{test_name}_page_source.xml")

    yield

    process = request.node.logcat_process
    log_file = request.node.log_file

    # any phase failure as failure.
    failed = (
            request.node.rep_setup.failed
            or request.node.rep_call.failed
            or request.node.rep_teardown.failed
    )
    # 👉 crash / ANR check
    try:
        check_for_crash_or_anr(driver)
        handel_app_from_recovery(driver)
    except AssertionError:
        failed = True   # treat crash as failure

    # 👉 final decision
    if failed:
        png = driver.get_screenshot_as_png()
        with open(screenshot_path, "wb") as f:
            f.write(png)
        allure.attach(png, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
        print("Screenshot saved")

        page_source = driver.page_source
        with open(source_path, "w", encoding="utf-8") as f:
            f.write(page_source)
        allure.attach(page_source, name="Page Source", attachment_type=allure.attachment_type.XML)

        process.terminate()
        shutil.move(log_file, log_path)
        with open(log_path, "r", encoding="utf-8") as f:
            allure.attach(f.read(),name="Logcat",attachment_type=allure.attachment_type.TEXT)

    else:
        if os.path.exists(log_file):
            process.terminate()
            time.sleep(1)
            os.remove(log_file)