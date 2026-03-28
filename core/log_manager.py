import os
import signal
import subprocess
import time


class LogManager:

    @staticmethod
    def start_logcat(test_name, temp_logs):
        log_file = os.path.join(temp_logs, f"{test_name}.txt")
        file_handle = open(log_file, "w")
        try:
            process = subprocess.Popen(
                ["adb", "logcat", "-v", "threadtime"],
                stdout=file_handle,
                stderr=subprocess.STDOUT,
                creationflags = subprocess.CREATE_NEW_PROCESS_GROUP  # 🔥 important (Windows)
            )
            return {"process": process, "file": log_file,"file_handle":file_handle}
        except FileNotFoundError :
            return None

    @staticmethod
    def stop_logcat(logcat):
        if not logcat:
            return

        process = logcat.get("process")
        file_handle = logcat.get("file_handle")

        try:
            if process:
                process.send_signal(signal.CTRL_BREAK_EVENT)  # 🔥 kills full group
                try:
                    process.wait(timeout=5)
                except TimeoutError:
                    process.kill()
                    process.wait()
            if file_handle:
                file_handle.close()
            time.sleep(2)
        except FileNotFoundError:
            pass