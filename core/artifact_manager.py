import os
import shutil
import time
import allure


class ArtifactManager:

    @staticmethod
    def capture_all(driver, test_name, reports, node):
        screenshot_path = os.path.join(reports, "screenshots", f"{test_name}.png")
        source_path = os.path.join(reports, "source_path", f"{test_name}.xml")
        log_path = os.path.join(reports, "log_path", f"{test_name}.txt")

        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        os.makedirs(os.path.dirname(source_path), exist_ok=True)
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        # Screenshot
        try:
            png = driver.get_screenshot_as_png()
            allure.attach(png, "Screenshot", allure.attachment_type.PNG)
            with open(screenshot_path, "wb") as f:
                f.write(png)
        except Exception as e:
            print("Screenshot failed:", e)

        # Page Source
        try:
            source = driver.page_source
            with open(source_path, "w", encoding="utf-8") as f:
                f.write(source)
            allure.attach(source, "Page Source", allure.attachment_type.XML)
        except FileNotFoundError:
            pass

        # Logcat
        logcat = getattr(node, "logcat", None)
        if logcat:
            log_file = logcat.get("file")
            if log_file and os.path.exists(log_file):
                for _ in range(3):
                    try:
                        shutil.move(log_file, log_path)
                        break
                    except PermissionError:
                        time.sleep(2)
                with open(log_path, "r", encoding="utf-8") as f:
                    allure.attach(f.read(), "Logcat", allure.attachment_type.TEXT)