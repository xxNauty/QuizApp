import lorem
import pytest

from pathlib import Path
from logs import logs_initializer
from datetime import datetime


LOG_FILE = f"logs/{datetime.now().strftime("%d_%m_%Y")}_logs.log"

def test_for_already_existing_log_file(tmp_path, monkeypatch):
    filepath = tmp_path / LOG_FILE

    some_lorem_ipsum = lorem.paragraph()

    log_path = Path(filepath)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch()

    with open(filepath, 'w') as file:
        file.write(some_lorem_ipsum)
        file.close()

    logs_initializer.init_logs(str(filepath))

    with open(filepath, 'r') as file:
        assert file.read() == some_lorem_ipsum
