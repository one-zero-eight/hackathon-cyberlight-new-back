import sys
from pathlib import Path

# add parent dir to sys.path
sys.path.append(str(Path(__file__).parents[1]))
from src.storages.predefined.storage import PredefinedLessons  # noqa: E402

PredefinedLessons.save_schema(Path(__file__).parents[1] / "predefined.schema.yaml")
