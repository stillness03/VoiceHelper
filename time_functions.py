import datetime
import time
import threading
import pyttsx3
import re
import winsound

timer_thread = None


def get_current_time():
    """Returns the current time as a string and speaks it."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak_text(f"Now is {current_time}")
    return current_time


def get_current_date():
    """Returns the current date as a string and speaks it."""
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    speak_text(f"Now is {current_date}")
    return current_date


def parse_time_string(time_string):
    """Parses the time period and returns the number of seconds."""
    hours = 0
    minutes = 0
    seconds = 0

    match = re.search(r"(\d+)\s*hour", time_string)
    if match:
        hours = int(match.group(1))

    match = re.search(r"(\d+)\s*minute", time_string)
    if match:
        minutes = int(match.group(1))

    match = re.search(r"(\d+)\s*second", time_string)
    if match:
        seconds = int(match.group(1))

    return hours * 3600 + minutes * 60 + seconds


def start_timer_from_text(time_string):
    """Starts a timer based on a voice command."""
    seconds = parse_time_string(time_string)
    if seconds > 0:
        start_timer(seconds)
    else:
        print("Incorrect time for the timer")
        speak_text("Incorrect time for the timer")


def start_timer(seconds):
    """Starts a timer and announces when it finishes."""
    global timer_thread

    def timer_task():
        print(f"Timer started for {seconds} seconds...")
        time.sleep(seconds)
        print("Timer finished!")
        speak_text("Timer finished!")
        winsound.Beep(1000, 1000)

    timer_thread = threading.Thread(target=timer_task, daemon=True)
    timer_thread.start()


def stop_timer():
    """Stops the timer if it is running."""
    global timer_thread
    if timer_thread and timer_thread.is_alive():
        timer_thread = None
        print("Timer stopped")
        speak_text("Timer stopped")
    else:
        print("No active timer")
        speak_text("No active timer")


def speak_text(text):
    """Speaks the given text."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
