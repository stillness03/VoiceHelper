import subprocess
import time
import pyautogui
import os


def run_malwarebytes_cleanup():
    """Running a scan through Malwarebytes"""
    malwarebytes_path = r"-"
    subprocess.Popen(malwarebytes_path)
    time.sleep(4)

    pyautogui.hotkey('alt', 't')
    time.sleep(1)

    for _ in range(10):
        pyautogui.press('tab')
        time.sleep(0.3)

    pyautogui.press('enter')


def shutdown_pc():
    os.system("shutdown /s /t 0")
