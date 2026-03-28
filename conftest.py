""""
Driver initialization and session management.
"""
import os
import time

import allure
import pytest

from datetime import datetime
from core.artifact_manager import ArtifactManager
from core.crash_handler import CrashHandler
from core.driver_factory import DriverFactory
from core.env_writer import EnvWriter
from core.file_manager import FileManager
from core.log_manager import LogManager
from utils.permission_handler import handle_permissions
from utils.app_lifecycle import handle_launch_stability


base_dir = os.path.dirname(__file__)
temp_logs = os.path.join(base_dir,"temp_logs")
reports = os.path.join(base_dir,"reports")
allure_results = os.path.join(base_dir, "allure-results")

@pytest.fixture(scope="session", autouse=True)
def create_environment_file(clean_report_folders):
    EnvWriter.write_allure_env(allure_results)


"""
Prepare clean report and log directories at the start of the test session for a fresh execution.
"""
@pytest.fixture(scope="session",autouse=True)
def clean_report_folders():
    FileManager.clean_folders(temp_logs, reports, allure_results)


@pytest.fixture(autouse=True)
def add_device_label(request):
    device = request.config.getoption("--platform")
    allure.dynamic.label("device", device)


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

def pytest_runtest_setup(item):
    item.start_time = time.time()

def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        end_time = time.time()
        start = getattr(item, "start_time", None)

        if start:
            start_12 = datetime.fromtimestamp(start).strftime("%I:%M:%S %p")
            end_12 = datetime.fromtimestamp(end_time).strftime("%I:%M:%S %p")

            duration = int(end_time - start)
            mins, secs = divmod(duration, 60)

            time_text = f"{start_12} - {end_12} ({mins}m {secs}s)"

            allure.attach(time_text, "Execution Time", allure.attachment_type.TEXT)
    # setattr lets you create attribute dynamically
    setattr(item, "rep_" + rep.when, rep)


def pytest_addoption(parser):
    parser.addoption("--platform", action="store", default="android")
    parser.addoption("--appium_url", action="store", default="http://127.0.0.1:4723")


"""
Initialize the Appium driver, manage the test session lifecycle, and start per-test log capture for debugging and recovery.
"""
@pytest.fixture(scope="function")
def driver(request):
    device = request.config.getoption("--platform")
    appium_url = request.config.getoption("--appium_url")
    driver = DriverFactory.create_driver(device, appium_url)

    allure.attach(str(driver.capabilities),name="Device Capabilities",attachment_type=allure.attachment_type.TEXT)

    logcat = LogManager.start_logcat(request.node.name, temp_logs)
    request.node.logcat = logcat

    handle_permissions(driver)
    handle_launch_stability(driver)

    yield driver
    # 👉 check failure AFTER test, BEFORE quit
    failed = (
            getattr(request.node, "rep_setup", None) and request.node.rep_setup.failed
            or getattr(request.node, "rep_call", None) and request.node.rep_call.failed
            or getattr(request.node, "rep_teardown", None) and request.node.rep_teardown.failed
    )
    # ✅ FIRST stop logcat
    try:
        LogManager.stop_logcat(logcat)
        time.sleep(2)  # 🔥 important (Windows release time)
    except (PermissionError, OSError):
        pass

    # ✅ THEN capture
    if failed and driver:
        ArtifactManager.capture_all(driver, request.node.name, reports, request.node)

    if driver:
        try:
            driver.quit()
        except (OSError, RuntimeError):
            pass

"""
Monitor each test for crashes/ANR, perform app recovery, and capture failure artifacts (logs, screenshots, page source) when needed
"""
@pytest.fixture(scope="function", autouse=True)
def crash_guard(driver, request):

    yield
    # 👉 Crash handling
    try:
        CrashHandler.check_and_recover(driver)
    except AssertionError:
        pass