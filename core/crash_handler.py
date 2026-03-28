from utils.crash_detector import check_for_crash_or_anr
from utils.recover_app_from_background import handle_app_from_recovery


class CrashHandler:

    @staticmethod
    def check_and_recover(driver):
        check_for_crash_or_anr(driver)
        handle_app_from_recovery(driver)