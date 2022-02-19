"""
This module is based on https://github.com/shenxn/rpi-bad-power maintained by https://github.com/shenxn
"""
import os

from . import config

HWMON_NAME = "rpi_volt"

SYSFILE_HWMON_DIR = f"{config.SYS_PATH}/class/hwmon"
SYSFILE_HWMON_FILE = "in0_lcrit_alarm"

def get_rpi_volt_hwmon():
    """Find rpi_volt hwmon device."""
    try:
        hwmons = os.listdir(SYSFILE_HWMON_DIR)
    except FileNotFoundError:
        return None

    for hwmon in hwmons:
        name_file = os.path.join(SYSFILE_HWMON_DIR, hwmon, "name")
        if os.path.isfile(name_file):
            with open(name_file, 'r', encoding='utf8') as file:
                hwmon_name = file.read().strip()
            if hwmon_name == HWMON_NAME:
                return os.path.join(SYSFILE_HWMON_DIR, hwmon)
    return None

def get_under_voltage_status() -> bool:
    """Get under voltage status."""
    hwmon = get_rpi_volt_hwmon()
    if not hwmon:
        return False

    with open(os.path.join(hwmon, SYSFILE_HWMON_FILE), 'r', encoding='utf8') as file:
        bit = file.read()[:-1]
    return bit == "1"
