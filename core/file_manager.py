import os


class FileManager:

    @staticmethod
    def clean_folders(temp_logs, reports, allure_results):
        folders = [temp_logs, allure_results]
        subfolders = ["log_path", "screenshots", "source_path"]

        for folder in folders:
            if os.path.exists(folder):
                for root, _, files in os.walk(folder):
                    for f in files:
                        if f in ("environment.properties", "categories.json", "executor.json"):
                            continue
                        path = os.path.join(root, f)
                        try:
                            os.remove(path)
                        except PermissionError:
                            print(f"Skipping locked file: {path}")
            os.makedirs(folder, exist_ok=True)

        if os.path.exists(reports):
            for root, _, files in os.walk(reports):
                for f in files:
                    path = os.path.join(root, f)
                    try:
                        os.remove(path)
                    except PermissionError:
                        print(f"Skipping locked file: {path}")
        else:
            os.makedirs(reports, exist_ok=True)

        for sub in subfolders:
            os.makedirs(os.path.join(reports, sub), exist_ok=True)