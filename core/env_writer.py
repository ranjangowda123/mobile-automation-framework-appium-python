import os

"""
adds environment info to Allure report
"""
class EnvWriter:

    @staticmethod
    def write_allure_env(allure_results):
        from config.app_config import DeviceName, PlatformName, AppPackage, AutomationName

        file_path = os.path.join(allure_results, "environment.properties")

        with open(file_path, "w") as f:
            f.write(f"Device={DeviceName}\n")
            f.write(f"Platform={PlatformName}\n")
            f.write(f"AppPackage={AppPackage}\n")
            f.write(f"AutomationName={AutomationName}\n")
