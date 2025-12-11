import logging
import os

from logs import logs_initializer
from pathlib import Path
from datetime import datetime

def test_for_log_file_not_exist(caplog):
    data_from_log_file = ""
    with open(f"logs/{datetime.now().strftime("%d_%m_%Y")}_logs.log", "r") as file:
        data_from_log_file = file.read()
        file.close()
    os.remove(f"logs/{datetime.now().strftime("%d_%m_%Y")}_logs.log")

    logs_path = Path("logs")
    log_files_before = [f.name for f in logs_path.iterdir() if f.is_file()]

    with(caplog.at_level(logging.INFO)):
        logs_initializer.init_logs()

    log_files_after = [f.name for f in logs_path.iterdir() if f.is_file()]

    assert len(log_files_after) - len(log_files_before) == 1
    assert f"{datetime.now().strftime("%d_%m_%Y")}_logs.log" not in log_files_before
    assert f"{datetime.now().strftime("%d_%m_%Y")}_logs.log" in log_files_after

    assert "Log file created" in caplog.messages

    with open(f"logs/{datetime.now().strftime("%d_%m_%Y")}_logs.log", "r+") as file:
        assert "" == file.read()
        file.write(data_from_log_file)
        file.close()

def test_for_log_file_already_existing(caplog):
    if not os.path.exists(f"logs/{datetime.now().strftime("%d_%m_%Y")}_logs.log"):
        open(f"logs/{datetime.now().strftime("%d_%m_%Y")}_logs.log").close()

    logs_path = Path("logs")
    log_files_before = [f.name for f in logs_path.iterdir() if f.is_file()]

    with(caplog.at_level(logging.INFO)):
        logs_initializer.init_logs()

    log_files_after = [f.name for f in logs_path.iterdir() if f.is_file()]

    assert len(log_files_before) == len(log_files_after)
    assert f"{datetime.now().strftime("%d_%m_%Y")}_logs.log" in log_files_before
    assert f"{datetime.now().strftime("%d_%m_%Y")}_logs.log" in log_files_after

    assert "Log file already exists" in caplog.messages
