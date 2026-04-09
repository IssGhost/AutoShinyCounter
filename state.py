from __future__ import annotations

import json
import threading
from dataclasses import dataclass, asdict
from pathlib import Path


STATE_PATH = Path("tracker_state.json")


@dataclass
class TrackerState:
    encounters: int = 0
    target_name: str = ""
    shiny_image_path: str = ""
    running: bool = False
    last_event_at: str = ""


class StateStore:
    def __init__(self, path: Path = STATE_PATH) -> None:
        self.path = path
        self.lock = threading.Lock()
        self.state = self._load()

    def _load(self) -> TrackerState:
        if not self.path.exists():
            return TrackerState()
        with self.path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
        return TrackerState(**raw)

    def save(self) -> None:
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(asdict(self.state), handle, indent=2)

    def mutate(self, mutator) -> TrackerState:
        with self.lock:
            mutator(self.state)
            self.save()
            return self.state

    def snapshot(self) -> TrackerState:
        with self.lock:
            return TrackerState(**asdict(self.state))
