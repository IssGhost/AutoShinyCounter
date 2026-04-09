# Auto Shiny Counter (Switch 2 + OBS)

This project gives you a full, local shiny hunting counter:

- Detects **new battle starts** from your capture-card feed using OCR and/or template matching.
- Increments a persistent encounter counter automatically.
- Provides an OBS-ready browser overlay at `/overlay`.
- Lets you set your current hunt name and upload the shiny sprite/photo you're targeting.

## 1) Prerequisites

- Python 3.11+
- A capture device that appears as a webcam/camera source on your PC
- Tesseract OCR installed on your machine
  - macOS: `brew install tesseract`
  - Ubuntu/Debian: `sudo apt install tesseract-ocr`
  - Windows: install from UB Mannheim builds and ensure `tesseract` is in PATH

## 2) Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp config.example.yaml config.yaml
```

## 3) Configure detection

Edit `config.yaml`:

- `camera_index`: your capture card index (`0`, `1`, etc.)
- OCR mode:
  - `ocr.enabled: true`
  - `ocr.roi`: portion of frame where battle text appears
  - `ocr.phrases`: fragments expected during battle intro (`wild`, `appeared`)
- Template mode:
  - `template.enabled: true` and set `template.image_path`
  - Use a cropped image of a consistent battle-start HUD element
- Anti-duplicate settings:
  - `cooldown_seconds`
  - `detection.min_motion_score`

Tip: use either OCR or template first, then layer both for better precision.

## 4) Run

```bash
python app.py
```

Open:

- Dashboard: <http://localhost:5000>
- OBS overlay: <http://localhost:5000/overlay>

## 5) Add to OBS

1. In OBS, add **Browser Source**.
2. URL: `http://<your-pc-ip>:5000/overlay` (or localhost if OBS runs on same PC).
3. Set width/height for your layout.
4. Enable "Shutdown source when not visible" only if you want refresh behavior when scenes switch.

## 6) Daily workflow

1. Launch game and route Switch 2 video through your capture card.
2. Open dashboard.
3. Set target name and upload your shiny target image.
4. Click **Start**.
5. Enter encounters; each detected new battle increments automatically.
6. Use **+1 Manual** if a detection was missed.

## 7) Notes

- Detection quality depends heavily on ROI and thresholds.
- If OCR misses text, tighten ROI and reduce `ocr_min_confidence` slightly.
- If false positives occur, increase `cooldown_seconds` and `min_motion_score`.

## 8) Files

- `app.py`: web app + background detection worker
- `detector.py`: OCR/template/motion battle detection
- `state.py`: persistent tracker state
- `templates/overlay.html`: OBS-facing widget
