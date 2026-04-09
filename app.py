from __future__ import annotations

import datetime as dt
import threading
import time
from pathlib import Path

import yaml
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, url_for

from detector import BattleDetector, DetectorConfig
from state import StateStore


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
store = StateStore()
worker_stop = threading.Event()
worker_thread: threading.Thread | None = None


def load_config(path: Path = Path("config.yaml")) -> DetectorConfig:
    if not path.exists():
        path = Path("config.example.yaml")
    with path.open("r", encoding="utf-8") as handle:
        cfg = yaml.safe_load(handle)
    return DetectorConfig(
        camera_index=cfg.get("camera_index", 0),
        poll_interval_ms=cfg.get("poll_interval_ms", 250),
        cooldown_seconds=cfg.get("cooldown_seconds", 3.0),
        ocr_enabled=cfg.get("ocr", {}).get("enabled", True),
        ocr_roi=tuple(cfg.get("ocr", {}).get("roi", [0.05, 0.72, 0.90, 0.25])),
        ocr_phrases=tuple(cfg.get("ocr", {}).get("phrases", ["wild", "appeared"])),
        ocr_min_confidence=cfg.get("ocr", {}).get("min_confidence", 0.55),
        template_enabled=cfg.get("template", {}).get("enabled", False),
        template_image_path=cfg.get("template", {}).get("image_path", ""),
        template_threshold=cfg.get("template", {}).get("threshold", 0.88),
        motion_roi=tuple(cfg.get("detection", {}).get("motion_roi", [0.0, 0.0, 1.0, 1.0])),
        min_motion_score=cfg.get("detection", {}).get("min_motion_score", 12.0),
    )


def detector_loop() -> None:
    config = load_config()
    detector = BattleDetector(config)
    detector.start()

    try:
        while not worker_stop.is_set():
            running = store.snapshot().running
            if running and detector.detect_new_battle():
                now = dt.datetime.now(dt.timezone.utc).isoformat()

                def _inc(st):
                    st.encounters += 1
                    st.last_event_at = now

                store.mutate(_inc)
            time.sleep(config.poll_interval_ms / 1000)
    finally:
        detector.stop()


@app.route("/")
def dashboard():
    return render_template("index.html", state=store.snapshot())


@app.route("/overlay")
def overlay():
    return render_template("overlay.html", state=store.snapshot())


@app.route("/api/state")
def api_state():
    return jsonify(store.snapshot().__dict__)


@app.route("/api/start", methods=["POST"])
def api_start():
    global worker_thread

    store.mutate(lambda st: setattr(st, "running", True))
    if worker_thread is None or not worker_thread.is_alive():
        worker_stop.clear()
        worker_thread = threading.Thread(target=detector_loop, daemon=True)
        worker_thread.start()
    return jsonify({"ok": True})


@app.route("/api/stop", methods=["POST"])
def api_stop():
    store.mutate(lambda st: setattr(st, "running", False))
    return jsonify({"ok": True})


@app.route("/api/reset", methods=["POST"])
def api_reset():
    def _reset(st):
        st.encounters = 0
        st.last_event_at = ""

    store.mutate(_reset)
    return jsonify({"ok": True})


@app.route("/api/increment", methods=["POST"])
def api_increment():
    now = dt.datetime.now(dt.timezone.utc).isoformat()

    def _inc(st):
        st.encounters += 1
        st.last_event_at = now

    store.mutate(_inc)
    return jsonify({"ok": True})


@app.route("/api/target", methods=["POST"])
def api_target():
    target_name = request.form.get("target_name", "").strip()

    def _set(st):
        st.target_name = target_name

    store.mutate(_set)
    return redirect(url_for("dashboard"))


@app.route("/api/upload_shiny", methods=["POST"])
def api_upload_shiny():
    file = request.files.get("shiny_image")
    if file is None or not file.filename:
        return redirect(url_for("dashboard"))

    ext = Path(file.filename).suffix.lower()
    fname = f"target{ext if ext in {'.png', '.jpg', '.jpeg', '.webp'} else '.png'}"
    target = UPLOAD_DIR / fname
    file.save(target)

    def _set(st):
        st.shiny_image_path = f"/uploads/{fname}"

    store.mutate(_set)
    return redirect(url_for("dashboard"))


@app.route("/uploads/<path:name>")
def uploaded(name: str):
    return send_from_directory(UPLOAD_DIR, name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
