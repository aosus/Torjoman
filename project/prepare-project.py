from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

local_json_file: Path = (BASE_DIR / "local_dictionary.json").resolve()

local_json_file.touch()
local_json_file.write_text("{}")
