import os
import subprocess


def push_test_image():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    pdf_path = os.path.join(base_dir, "test_data", "test_image.png")

    result = subprocess.run(f'adb push "{pdf_path}" /sdcard/DCIM/Camera/test_image.png',
        shell=True,
        capture_output=True,
        text=True
    )
    return result

def push_test_pdf():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    pdf_path = os.path.join(base_dir, "test_data", "test_document.pdf")
    file_name = os.path.basename(pdf_path)

    result = subprocess.run(
        f'adb push "{pdf_path}" /sdcard/Download/test_document.pdf',
        shell=True,           # Allows running the command as terminal string.
        capture_output=True,  # Lets you read success/error.
        text=True             # Returns output as string instead of bytes.
    )
    return result,file_name