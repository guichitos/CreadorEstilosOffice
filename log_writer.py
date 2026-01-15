import datetime
import os

LOG_FILE = "log.txt"

ICON_MAP = {
    "INFO": "",
    "WARNING": "⚠️",
    "ERROR": "❌"
}

def log_event(message: str, level: str = "INFO"):
    """Writes a log entry with a timestamp in the log file and prints a version with icons to the console."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{now}] [{level}] {message}"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")
    
    icon = ICON_MAP.get(level, "")
    print(f"{icon} {message}")

def log_info(message: str):
    log_event(message, "INFO")

def log_warning(message: str):
    log_event(message, "WARNING")

def log_error(message: str):
    log_event(message, "ERROR")

def log_separator():
    """Adds 3 empty lines to the log and console output to visually separate execution blocks."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n\n\n")
    print("\n\n")
