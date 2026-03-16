import subprocess


def run_adb_command(command):
    # subprocess → Python module to run system command
    # run() → method that executes a command
    subprocess.run(command, shell=True)


def disable_wifi():
    run_adb_command("adb shell svc wifi disable")


def enable_wifi():
    run_adb_command("adb shell svc wifi enable")


def disable_data():
    run_adb_command("adb shell svc data disable")


def enable_data():
    run_adb_command("adb shell svc data enable")


def set_slow_network_gprs():
    run_adb_command("adb emu network delay gprs")


def set_slow_network_edge():
    run_adb_command("adb emu network delay edge")


def set_network_none():
    run_adb_command("adb emu network delay none")

# shell=True means
# Run the command through system shell (like CMD / Terminal)
# Why needed?
# Because command is a string exactly like terminal text
# Example:
# adb shell svc wifi disable
# adb devices
# dir / ls
# Without shell → Python expects list format
# With shell → string works directly