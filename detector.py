from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import pytesseract


@dataclass
class DetectorConfig:
    camera_index: int = 0
    poll_interval_ms: int = 250
    cooldown_seconds: float = 3.0
    ocr_enabled: bool = True
    tesseract_cmd: str = ""
    ocr_roi: tuple[float, float, float, float] = (0.05, 0.72, 0.90, 0.25)
    ocr_phrases: tuple[str, ...] = ("wild", "appeared")
    ocr_min_confidence: float = 0.55
    template_enabled: bool = False
    template_image_path: str = ""
    template_threshold: float = 0.88
    motion_roi: tuple[float, float, float, float] = (0.0, 0.0, 1.0, 1.0)
    min_motion_score: float = 12.0


class BattleDetector:
    def __init__(self, config: DetectorConfig) -> None:
        self.config = config
        self.cap: Optional[cv2.VideoCapture] = None
        self.template: Optional[np.ndarray] = None
        self.prev_motion_frame: Optional[np.ndarray] = None
        self.last_detection_time = 0.0
        self.active_battle = False
        self.warned_missing_tesseract = False
        self.warned_bad_template_size = False

        if config.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = config.tesseract_cmd
        elif os.name == "nt":
            common = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
            if common.exists():
                pytesseract.pytesseract.tesseract_cmd = str(common)

        if config.template_enabled and config.template_image_path:
            path = Path(config.template_image_path)
            if path.exists():
                self.template = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)

    def start(self) -> None:
        self.cap = cv2.VideoCapture(self.config.camera_index)
        if not self.cap.isOpened():
            raise RuntimeError(
                f"Could not open camera/capture device at index {self.config.camera_index}"
            )

    def stop(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def _crop_roi(self, frame: np.ndarray, roi: tuple[float, float, float, float]) -> np.ndarray:
        h, w = frame.shape[:2]
        x, y, rw, rh = roi
        x1, y1 = int(w * x), int(h * y)
        x2, y2 = int(w * (x + rw)), int(h * (y + rh))
        return frame[max(0, y1):min(h, y2), max(0, x1):min(w, x2)]

    def _motion_score(self, gray: np.ndarray) -> float:
        roi_gray = self._crop_roi(gray, self.config.motion_roi)
        if self.prev_motion_frame is None:
            self.prev_motion_frame = roi_gray
            return 0.0
        diff = cv2.absdiff(self.prev_motion_frame, roi_gray)
        self.prev_motion_frame = roi_gray
        return float(np.mean(diff))

    def _ocr_hit(self, frame: np.ndarray) -> bool:
        if not self.config.ocr_enabled:
            return False
        roi = self._crop_roi(frame, self.config.ocr_roi)
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        try:
            text = pytesseract.image_to_string(gray).lower()
        except pytesseract.TesseractNotFoundError:
            if not self.warned_missing_tesseract:
                print(
                    "WARNING: Tesseract was not found. Set config `ocr.tesseract_cmd` to your "
                    "tesseract.exe path (for example: C:\\Program Files\\Tesseract-OCR\\tesseract.exe)."
                )
                self.warned_missing_tesseract = True
            return False
        hits = sum(1 for phrase in self.config.ocr_phrases if phrase.lower() in text)
        confidence = hits / max(len(self.config.ocr_phrases), 1)
        return confidence >= self.config.ocr_min_confidence

    def _template_hit(self, frame: np.ndarray) -> bool:
        if not (self.config.template_enabled and self.template is not None):
            return False
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        th, tw = self.template.shape[:2]
        fh, fw = gray.shape[:2]
        if th > fh or tw > fw:
            if not self.warned_bad_template_size:
                print(
                    "WARNING: Template image is larger than the camera frame. "
                    "Use a smaller crop for `template.image_path`."
                )
                self.warned_bad_template_size = True
            return False
        try:
            result = cv2.matchTemplate(gray, self.template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            return max_val >= self.config.template_threshold
        except cv2.error:
            return False

    def detect_new_battle(self) -> bool:
        if self.cap is None:
            raise RuntimeError("BattleDetector.start() must be called before detect_new_battle()")

        ok, frame = self.cap.read()
        if not ok:
            return False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        motion = self._motion_score(gray)
        signal = self._ocr_hit(frame) or self._template_hit(frame)

        now = time.time()
        cooldown_ok = now - self.last_detection_time >= self.config.cooldown_seconds

        if signal and motion >= self.config.min_motion_score and cooldown_ok and not self.active_battle:
            self.last_detection_time = now
            self.active_battle = True
            return True

        if not signal:
            self.active_battle = False

        return False