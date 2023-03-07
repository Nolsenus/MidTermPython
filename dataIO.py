from pathlib import Path
import json
import os
from datetime import datetime


def load_from_json(filename: str):
    path = Path(filename)
    if path.is_file():
        with open(filename, 'r', encoding='utf-8') as file:
            if os.stat(filename).st_size > 0:
                data = json.load(file)
                for note in data:
                    note['date'] = datetime.fromisoformat(note['date'])
                return data
            return f'Файл {filename} пуст.'
    else:
        return f'Файл {filename} не найден.'


def save_to_json(filename: str, data):
    path = Path(filename)
    if not path.is_file():
        open(filename, 'x')
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False, default=str))
