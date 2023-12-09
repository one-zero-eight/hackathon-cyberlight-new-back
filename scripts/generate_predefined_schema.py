import sys
from pathlib import Path

# add parent dir to sys.path
sys.path.append(str(Path(__file__).parents[1]))
from src.storages.predefined.storage import Predefined  # noqa: E402

Predefined.save_schema(Path(__file__).parents[1] / "predefined.schema.yaml")
