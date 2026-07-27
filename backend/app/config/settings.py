from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

BUILDING_FILE = BASE_DIR / "building.json"

MQTT_BROKER = "localhost"

UPDATE_INTERVAL = 1