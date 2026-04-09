
Create auto shiny tracker with counter
Apr 9
·
AutoShinyCounter
·
…ex/create-auto-shiny-tracker-with-counter-f05txo
·
+583
-0

Archive

Share
View PR


Create me a start to finish auto shiny tracker this should include the current counter that when i go into battle on my switch 2 it checks the screen verifies the new battle starts via either text recognition or the actual image of the pokemon, ticks the counter up one and i can add this as a source to obs to keep track of pokemon encounters. also allow me to add the image of the shiny pokemon im currently hunting for
Copy
Summary
Built a complete Flask app that runs an auto shiny encounter tracker end-to-end: it loads config, starts a background detector thread, increments encounters on new-battle events, exposes API routes (start/stop/reset/increment/state), supports target naming, and handles shiny image uploads for display in the UI and overlay.

Implemented battle detection logic using capture-card input (camera_index) with OCR phrase matching, optional template image matching, motion scoring, cooldown gating, and active-battle state to reduce duplicate counts from the same encounter intro screen.

Added persistent tracker state with thread-safe read/mutate operations so encounters/target/running state survive restarts via tracker_state.json.

Added a full dashboard page for control + monitoring (start/stop/reset/manual +1), target name entry, shiny image upload, and live polling updates from /api/state.

Added a transparent OBS-ready /overlay page showing current hunt name, encounter count, and optional shiny image, with live refresh every second for stream use.

Added setup/configuration documentation and dependencies so you can go from install to OBS integration quickly, including OCR/template tuning guidance and workflow steps for Switch 2 hunting sessions.

Testing

✅ python -m compileall app.py detector.py state.py

⚠️ Screenshot step: browser screenshot tooling was not available in this environment, so I could not capture and attach a UI screenshot artifact.

Committed on current branch:

16772bd — Build end-to-end auto shiny tracker with OBS overlay

PR metadata was recorded via the make_pr tool with matching title/body after commit.


Files (8)
ok so now i downloadthe zip and it will run how do i use this application i need to add this as a scene to display but also capture the virtual camera that im displaying from the capture card to obs
Copy
Perfect question — here’s the exact start-to-finish flow for your setup (capture card + OBS + this tracker overlay).

1) Run the app first
From the folder you unzipped:

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp config.example.yaml config.yaml
python app.py
Those install/run steps and URLs are documented in the project README.

When it starts, open:

Dashboard: http://localhost:5000

Overlay URL for OBS: http://localhost:5000/overlay

2) Important: capture card + OBS + tracker camera source
You want both OBS and the tracker to “see” the game feed. Usually one app can lock the capture device, so do this:

In OBS, add your capture card as Video Capture Device.

In OBS, click Start Virtual Camera.

In config.yaml, set camera_index to the OBS Virtual Camera device index (instead of raw capture card index), so the tracker reads the same feed OBS is already using.

Restart python app.py after changing config.

The tracker reads camera input by index via OpenCV (cv2.VideoCapture(camera_index)).

3) Configure battle detection
In config.yaml:

Turn OCR on (ocr.enabled: true) and tune text ROI (ocr.roi) + phrases (wild, appeared).

Optionally enable template mode and set a cropped battle-start image path (template.image_path).

Tune anti-duplicate sensitivity using cooldown_seconds and detection.min_motion_score.

The app uses OCR and/or template matching with cooldown/motion gating before counting a new encounter.

4) Use the dashboard during hunts
On http://localhost:5000:

Set target name

Upload shiny image

Click Start to enable auto counting

Use +1 Manual when needed

These actions call API routes like /api/start, /api/increment, /api/upload_shiny.

5) Add overlay to OBS scene
In OBS scene:

Add Browser Source

URL = http://localhost:5000/overlay

Set size/position where you want counter shown

Overlay pulls live state every second and shows:

encounter count

hunt name

shiny image (if uploaded)

6) Quick troubleshooting
Counter not moving: lower OCR threshold a bit, tighten OCR ROI, or enable template detection.

Double counts: increase cooldown_seconds / min_motion_score.

Camera open error: tracker and OBS are probably fighting over device; use OBS Virtual Camera path as described.

If you want, I can next give you a recommended config.yaml preset specifically for Pokémon battle intros (safe starter values for OCR ROI, cooldown, and motion).

make sure to push this to the git so i can insteall thefiles
Copy
Got it — I checked the repo state and there are no uncommitted changes, and there is currently no Git remote configured, so I can’t push from this environment yet.

What I verified
Command run:
✅ git status --short && git remote -v
Result: clean working tree, and no remotes listed.

Why push didn’t happen
Without a configured remote (like origin), git push has nowhere to send commits.

What you should run on your machine (once)
From your project folder:

git remote add origin <YOUR_GITHUB_REPO_URL>
git branch -M main
git push -u origin main
If your branch is not main, replace it with your current branch name.

Current project install/run files are already present in repo
The install and run steps are documented in README.md (venv, pip install, cp config, python app.py) and OBS overlay URL setup is there too.

If you want, I can make a follow-up commit that adds a one-command installer script (install.sh + Windows .bat) so setup is even easier before you push.

give me step by step in detail how to get this to launch properly
Copy
Absolutely — here is a detailed, click-by-click setup so you can get it launching reliably.

0) What this app does (so setup makes sense)
Runs a local web app at port 5000.

Watches a video input (camera_index) for battle starts.

Increments encounters automatically.

Gives you an OBS browser overlay at /overlay.

Lets you set target name + upload shiny image from the dashboard.

1) Prerequisites you must install first
Python 3.11+

Tesseract OCR (required for OCR mode):

macOS: brew install tesseract

Ubuntu/Debian: sudo apt install tesseract-ocr

Windows: install Tesseract and make sure it is in PATH.

Your Switch capture card connected and visible on PC as a camera input device.

2) Put files in a folder and open terminal there
Example folder:

AutoShinyCounter/

app.py

requirements.txt

config.example.yaml

templates/...

3) Create Python environment and install dependencies
macOS/Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config.example.yaml config.yaml
Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy config.example.yaml config.yaml
These are the project’s documented install steps.

4) Configure config.yaml before first launch
Open config.yaml and set:

camera_index: camera input number.

OCR settings (ocr.enabled, ocr.roi, ocr.phrases, ocr.min_confidence).

Optional template settings (template.enabled, template.image_path, template.threshold).

Anti-duplicate settings (cooldown_seconds, detection.min_motion_score).

Practical starter config
Leave OCR enabled.

Start with:

cooldown_seconds: 3.0

min_motion_score: 12.0

Keep template.enabled: false until OCR is working, then enable template mode for better accuracy.

5) Launch the app
python app.py
Then open in browser:

Dashboard: http://localhost:5000

Overlay: http://localhost:5000/overlay

6) Connect this correctly with OBS (important)
You need both:

Game video in OBS

Counter overlay in OBS

A) Add game feed to OBS
Add Video Capture Device source in OBS for your capture card.

B) Add counter overlay to OBS
Add Browser Source in OBS

URL: http://localhost:5000/overlay

Set size/position in your scene.

7) If camera conflicts happen (OBS + app both using card)
If app can’t access capture card while OBS is using it:

In OBS, click Start Virtual Camera.

Set camera_index in config.yaml to OBS virtual camera device index.

Restart app.

This avoids two apps competing for the same physical capture device.
(Your detector opens one camera index directly via OpenCV.)

8) Start hunting workflow (every session)
Open dashboard (/).

Enter target name.

Upload shiny image.

Click Start.

Begin encounters on Switch.

Use +1 Manual if a miss happens.

9) Quick tuning if detection is bad
Too many false counts:

Raise cooldown_seconds

Raise min_motion_score

Not counting enough:

Lower ocr.min_confidence

Tighten ocr.roi to only battle text area

Optionally enable template mode with a clean cropped battle UI image.

10) Common “won’t launch” checklist
Did you activate .venv before running?

Did pip install -r requirements.txt complete?

Did you create config.yaml from example?

Is Tesseract installed and in PATH?

Is port 5000 already used by another app?

Commands I used to verify project docs/config right now
nl -ba README.md | sed -n '1,200p'

nl -ba config.example.yaml | sed -n '1,200p'

If you want, next I can give you a pre-tuned config.yaml for Pokémon Scarlet/Violet battle intro text placement (with recommended ROI values to test first).

once i download tesseract from git how do i addd it to path do i add the whole file outside the zip? im on a windows pc
Copy
Yep — on Windows, you do not add the .zip itself to PATH.
You add the folder that contains tesseract.exe to PATH. (Your README already notes Tesseract must be in PATH on Windows.)

Step-by-step (Windows)
Extract the Tesseract zip to a permanent folder, for example:
C:\Program Files\Tesseract-OCR\

Confirm this file exists:
C:\Program Files\Tesseract-OCR\tesseract.exe

Open Start → search “Edit the system environment variables”.

Click Environment Variables.

Under User variables (or System), select Path → Edit.

Click New and add:
C:\Program Files\Tesseract-OCR\

Click OK on all dialogs.

Close and reopen PowerShell/CMD.

Verify it worked
Run:

tesseract --version
If it prints a version, PATH is correct.

If tesseract --version still fails
Make sure you added the folder with tesseract.exe (not the zip, not parent folder).

Reboot terminal (or reboot Windows).

Check for typos/spaces in path entry.

Then run your app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy config.example.yaml config.yaml
python app.py
(These are the project’s install/run steps.)

If you want, I can give you a quick screenshot-style checklist for exactly where to click in Windows 11 Environment Variables UI.

give me the download for tesseract or the git repo
Copy
Yep — here are the correct links:

✅ Tesseract download (Windows installer)
UB Mannheim Windows builds (recommended):
https://github.com/UB-Mannheim/tesseract/wiki

✅ Official Tesseract GitHub repo
Main source repo:
https://github.com/tesseract-ocr/tesseract

✅ Official install docs (mentions Windows installer source)
https://tesseract-ocr.github.io/tessdoc/Installation.html

If you’re on Windows, use the UB Mannheim installer (easy path). The main tesseract-ocr/tesseract repo is mostly source code (not the simplest installer route).
(Your project README also says Windows should install Tesseract and ensure it’s in PATH.)

how do i know what index the camera is
Copy
Great question — camera_index is just the number OpenCV uses for available video devices (0, 1, 2, ...).
Your project uses that in config.yaml as camera_index.

Easiest way to find it (Windows)
Run this in the same venv where you installed requirements:

python - << 'PY'
import cv2

print("Scanning camera indexes 0-9...")
for i in range(10):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # CAP_DSHOW helps on Windows
    ok, frame = cap.read()
    opened = cap.isOpened()
    cap.release()
    if opened and ok and frame is not None:
        print(f"Index {i}: OK")
    else:
        print(f"Index {i}: no signal")
PY
Any index that says OK is a valid source.
Then set that number in config.yaml:

camera_index: <that_number>
If you use OBS Virtual Camera
Start OBS Virtual Camera first.

Re-run the scan script above.

A new index should appear — use that one in camera_index.

Quick sanity check after setting index
Save config.yaml

Run python app.py

Click Start in dashboard and test one battle intro.

If no counts happen, try next valid index (0, then 1, etc.) and retest.

If you want, I can also give you a tiny script that opens each index in a preview window so you can visually confirm which one is your capture card vs OBS virtual cam.

where do i add the into the venv
Copy
Good catch — you don’t add camera/Tesseract into the venv folder itself.

What goes in venv vs system
Inside venv: Python packages (pip install -r requirements.txt).

Outside venv (system install): Tesseract program (tesseract.exe) and PATH entry on Windows.

Camera index: set in your project config.yaml, not in venv.

Exact Windows flow
Open terminal in project folder.

Create/activate venv:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
Install Python deps:

pip install -r requirements.txt
Create config:

copy config.example.yaml config.yaml
Edit config.yaml and set:

camera_index: 0
(or whatever index you found).

Run app:

python app.py
If you meant “where do I paste that camera-index test script,” run it in the same terminal after activating .venv (you don’t save it inside venv).

no this python - << 'PY'\nimport cv2\n\nprint("Scanning camera indexes 0-9...")\nfor i in range(10):\n    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # CAP_DSHOW helps on Windows\n    ok, frame = cap.read()\n    opened = cap.isOpened()\n    cap.release()\n    if opened and ok and frame is not None:\n        print(f"Index {i}: OK")\n    else:\n        print(f"Index {i}: no signal")\nPY
Copy
Ahh got it — you’re right. That python - << 'PY' ... style is Linux/macOS style, not friendly in normal Windows PowerShell.

Use this instead on Windows 👇

Option A (easiest): make a small file and run it
1) Create find_camera.py in your project folder with this code:
import cv2

print("Scanning camera indexes 0-9...")
for i in range(10):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    opened = cap.isOpened()
    ok, frame = cap.read()
    cap.release()

    if opened and ok and frame is not None:
        print(f"Index {i}: OK")
    else:
        print(f"Index {i}: no signal")
2) Run it (after venv is activated):
python find_camera.py
3) Put the working number in config.yaml:
camera_index: 1
(Use whatever index printed OK).

Option B: PowerShell inline (no file)
@'
import cv2
print("Scanning camera indexes 0-9...")
for i in range(10):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    opened = cap.isOpened()
    ok, frame = cap.read()
    cap.release()
    print(f"Index {i}: {'OK' if opened and ok and frame is not None else 'no signal'}")
'@ | python -
If you want, I can give you the next script that opens a preview window for each working index so you can tell which one is your capture card vs OBS Virtual Camera.

(.venv) PS C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main> python find_camera.py\nScanning camera indexes 0-9...\n[ WARN:0@0.420] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 0: no signal\n[ WARN:0@0.443] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 1: no signal\nIndex 2: OK\n[ WARN:0@0.749] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 3: no signal\n[ WARN:0@0.754] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 4: no signal\n[ WARN:0@0.761] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 5: no signal\n[ WARN:0@0.767] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 6: no signal\n[ WARN:0@0.774] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 7: no signal\n[ WARN:0@0.780] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 8: no signal\n[ WARN:0@0.785] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 9: no signal\n(.venv) PS C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main> python find_camera.py\nScanning camera indexes 0-9...\n[ WARN:0@0.405] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 0: no signal\n[ WARN:0@0.428] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index\nIndex 1: no signal\nIndex 2: OK\n[ WARN:0@0.728] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 3: no signal\n[ WARN:0@0.735] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 4: no signal\n[ WARN:0@0.741] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 5: no signal\n[ WARN:0@0.747] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 6: no signal\n[ WARN:0@0.752] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 7: no signal\n[ WARN:0@0.759] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 8: no signal\n[ WARN:0@0.765] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 9: no signal\n(.venv) PS C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main>
Copy
Perfect — this output is actually good.
The key line is:

Index 2: OK ✅

So your capture source is available at camera index 2.

Do this now
Open config.yaml

Set:

camera_index: 2
(camera_index is exactly what the app uses for the video source).

Start app:

python app.py
Then open dashboard at http://localhost:5000.

Click Start on dashboard and test a battle.

About those WARN lines
Those VIDEOIO(DSHOW)... can't be used to capture by index warnings for other indexes are normal during scanning.
What matters is at least one working index — and yours is 2.

If it still doesn’t count battles
Make sure OCR is enabled in config (ocr.enabled: true).

Keep playing with ocr.roi and ocr.min_confidence.

If OBS is also using the same device, use OBS Virtual Camera and scan indexes again (the working index may change).

You’re basically past the hard part now — set camera_index: 2 and run.

user attachment image
user attachment image
user attachment image
this is what im seeing im not seeing anything fom the overlay itself
Copy
You’re very close — your screenshots actually help a lot.

Why it looks “blank”
Your overlay page is designed as a transparent background with white text for streaming. In code, the overlay text color is white and page background is transparent.
So if OBS/browser rendering has any issue, it can look like an empty black box.

Also, /overlay should always render at least:

target text (Current Hunt fallback)

count (0)

So if literally nothing appears, this is usually an OBS browser-source loading/cache/config issue, not your counter state.

Do this exact checklist in OBS (in order)
Delete current Browser Source and re-add a new one.

URL: http://127.0.0.1:5000/overlay
(use 127.0.0.1 instead of localhost just to avoid hostname oddities)

Width/Height: set to 1920x1080 temporarily.

Clear/empty Custom CSS completely (for now).

Check:

✅ “Refresh browser when scene becomes active”

✅ “Shutdown source when not visible” OFF (temporarily)

Click Refresh cache of current page in Browser Source properties.

Keep python app.py running and open http://127.0.0.1:5000/overlay in Chrome at the same time.

Fast connectivity test
If overlay still black in OBS:

Change Browser Source URL to http://127.0.0.1:5000/ (dashboard page).

If dashboard shows in OBS, then OBS can reach Flask and the issue is purely overlay styling/render.

If dashboard also doesn’t show, OBS cannot reach your local Flask process (URL/port/firewall/process issue).

Dashboard and overlay URLs are the intended routes in the app docs and code.

If you want a quick guaranteed-visible workaround
I can patch templates/overlay.html to add:

bright neon text

optional semi-transparent panel background

debug border

So even if transparency/styles are weird in OBS, you’ll always see it immediately.

ok i can see it now but the number is not incremementing
Copy
Nice — great progress. If overlay shows but counter won’t auto-increment, it means detection conditions are not being met.

Auto-increment only happens when all of these pass:

OCR/template signal is true

motion score passes threshold

cooldown passed

detector thinks this is a new battle state

Quick isolation test (1 minute)
Click +1 Manual on dashboard.

If number changes, overlay/state is fine, and only auto-detection needs tuning.

Most likely cause in your setup: OCR strictness
Your default config phrases are wild + appeared, and confidence is computed from phrase hits.
With current default 0.55, OCR usually needs both words recognized cleanly.

Change these in config.yaml:
poll_interval_ms: 120
cooldown_seconds: 2.0

ocr:
  enabled: true
  roi: [0.05, 0.70, 0.90, 0.28]
  phrases:
    - "wild"
    - "appeared"
    - "go!"
    - "sent out"
  min_confidence: 0.34

detection:
  min_motion_score: 4.0
Why:

lower confidence => one phrase can still trigger

slightly bigger ROI => catches dialogue box better

lower motion threshold => less likely to miss battle transition

faster polling => less likely to miss short intro text

(These fields are the ones the app reads from config.)

Restart required
After editing config.yaml, stop and run again:

python app.py
Then click Start and test a new encounter from outside battle.

Important behavior note
The detector increments on new battle start text/event, not while already in battle menu.
So if you test while already in “What will X do?”, it may not increment until you leave and trigger a fresh encounter.

If you want, next I can give you a tiny debug script that prints OCR text every frame so we can tune phrases/ROI exactly for your game feed in 2–3 minutes.

still now is there a way to track it to the source in obs maybe thatll make it easier to actualy track the screen maybe it cant pull up the virtual camera
Copy
Yes — you’re thinking in the right direction.

Short answer
This app cannot read an OBS scene/source directly right now.
It only reads a camera device via OpenCV (cv2.VideoCapture(camera_index)).
So the correct method is: OBS source → OBS Virtual Camera → app camera_index.

Recommended setup (most reliable)
In OBS, put your capture card in a scene and make sure it is visible.

Click Start Virtual Camera in OBS.

Run your camera-index scan again.

Set camera_index in config.yaml to the index that corresponds to OBS Virtual Camera.

Restart app (python app.py) and click Start in dashboard.

If virtual camera still doesn’t show in scan
Try this improved scan script (checks multiple Windows backends):

import cv2

backends = [
    ("DEFAULT", None),
    ("DSHOW", cv2.CAP_DSHOW),
    ("MSMF", cv2.CAP_MSMF),
]

for name, backend in backends:
    print(f"\n=== {name} ===")
    for i in range(10):
        cap = cv2.VideoCapture(i) if backend is None else cv2.VideoCapture(i, backend)
        opened = cap.isOpened()
        ok, frame = cap.read()
        cap.release()
        if opened and ok and frame is not None:
            print(f"Index {i}: OK")
Then use the index that is OK under either DEFAULT/MSMF if DSHOW misses it.

Why this matters
Your detector depends on seeing the same video feed where battle text appears. If it opens the wrong device (or a black virtual cam), OCR/template never triggers, so count never increments.

If you want, I can patch the app next so it supports a configurable backend (DSHOW/MSMF/DEFAULT) in config.yaml — that would make OBS virtual camera detection on Windows much easier.

(.venv) PS C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main> python find_camera.py\n\n=== DEFAULT ===\n[ WARN:0@6.573] global cap_msmf.cpp:476 `anonymous-namespace'::SourceReaderCB::OnReadSample videoio(MSMF): OnReadSample() is called with error status: -1072875772\n[ WARN:0@6.576] global cap_msmf.cpp:488 `anonymous-namespace'::SourceReaderCB::OnReadSample videoio(MSMF): async ReadSample() call is failed with error status: -1072875772\n[ WARN:1@6.578] global cap_msmf.cpp:1769 CvCapture_MSMF::grabFrame videoio(MSMF): can't grab frame. Error: -1072875772\n[ERROR:1@6.788] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\nIndex 2: OK\n[ERROR:1@7.419] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@7.562] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@7.713] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@7.856] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@8.009] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@8.148] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@8.294] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n\n=== DSHOW ===\n[ WARN:1@8.644] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.659] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \nIndex 2: OK\n[ WARN:1@8.957] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.960] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.963] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.967] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.970] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.974] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.977] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n\n=== MSMF ===\n[ WARN:0@14.695] global cap_msmf.cpp:476 `anonymous-namespace'::SourceReaderCB::OnReadSample videoio(MSMF): OnReadSample() is called with error status: -1072875772\n[ WARN:0@14.697] global cap_msmf.cpp:488 `anonymous-namespace'::SourceReaderCB::OnReadSample videoio(MSMF): async ReadSample() call is failed with error status: -1072875772\n[ WARN:1@14.700] global cap_msmf.cpp:1769 CvCapture_MSMF::grabFrame videoio(MSMF): can't grab frame. Error: -1072875772\n[ WARN:1@14.774] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@14.929] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.072] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.232] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.384] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.526] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.668] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.811] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.968] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n(.venv) PS C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main>
Copy
This output is actually telling us something clear:

Index 2: OK under both DEFAULT and DSHOW = your usable video device is index 2.

All the other WARN/ERROR lines are noise from probing invalid indexes/backends.

So your camera access is not the blocker now.

What to set now
In config.yaml:

camera_index: 2
That is the field the app reads for capture input.

And the detector opens that with OpenCV VideoCapture.

Why it still may not increment
At this point, it’s usually OCR/trigger tuning, not camera open:

OCR must detect configured phrases (wild, appeared by default).

Motion must exceed threshold.

Cooldown/new-battle gating must pass.

If OCR misses intro text even once, counter won’t tick.

Do this exact next test
Keep camera_index: 2.

Lower sensitivity barriers in config.yaml:

poll_interval_ms: 120
cooldown_seconds: 1.5
ocr:
  min_confidence: 0.34
detection:
  min_motion_score: 3.0
Restart app.

Start from overworld and enter a brand new battle (don’t test while already in “Fight/Bag” menu).

If you want, I can give you a copy/paste OCR debug script next that prints exactly what text Tesseract is reading from your ROI, so we can tune phrases in one pass and make auto-count reliable.

(.venv) PS C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main> python find_camera.py\n\n=== DEFAULT ===\n[ WARN:0@6.394] global cap_msmf.cpp:476 `anonymous-namespace'::SourceReaderCB::OnReadSample videoio(MSMF): OnReadSample() is called with error status: -1072875772\n[ WARN:0@6.396] global cap_msmf.cpp:488 `anonymous-namespace'::SourceReaderCB::OnReadSample videoio(MSMF): async ReadSample() call is failed with error status: -1072875772\n[ WARN:1@6.399] global cap_msmf.cpp:1769 CvCapture_MSMF::grabFrame videoio(MSMF): can't grab frame. Error: -1072875772\n[ERROR:1@6.519] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\nIndex 2: OK\n[ERROR:1@7.131] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@7.279] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@7.423] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@7.580] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@7.718] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@7.871] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n[ERROR:1@8.013] global obsensor_uvc_stream_channel.cpp:158 cv::obsensor::getStreamChannelGroup Camera index out of range\n\n=== DSHOW ===\n[ WARN:1@8.327] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.343] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index\nIndex 2: OK\n[ WARN:1@8.619] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.622] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.625] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index\n[ WARN:1@8.629] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.633] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.637] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n[ WARN:1@8.641] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(DSHOW): backend is generally available but can't be used to capture by index      \n\n=== MSMF ===\n[ WARN:0@14.424] global cap_msmf.cpp:476 `anonymous-namespace'::SourceReaderCB::OnReadSample videoio(MSMF): OnReadSample() is called with error status: -1072875772\n[ WARN:0@14.426] global cap_msmf.cpp:488 `anonymous-namespace'::SourceReaderCB::OnReadSample videoio(MSMF): async ReadSample() call is failed with error status: -1072875772\n[ WARN:1@14.428] global cap_msmf.cpp:1769 CvCapture_MSMF::grabFrame videoio(MSMF): can't grab frame. Error: -1072875772\n[ WARN:1@14.516] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@14.654] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@14.800] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@14.949] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.090] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.225] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.372] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.517] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index      \n[ WARN:1@15.654] global cap.cpp:344 cv::VideoCapture::open VIDEOIO(MSMF): backend is generally available but can't be used to capture by index 

does the setting he virtual camera is on matter i put it on program now it was on preview before
Copy
Yes — that OBS Virtual Camera setting can matter.

In OBS Studio Mode
If Virtual Camera is set to Preview, it sends whatever is in the Preview pane.
If it’s set to Program, it sends the live Program output.

So if your app is reading OBS Virtual Camera and you had it on Preview while preview wasn’t your gameplay scene, the tracker can see wrong/blank frames and never increment.

What to use
Set Virtual Camera output to Program (recommended).

Make sure your gameplay/capture-card scene is actually on Program.

Then run tracker with the index that corresponds to that feed (camera_index).

The app only reads whichever camera index you configured via OpenCV; it does not read OBS scenes directly.

Quick confirm in 30 seconds
Run a tiny preview script for camera_index: 2 and verify you see your game feed in the OpenCV window.
If you don’t see gameplay there, detection can’t work yet.

Given your logs, Index 2: OK is stable — now the key is making sure index 2 is the actual battle feed (program output/capture card), not a blank/other source.

are there other cameras that are foundby the scriptor is #2 the only one still
Copy
From the logs you pasted, #2 is the only usable camera index right now.

Index 2: OK

all others returned no signal / backend warnings

So for this app, treat 2 as your active source and set:

camera_index: 2

If you want to double-check for hidden devices, scan a wider range (0–20). But based on your output so far, yes — only #2 is valid at the moment.
And that’s fine; the app only needs one working index to run capture/detection.

(.venv) PS C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main> python app.py        \n * Serving Flask app 'app'\n * Debug mode: off\nWARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n * Running on all addresses (0.0.0.0)\n * Running on http://127.0.0.1:5000\n * Running on http://192.168.1.66:5000\nPress CTRL+C to quit\n127.0.0.1 - - [09/Apr/2026 15:48:17] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:17] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:18] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:19] "GET / HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:19] "GET /uploads/target.png HTTP/1.1" 304 -\n127.0.0.1 - - [09/Apr/2026 15:48:20] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:20] "POST /api/start HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:21] "GET /api/state HTTP/1.1" 200 -\nException in thread Thread-8 (detector_loop):\nTraceback (most recent call last):\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 275, in run_tesseract       \n    proc = subprocess.Popen(cmd_args, **subprocess_args())\n  File "C:\Python313\Lib\subprocess.py", line 1038, in __init__\n    self._execute_child(args, executable, preexec_fn, close_fds,\n    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n                        pass_fds, cwd, env,\n                        ^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n                        gid, gids, uid, umask,\n                        ^^^^^^^^^^^^^^^^^^^^^^\n                        start_new_session, process_group)\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Python313\Lib\subprocess.py", line 1550, in _execute_child     \n    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,\n                       ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n                             # no special security\n                             ^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n                             cwd,\n                             ^^^^\n                             startupinfo)\n                             ^^^^^^^^^^^^\nFileNotFoundError: [WinError 2] The system cannot find the file specified \n\nDuring handling of the above exception, another exception occurred:       \n\nTraceback (most recent call last):\n  File "C:\Python313\Lib\threading.py", line 1041, in _bootstrap_inner    \n    self.run()\n    ~~~~~~~~^^\n  File "C:\Python313\Lib\threading.py", line 992, in run\n    self._target(*self._args, **self._kwargs)\n    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\app.py", line 53, in detector_loop\n    if running and detector.detect_new_battle():\n                   ~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 99, in detect_new_battle\n    signal = self._ocr_hit(frame) or self._template_hit(frame)\n             ~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 76, in _ocr_hit\n    text = pytesseract.image_to_string(gray).lower()\n           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 486, in image_to_string     \n    return {\n           ~\n    ...<2 lines>...\n        Output.STRING: lambda: run_and_get_output(*args),\n        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n    }[output_type]()\n    ~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 489, in <lambda>\n    Output.STRING: lambda: run_and_get_output(*args),\n                           ~~~~~~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 352, in run_and_get_output  \n    run_tesseract(**kwargs)\n    ~~~~~~~~~~~~~^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 280, in run_tesseract       \n    raise TesseractNotFoundError()\npytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH. See README file for more information.\n127.0.0.1 - - [09/Apr/2026 15:48:22] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:23] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:24] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:25] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:26] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:27] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:28] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:29] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:30] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:31] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:32] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:33] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:34] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:35] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:36] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:37] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:38] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:39] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:40] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:41] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:42] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:43] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:44] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:45] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:46] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:47] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:48] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:49] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:50] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:51] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:52] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:53] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:54] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:55] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:56] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:57] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:58] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:59] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:00] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:01] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:02] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:03] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:04] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:05] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:06] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:07] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:08] "GET (.venv) PS C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main> python app.py        \n * Serving Flask app 'app'\n * Debug mode: off\nWARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n * Running on all addresses (0.0.0.0)\n * Running on http://127.0.0.1:5000\n * Running on http://192.168.1.66:5000\nPress CTRL+C to quit\n127.0.0.1 - - [09/Apr/2026 15:48:17] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:17] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:18] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:19] "GET / HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:19] "GET /uploads/target.png HTTP/1.1" 304 -\n127.0.0.1 - - [09/Apr/2026 15:48:20] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:20] "POST /api/start HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:21] "GET /api/state HTTP/1.1" 200 -\nException in thread Thread-8 (detector_loop):\nTraceback (most recent call last):\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 275, in run_tesseract       \n    proc = subprocess.Popen(cmd_args, **subprocess_args())\n  File "C:\Python313\Lib\subprocess.py", line 1038, in __init__\n    self._execute_child(args, executable, preexec_fn, close_fds,\n    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n                        pass_fds, cwd, env,\n                        ^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n                        gid, gids, uid, umask,\n                        ^^^^^^^^^^^^^^^^^^^^^^\n                        start_new_session, process_group)\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Python313\Lib\subprocess.py", line 1550, in _execute_child     \n    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,\n                       ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n                             # no special security\n                             ^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n                             cwd,\n                             ^^^^\n                             startupinfo)\n                             ^^^^^^^^^^^^\nFileNotFoundError: [WinError 2] The system cannot find the file specified \n\nDuring handling of the above exception, another exception occurred:       \n\nTraceback (most recent call last):\n  File "C:\Python313\Lib\threading.py", line 1041, in _bootstrap_inner    \n    self.run()\n    ~~~~~~~~^^\n  File "C:\Python313\Lib\threading.py", line 992, in run\n    self._target(*self._args, **self._kwargs)\n    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\app.py", line 53, in detector_loop\n    if running and detector.detect_new_battle():\n                   ~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 99, in detect_new_battle\n    signal = self._ocr_hit(frame) or self._template_hit(frame)\n             ~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 76, in _ocr_hit\n    text = pytesseract.image_to_string(gray).lower()\n           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 486, in image_to_string     \n    return {\n           ~\n    ...<2 lines>...\n        Output.STRING: lambda: run_and_get_output(*args),\n        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n    }[output_type]()\n    ~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 489, in <lambda>\n    Output.STRING: lambda: run_and_get_output(*args),\n                           ~~~~~~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 352, in run_and_get_output  \n    run_tesseract(**kwargs)\n    ~~~~~~~~~~~~~^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 280, in run_tesseract       \n    raise TesseractNotFoundError()\npytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH. See README file for more information.\n127.0.0.1 - - [09/Apr/2026 15:48:22] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:23] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:24] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:25] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:26] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:27] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:28] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:29] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:30] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:31] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:32] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:33] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:34] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:35] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:36] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:37] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:38] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:39] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:40] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:41] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:42] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:43] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:44] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:45] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:46] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:47] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:48] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:49] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:50] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:51] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:52] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:53] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:54] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:55] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:56] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:57] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:58] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:48:59] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:00] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:01] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:02] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:03] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:04] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:05] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:06] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:07] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 15:49:08] "GET
Copy
You found the root cause ✅

Your crash is exactly this:

pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH.

So the detector thread dies right after you click Start, and auto-counting stops.
OCR is required in your current config path (_ocr_hit calls pytesseract.image_to_string).
README also states Tesseract must be installed and in PATH on Windows.

Fix it on Windows (do this exactly)
1) Install Tesseract (if not installed)
Use UB Mannheim Windows installer:

https://github.com/UB-Mannheim/tesseract/wiki

2) Add install folder to PATH
Usually:

C:\Program Files\Tesseract-OCR\

3) Open new PowerShell and test:
tesseract --version
where.exe tesseract
If these fail, PATH is still wrong.

4) Restart your app
python app.py
Then click Start again.

Quick temporary workaround (if needed right now)
If you want app not to crash while fixing Tesseract:

set ocr.enabled: false in config

but then you must configure template detection (template.enabled: true + image_path) or no auto-detections will happen.

If you want, I can give you a copy/paste PowerShell command to add Tesseract to PATH automatically, then verify it in one go.

user attachment image
this is the paths
Copy
Perfect — that PATH screenshot looks correct ✅
C:\Program Files\Tesseract-OCR is the right entry.

The most likely issue now is: your PowerShell session was opened before PATH changed.

Do this now (exact)
Click OK on all Environment Variable windows.

Close all PowerShell windows.

Open a brand-new PowerShell.

Run:

where.exe tesseract
tesseract --version
You should see something like:
C:\Program Files\Tesseract-OCR\tesseract.exe

If that works, start app again:

python app.py
Then click Start in dashboard.

If where.exe tesseract still fails
Use direct exe test:

& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
If this works, PATH just didn’t refresh globally yet (log out/reboot once).

If this fails, reinstall Tesseract installer (not just source zip).

Also, the C:\Users\rcolt\Downloads\tesseract-main entry is source code and not needed for runtime OCR; the executable path is the important one.
Your app’s OCR call will fail until Windows can resolve tesseract on PATH.

i restarted my computer still not working for where
Windows PowerShell\nCopyright (C) Microsoft Corporation. All rights reserved.\n\nInstall the latest PowerShell for new features and improvements! https://aka.ms/PSWindows\n\nPS C:\Users\rcolt> where.exe tesseract\n>> tesseract --version\nINFO: Could not find files for the given pattern(s).\ntesseract : The term 'tesseract' is not recognized as the name of a cmdlet, function, script file, or operable\nprogram. Check the spelling of the name, or if a path was included, verify that the path is correct and try again.\nAt line:2 char:1\n+ tesseract --version\n+ ~~~~~~~~~\n    + CategoryInfo          : ObjectNotFound: (tesseract:String) [], CommandNotFoundException\n    + FullyQualifiedErrorId : CommandNotFoundException\n\nPS C:\Users\rcolt> & "C:\Program Files\Tesseract-OCR\tesseract.exe" --version\ntesseract v5.5.0.20241111\n leptonica-1.85.0\n  libgif 5.2.2 : libjpeg 8d (libjpeg-turbo 3.0.4) : libpng 1.6.44 : libtiff 4.7.0 : zlib 1.3.1 : libwebp 1.4.0 : libopenjp2 2.5.2\n Found AVX2\n Found AVX\n Found FMA\n Found SSE4.1\n Found libarchive 3.7.7 zlib/1.3.1 liblzma/5.6.3 bz2lib/1.0.8 liblz4/1.10.0 libzstd/1.5.6\n Found libcurl/8.11.0 Schannel zlib/1.3.1 brotli/1.1.0 zstd/1.5.6 libidn2/2.3.7 libpsl/0.21.5 libssh2/1.11.0\nPS C:\Users\rcolt>\n
Copy
Summary
You diagnosed the exact issue correctly: Tesseract runs by absolute path, but Windows still can’t resolve tesseract from PATH. I patched the tracker so you can now set an explicit executable path in config via ocr.tesseract_cmd (no PATH dependency required).

I updated the detector to auto-try the common Windows install path (C:\Program Files\Tesseract-OCR\tesseract.exe) and to avoid crashing the detector thread if Tesseract is missing; it now logs a warning once and keeps running instead of dying.

I documented the new config option in README + example config so setup is explicit for Windows users with PATH issues.

What you should do on your PC now
Since your direct command works:

& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
set this in your config.yaml:

ocr:
  enabled: true
  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
Then restart:

python app.py
This bypasses where.exe tesseract entirely.

Testing

✅ python -m compileall app.py detector.py state.py

Committed on current branch:

cbcee36 — Handle missing Tesseract path and support explicit OCR binary path


Files (8)
still not incremementing what else do i need to try my guess is the camera index but im not sure how else to find the camera index
Copy
You’re probably past the camera-index issue already.

From your earlier scans, index 2 was consistently OK, so this is more likely OCR trigger tuning, not wrong index.
The app only uses whatever camera_index is set in config and opens that device directly.

Best way to 100% confirm camera index (visual test)
Create preview_index.py:

import cv2

index = 2  # change this to test 0,1,2,3...
cap = cv2.VideoCapture(index)

if not cap.isOpened():
    print(f"Index {index} failed to open")
    raise SystemExit(1)

print(f"Showing index {index}. Press Q to quit.")
while True:
    ok, frame = cap.read()
    if not ok:
        print("No frame")
        break
    cv2.putText(frame, f"INDEX {index}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Camera Preview", frame)
    if cv2.waitKey(1) & 0xFF in (ord('q'), ord('Q')):
        break

cap.release()
cv2.destroyAllWindows()
Run:

python preview_index.py
If you see your game feed, that index is correct.

If index is correct but still no auto increment
Then tune detection (this is the likely part):

ocr.tesseract_cmd set (since PATH issue earlier).

Lower OCR strictness (ocr.min_confidence).

Increase polling speed (poll_interval_ms lower).

Lower motion threshold (detection.min_motion_score).

Ensure you test from new battle entry, not already in menu.

Detection requires signal + motion + cooldown/new-state logic together.

If you want, I can give you a ready-to-paste “high sensitivity” config.yaml for Gen 3 battle intros so you can test immediately.

user attachment image
Ok this window popped up
Copy
That screenshot explains everything 🎯

Your app is reading index 2, but index 2 is currently showing a black OBS output with your overlay only (not the game battle feed).
So OCR never sees battle text, and auto-increment won’t trigger.

Why this happens
BattleDetector can only increment when OCR/template detects battle-start signal in the incoming frame.
Right now the frame is basically black + your counter overlay, not Pokémon battle UI.

Fix (recommended OBS setup)
1) Create a dedicated OBS scene for tracker input
Name it something like: TrackerInput

Add capture card source only (game video).

Do not include your browser overlay in this scene.

2) Set OBS Virtual Camera to output that scene/program
In Studio Mode, ensure TrackerInput is what Program is outputting (or set virtual cam source accordingly).

3) Keep app camera_index at 2
Since index 2 is virtual cam, keep using it, but make sure virtual cam content is actual gameplay.

4) Re-run preview script
You should now see full game frame in preview window (not black).

Important anti-loop rule
Don’t feed overlay back into the same virtual camera source the tracker reads, or you get recursion/black/empty frames (exactly what your screenshot shows).

If you want, I can give you a clean 2-scene OBS layout (Game scene + Overlay scene) so the tracker reads game-only while stream still shows game + overlay.

no no the window came up with the game it was the correct index the game was just loading sorry so its something else
Copy
Got it — thanks for clarifying. If index is correct, then the blocker is almost certainly detection thresholds/text matching, not camera selection.

Let’s do a fast, reliable debug pass.

1) Confirm detector thread is not crashing
When you click Start, you should not see Tesseract exceptions anymore.
If it crashes, no auto increment can happen.

(Detector increments only inside detect_new_battle() when signal + motion + cooldown/new-battle checks pass.)

2) Use this high-sensitivity test config first
In config.yaml set:

camera_index: 2
poll_interval_ms: 80
cooldown_seconds: 1.0

ocr:
  enabled: true
  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
  roi: [0.03, 0.68, 0.94, 0.30]
  phrases:
    - "wild"
    - "appeared"
    - "go!"
    - "sent out"
  min_confidence: 0.25

template:
  enabled: false
  image_path: ""
  threshold: 0.88

detection:
  motion_roi: [0.0, 0.0, 1.0, 1.0]
  min_motion_score: 1.5
These keys are all supported by your loader/config model.

3) Critical test method
Start from outside battle, then trigger a fresh encounter.
Don’t test while already on the battle command menu — detector is designed to catch new battle start transitions.

4) If still not counting: switch to template mode (more stable)
OCR can miss retro pixel text depending on scaling/filtering.
Template matching is often more stable for emulator/capture visuals.

Crop a small, consistent UI element that appears right at battle start.

Save image locally.

Set:

template:
  enabled: true
  image_path: "C:\\path\\to\\battle_start_template.png"
  threshold: 0.80
Keep OCR enabled too (hybrid gives best chance).

If you want, I can give you a ready-to-use OCR debug script that prints exactly what text Tesseract is seeing from your ROI every second, so we can tune this in one round instead of guessing.

127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -      \n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -      \n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -      \n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -      \n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -      \n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:25] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:25] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:25] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:26] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:26] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:27] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:28] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:28] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:29] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:29] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:30] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:30] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:30] "POST /api/stop HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:31] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:31] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:32] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:32] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:32] "POST /api/start HTTP/1.1" 200 -\nException in thread Thread-47 (detector_loop):\nTraceback (most recent call last):\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 275, in run_tesseract       \n    proc = subprocess.Popen(cmd_args, **subprocess_args())\n  File "C:\Python313\Lib\subprocess.py", line 1038, in __init__\n    self._execute_child(args, executable, preexec_fn, close_fds,\n    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n                        pass_fds, cwd, env,\n                        ^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n                        gid, gids, uid, umask,\n                        ^^^^^^^^^^^^^^^^^^^^^^\n                        start_new_session, process_group)\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Python313\Lib\subprocess.py", line 1550, in _execute_child     \n    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,\n                       ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n                             # no special security\n                             ^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n                             cwd,\n                             ^^^^\n                             startupinfo)\n                             ^^^^^^^^^^^^\nFileNotFoundError: [WinError 2] The system cannot find the file specified \n\nDuring handling of the above exception, another exception occurred:       \n\nTraceback (most recent call last):\n  File "C:\Python313\Lib\threading.py", line 1041, in _bootstrap_inner    \n    self.run()\n    ~~~~~~~~^^\n  File "C:\Python313\Lib\threading.py", line 992, in run\n    self._target(*self._args, **self._kwargs)\n    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\app.py", line 53, in detector_loop\n    if running and detector.detect_new_battle():\n                   ~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 99, in detect_new_battle\n    signal = self._ocr_hit(frame) or self._template_hit(frame)\n             ~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 76, in _ocr_hit\n    text = pytesseract.image_to_string(gray).lower()\n           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 486, in image_to_string     \n    return {\n           ~\n    ...<2 lines>...\n        Output.STRING: lambda: run_and_get_output(*args),\n        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n    }[output_type]()\n    ~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 489, in <lambda>\n    Output.STRING: lambda: run_and_get_output(*args),\n                           ~~~~~~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 352, in run_and_get_output  \n    run_tesseract(**kwargs)\n    ~~~~~~~~~~~~~^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 280, in run_tesseract       \n    raise TesseractNotFoundError()\npytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH. See README file for more information.\n127.0.0.1 - - [09/Apr/2026 16:10:33] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:33] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:34] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:34] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:35] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:35] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:36] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:36] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:37] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:37] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:38] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:38] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:39] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:39] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:40] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:40] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:41] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:41] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:42] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:42] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:43] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:43] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:44] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:44] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:45] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:45] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:46] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:46] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:47] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:47] "GET /api/state HTTP/1.1" 200 -127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -      \n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -      \n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -      \n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -      \n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -      \n127.0.0.1 - - [09/Apr/2026 16:10:24] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:25] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:25] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:25] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:26] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:26] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:27] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:28] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:28] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:29] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:29] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:30] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:30] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:30] "POST /api/stop HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:31] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:31] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:32] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:32] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:32] "POST /api/start HTTP/1.1" 200 -\nException in thread Thread-47 (detector_loop):\nTraceback (most recent call last):\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 275, in run_tesseract       \n    proc = subprocess.Popen(cmd_args, **subprocess_args())\n  File "C:\Python313\Lib\subprocess.py", line 1038, in __init__\n    self._execute_child(args, executable, preexec_fn, close_fds,\n    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n                        pass_fds, cwd, env,\n                        ^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n                        gid, gids, uid, umask,\n                        ^^^^^^^^^^^^^^^^^^^^^^\n                        start_new_session, process_group)\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Python313\Lib\subprocess.py", line 1550, in _execute_child     \n    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,\n                       ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n                             # no special security\n                             ^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n                             cwd,\n                             ^^^^\n                             startupinfo)\n                             ^^^^^^^^^^^^\nFileNotFoundError: [WinError 2] The system cannot find the file specified \n\nDuring handling of the above exception, another exception occurred:       \n\nTraceback (most recent call last):\n  File "C:\Python313\Lib\threading.py", line 1041, in _bootstrap_inner    \n    self.run()\n    ~~~~~~~~^^\n  File "C:\Python313\Lib\threading.py", line 992, in run\n    self._target(*self._args, **self._kwargs)\n    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\app.py", line 53, in detector_loop\n    if running and detector.detect_new_battle():\n                   ~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 99, in detect_new_battle\n    signal = self._ocr_hit(frame) or self._template_hit(frame)\n             ~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 76, in _ocr_hit\n    text = pytesseract.image_to_string(gray).lower()\n           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 486, in image_to_string     \n    return {\n           ~\n    ...<2 lines>...\n        Output.STRING: lambda: run_and_get_output(*args),\n        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n    }[output_type]()\n    ~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 489, in <lambda>\n    Output.STRING: lambda: run_and_get_output(*args),\n                           ~~~~~~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 352, in run_and_get_output  \n    run_tesseract(**kwargs)\n    ~~~~~~~~~~~~~^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 280, in run_tesseract       \n    raise TesseractNotFoundError()\npytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH. See README file for more information.\n127.0.0.1 - - [09/Apr/2026 16:10:33] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:33] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:34] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:34] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:35] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:35] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:36] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:36] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:37] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:37] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:38] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:38] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:39] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:39] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:40] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:40] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:41] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:41] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:42] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:42] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:43] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:43] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:44] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:44] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:45] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:45] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:46] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:46] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:47] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:10:47] "GET /api/state HTTP/1.1" 200 -

i stopped the program and started again and once i started it again i get those flags
Copy
Yep — this log tells us exactly what happened:

What’s happening
When you hit Start, detector thread calls OCR.

OCR tries to launch tesseract and fails.

Thread crashes, so auto increment stops.

The key clue: your traceback points to detector.py line where OCR is called directly, which means you’re still running an older copy of files (before my fallback patch). In the updated code, _ocr_hit has a Tesseract guard and optional explicit ocr.tesseract_cmd.

Fastest fix right now (works even on older copy)
In the same PowerShell window before python app.py, run:

$env:PATH += ";C:\Program Files\Tesseract-OCR"
$env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"
python app.py
Then click Start again.

Better permanent fix (recommended)
Update your local project files to latest version (the patched one), then in config.yaml set:

ocr:
  enabled: true
  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
ocr.tesseract_cmd is now supported in config loading and docs in current repo version.

If you need it running immediately without OCR
As temporary fallback:

ocr:
  enabled: false
But then enable template mode or auto-increment won’t fire from OCR at all.

If you want, I can walk you through a 2-minute file check to confirm whether your local detector.py is old or patched.

user attachment image
# Copy this file to config.yaml and tune thresholds based on your game/capture feed.\ncamera_index: 2\npoll_interval_ms: 80\ncooldown_seconds: 1.0\n\n# OCR mode checks for expected battle text fragments.\nocr:\n  enabled: true\n  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"\n  roi: [0.05, 0.70, 0.90, 0.28]\n  phrases:\n    - "wild"\n    - "appeared"\n    - "go!"\n    - "sent out"\n  min_confidence: 0.25\n\n# Template mode checks for visual match of a battle-start indicator image.\ntemplate:\n  enabled: false\n  image_path: ""\n  threshold: 0.88\n\n# Optional per-game encounter gating to prevent duplicate counts\n# when battle intro remains on-screen for multiple polling cycles.\ndetection:\n  motion_roi: [0.0, 0.0, 1.0, 1.0]\n  min_motion_score: 1.5\n
Copy
You’re super close — I can see the issue from your screenshot.

The actual problem now
You ran:

python app.py from C:\Users\rcolt>
and Python says it can’t open C:\Users\rcolt\app.py.

So the app is not being launched from the project folder.

I also see a typo in one command path: Tesseract-ORC (should be Tesseract-OCR).

Do this exact sequence (copy/paste)
cd "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main"
.\.venv\Scripts\Activate.ps1

# Optional check:
Get-Location
Test-Path .\app.py
Test-Path .\config.yaml

python app.py
If Test-Path .\app.py prints True, you’re in the right place.

This matches how the app is intended to run from project root (python app.py).

Then verify OCR binary path in config
In config.yaml, keep:

ocr:
  enabled: true
  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
That key is supported by the current loader and config schema.

One more quick check
From the same terminal (while in project folder):

& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
If that works and app is started from correct folder, the detector should stop throwing TesseractNotFoundError.

If you want, next I can give you a single “launch.ps1” script so you don’t have to remember any of this each time.

PS C:\Users\rcolt> $env:PATH += ";C:\Program Files\Tesseract-OCR"\n>> $env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"\n>> python app.py\nC:\Python313\python.exe: can't open file 'C:\\Users\\rcolt\\app.py': [Errno 2] No such file or directory\nPS C:\Users\rcolt> cd "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main"\n>> .\.venv\Scripts\Activate.ps1\n>>\n>> # Optional check:\n>> Get-Location\n>> Test-Path .\app.py\n>> Test-Path .\config.yaml\n>>\n>> python app.py\n\n * Serving Flask app 'app'\n * Debug mode: off\nWARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n * Running on all addresses (0.0.0.0)\n * Running on http://127.0.0.1:5000\n * Running on http://192.168.1.66:5000\nPress CTRL+C to quit
Copy
YES — perfect, that means you fixed the launch issue 🎉

You are now running it correctly from the project directory.

Next steps right now
Leave that terminal open (don’t close it).

Open http://127.0.0.1:5000

Click Start on dashboard (this starts detection worker).

Trigger a new battle from overworld.

Watch if count increments.

Quick sanity checks
Click +1 Manual once — if number changes, UI/state path is good.

If manual works but auto does not:

camera feed/ROI/phrases still need tuning

detector only increments when its battle conditions pass.

If you want, I’ll give you a final known-good config.yaml tuned for your Gen 3-style battle text so you can paste it and test immediately.

- [09/Apr/2026 16:21:10] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:11] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:11] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:11] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:12] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:12] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:13] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:13] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:13] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:14] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:14] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:15] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:15] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:15] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:16] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:16] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:16] "POST /api/stop HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:17] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:17] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:17] "POST /api/start HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:17] "GET /api/state HTTP/1.1" 200 -\nException in thread Thread-216 (detector_loop):\nTraceback (most recent call last):\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 275, in run_tesseract\n    proc = subprocess.Popen(cmd_args, **subprocess_args())\n  File "C:\Python313\Lib\subprocess.py", line 1038, in __init__\n    self._execute_child(args, executable, preexec_fn, close_fds,\n    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n                        pass_fds, cwd, env,\n                        ^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n                        gid, gids, uid, umask,\n                        ^^^^^^^^^^^^^^^^^^^^^^\n                        start_new_session, process_group)\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Python313\Lib\subprocess.py", line 1550, in _execute_child\n    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,\n                       ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n                             # no special security\n                             ^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n                             cwd,\n                             ^^^^\n                             startupinfo)\n                             ^^^^^^^^^^^^\nFileNotFoundError: [WinError 2] The system cannot find the file specified\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File "C:\Python313\Lib\threading.py", line 1041, in _bootstrap_inner\n    self.run()\n    ~~~~~~~~^^\n  File "C:\Python313\Lib\threading.py", line 992, in run\n    self._target(*self._args, **self._kwargs)\n    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\app.py", line 53, in detector_loop\n    if running and detector.detect_new_battle():\n                   ~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 99, in detect_new_battle\n    signal = self._ocr_hit(frame) or self._template_hit(frame)\n             ~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 76, in _ocr_hit\n    text = pytesseract.image_to_string(gray).lower()\n           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 486, in image_to_string\n    return {\n           ~\n    ...<2 lines>...\n        Output.STRING: lambda: run_and_get_output(*args),\n        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n    }[output_type]()\n    ~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 489, in <lambda>\n    Output.STRING: lambda: run_and_get_output(*args),\n                           ~~~~~~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 352, in run_and_get_output\n    run_tesseract(**kwargs)\n    ~~~~~~~~~~~~~^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 280, in run_tesseract\n    raise TesseractNotFoundError()\npytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH. See README file for more information.\n127.0.0.1 - - [09/Apr/2026 16:21:18] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:18] "GET /api/state HTTP/1.1" 200 -- [09/Apr/2026 16:21:10] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:11] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:11] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:11] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:12] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:12] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:13] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:13] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:13] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:14] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:14] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:15] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:15] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:15] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:16] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:16] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:16] "POST /api/stop HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:17] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:17] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:17] "POST /api/start HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:17] "GET /api/state HTTP/1.1" 200 -\nException in thread Thread-216 (detector_loop):\nTraceback (most recent call last):\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 275, in run_tesseract\n    proc = subprocess.Popen(cmd_args, **subprocess_args())\n  File "C:\Python313\Lib\subprocess.py", line 1038, in __init__\n    self._execute_child(args, executable, preexec_fn, close_fds,\n    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n                        pass_fds, cwd, env,\n                        ^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n                        gid, gids, uid, umask,\n                        ^^^^^^^^^^^^^^^^^^^^^^\n                        start_new_session, process_group)\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Python313\Lib\subprocess.py", line 1550, in _execute_child\n    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,\n                       ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n                             # no special security\n                             ^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n                             cwd,\n                             ^^^^\n                             startupinfo)\n                             ^^^^^^^^^^^^\nFileNotFoundError: [WinError 2] The system cannot find the file specified\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File "C:\Python313\Lib\threading.py", line 1041, in _bootstrap_inner\n    self.run()\n    ~~~~~~~~^^\n  File "C:\Python313\Lib\threading.py", line 992, in run\n    self._target(*self._args, **self._kwargs)\n    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\app.py", line 53, in detector_loop\n    if running and detector.detect_new_battle():\n                   ~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 99, in detect_new_battle\n    signal = self._ocr_hit(frame) or self._template_hit(frame)\n             ~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 76, in _ocr_hit\n    text = pytesseract.image_to_string(gray).lower()\n           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 486, in image_to_string\n    return {\n           ~\n    ...<2 lines>...\n        Output.STRING: lambda: run_and_get_output(*args),\n        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n    }[output_type]()\n    ~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 489, in <lambda>\n    Output.STRING: lambda: run_and_get_output(*args),\n                           ~~~~~~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 352, in run_and_get_output\n    run_tesseract(**kwargs)\n    ~~~~~~~~~~~~~^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\.venv\Lib\site-packages\pytesseract\pytesseract.py", line 280, in run_tesseract\n    raise TesseractNotFoundError()\npytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH. See README file for more information.\n127.0.0.1 - - [09/Apr/2026 16:21:18] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 16:21:18] "GET /api/state HTTP/1.1" 200 -
Copy
You’re absolutely right to paste that — this log gives a clear answer:

Root cause (confirmed)
Your local detector.py is still the old version.
I can tell because traceback hits:

detector.py, line 76, direct pytesseract.image_to_string(...)

and crashes with TesseractNotFoundError

In the patched version, OCR has a fallback/guard and tesseract_cmd support from config, so it wouldn’t crash at that exact point.

Fastest fix right now (manual, 30 seconds)
Open your local detector.py and add this line right under imports:

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
If import pytesseract already exists, just add the second line below it.

Then save and restart:

python app.py
This bypasses PATH entirely.

Why your config.yaml change didn’t work
Your current local app likely doesn’t include the newer loader field for ocr.tesseract_cmd yet, so it ignores that config key.
That support exists in the updated code, but not in the old file set you’re running.

Optional check to confirm you’re on old code
In PowerShell from project root:

Select-String -Path .\detector.py -Pattern "tesseract_cmd"
If no result, you’re on older code.

If result exists, then restart app and we’ll debug next layer.

You’re very close — once this single line is in your local detector.py, the crash loop should stop.

ok it is ticking up now thats great, the only issue no is too many things are getting acceted as the target words so its ticking more than it should the text before the fight start says Mew! can i add that word? but also i need the model to be mroe finetuned so i dont get so many FP
Copy
Amazing — great progress. ✅
And yes, you can absolutely add "mew" as a phrase.

You’re using a rule-based detector (OCR/template/motion), not a trained ML model yet, so false positives are reduced by tighter config, not model training right now.

Why you’re getting false positives
Your OCR logic currently does:

confidence = matched_phrases / total_phrases
then checks confidence >= ocr_min_confidence.

So with a low threshold, random text can pass too often.

Better “low false-positive” config
Use this as a starting point:

ocr:
  enabled: true
  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
  roi: [0.03, 0.73, 0.94, 0.24]   # tighter to dialogue box only
  phrases:
    - "mew"
    - "appeared"
  min_confidence: 1.0             # require BOTH words

detection:
  min_motion_score: 8.0           # raise to reduce random triggers

cooldown_seconds: 3.0             # avoid double ticks per encounter
poll_interval_ms: 120
Fields above are supported in your config loader/example.

If you still get FPs (strong recommendation)
Turn on template mode too (or even OCR off and template on), because template matching on a stable battle-start UI element is usually cleaner than OCR for pixel text:

template:
  enabled: true
  image_path: "C:\\path\\to\\battle_start_template.png"
  threshold: 0.90
Template checks are built into the same signal path.

Practical tuning order
Tighten ROI first

Raise min_confidence

Raise min_motion_score

Increase cooldown_seconds

Add template mode for final stability

If you want, I can give you a “super strict mew-only hunt profile” and a “general hunt profile” you can swap quickly.

# Copy this file to config.yaml and tune thresholds based on your game/capture feed.\ncamera_index: 2\npoll_interval_ms: 80\ncooldown_seconds: 1.0\n\n# OCR mode checks for expected battle text fragments.\nocr:\n  enabled: true\n  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"\n  roi: [0.05, 0.70, 0.90, 0.28]\n  phrases:\n    - "wild"\n    - "appeared"\n  min_confidence: 0.25\n\n# Template mode checks for visual match of a battle-start indicator image.\ntemplate:\n  enabled: false\n  image_path: ""\n  threshold: 0.88\n\n# Optional per-game encounter gating to prevent duplicate counts\n# when battle intro remains on-screen for multiple polling cycles.\ndetection:\n  motion_roi: [0.0, 0.0, 1.0, 1.0]\n  min_motion_score: 1.5\n
give me full new config with these changes
Copy
Perfect — here’s a full stricter config to reduce false positives and still catch Mew battle starts.

# Copy this file to config.yaml and tune thresholds based on your game/capture feed.
camera_index: 2
poll_interval_ms: 120
cooldown_seconds: 3.0

# OCR mode checks for expected battle text fragments.
ocr:
  enabled: true
  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
  # tighter ROI focused on dialogue text box
  roi: [0.03, 0.73, 0.94, 0.24]
  phrases:
    - "mew"
    - "appeared"
  # require both phrases to match (2/2)
  min_confidence: 1.0

# Template mode checks for visual match of a battle-start indicator image.
template:
  enabled: false
  image_path: ""
  threshold: 0.90

# Optional per-game encounter gating to prevent duplicate counts
# when battle intro remains on-screen for multiple polling cycles.
detection:
  motion_roi: [0.0, 0.0, 1.0, 1.0]
  min_motion_score: 8.0
After saving config.yaml, restart app:

python app.py
This uses the same supported keys your app already reads (camera_index, OCR fields, template fields, detection fields).

ok now it isnt ticking up at all anymore
Copy
Makes sense — we over-tightened it (too strict), so now it misses everything.

Let’s back it off to a balanced profile:

camera_index: 2
poll_interval_ms: 100
cooldown_seconds: 2.0

ocr:
  enabled: true
  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
  roi: [0.04, 0.71, 0.92, 0.27]
  phrases:
    - "mew"
    - "appeared"
    - "wild"
  min_confidence: 0.5

template:
  enabled: false
  image_path: ""
  threshold: 0.88

detection:
  motion_roi: [0.0, 0.0, 1.0, 1.0]
  min_motion_score: 3.5
Why this should work better
min_confidence: 0.5 = needs about half phrase hits, not all.

Motion threshold lowered from very strict.

Cooldown still prevents rapid duplicate spam.

(These are exactly the detection knobs your app uses.)

After saving:

restart python app.py

click Start

trigger a fresh encounter from overworld

If still missing, set just this one line lower:

ocr:
  min_confidence: 0.34
If still too many false positives, raise only:

detection:
  min_motion_score: 5.0
We’ll tune one knob at a time now (so it converges fast).

ok now it is not getting any positives even with removing one of the prashes and just havingappered and wld
Copy
Got it — at this point OCR is likely too unreliable on your feed/font scaling.

Best move now: switch to template-only detection
It’s way more stable for retro Pokémon battle starts.

BattleDetector already supports this with cv2.matchTemplate.

1) Make one template image
Take a screenshot of the exact battle-start moment (e.g. where the text box says ... appeared!), then crop a small unique area like:

the left side of the text box border + first word area

or a consistent HUD element present only at battle start

Save as:
C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\templates\battle_start.png

2) Use this config (template only)
camera_index: 2
poll_interval_ms: 80
cooldown_seconds: 2.0

ocr:
  enabled: false
  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
  roi: [0.04, 0.71, 0.92, 0.27]
  phrases:
    - "wild"
    - "appeared"
  min_confidence: 0.25

template:
  enabled: true
  image_path: "C:\\Users\\rcolt\\OneDrive\\Desktop\\AutoShinyCounter-main\\templates\\battle_start.png"
  threshold: 0.82

detection:
  motion_roi: [0.0, 0.0, 1.0, 1.0]
  min_motion_score: 3.0
(These keys are all supported by your app config loader.)

3) Restart and test
python app.py

Click Start

Trigger fresh encounters

If misses occur: lower template.threshold to 0.78
If false positives: raise to 0.86

If you want, I can show you exactly what to crop from your battle screenshot so the template hits cleanly and avoids random matches.

user attachment image
could i use this as the template instead? this is where id prefer it to tick the encounter because i can reset faster
Copy
Yes — that’s actually a good idea. ✅
You can trigger on the “Mew!” text box frame if that’s your preferred reset point.

Template matching will fire wherever your saved image appears in the feed.

How to make this work well
Crop a small, unique template from that frame (don’t use full screen):

include Mew! text + a bit of textbox border.

Save it as PNG (example):
C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\templates\mew_trigger.png

Use template mode (OCR off to avoid OCR noise).

camera_index: 2
poll_interval_ms: 80
cooldown_seconds: 2.0

ocr:
  enabled: false
  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
  roi: [0.04, 0.71, 0.92, 0.27]
  phrases:
    - "wild"
    - "appeared"
  min_confidence: 0.25

template:
  enabled: true
  image_path: "C:\\Users\\rcolt\\OneDrive\\Desktop\\AutoShinyCounter-main\\templates\\mew_trigger.png"
  threshold: 0.88

detection:
  motion_roi: [0.0, 0.0, 1.0, 1.0]
  min_motion_score: 2.0
Tuning
If it misses: lower threshold to 0.84

If false positives: raise to 0.91

If duplicate ticks: raise cooldown_seconds to 2.5–3.0

The detector still uses cooldown + motion + active-battle gating, which helps prevent repeat counts on the same encounter frame.

If you want, I can give you a “what exact rectangle to crop” guide on your screenshot so the template is maximally stable.

user attachment image
camera_index: 2\npoll_interval_ms: 80\ncooldown_seconds: 2.0\n\nocr:\n  enabled: false\n  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"\n  roi: [0.04, 0.71, 0.92, 0.27]\n  phrases:\n    - "wild"\n    - "appeared"\n  min_confidence: 0.25\n\ntemplate:\n  enabled: true\n  image_path: "C:\\Users\\rcolt\\OneDrive\\Desktop\\AutoShinyCounter-main\\templates\\mew_trigger.png"\n  threshold: 0.84\n\ndetection:\n  motion_roi: [0.0, 0.0, 1.0, 1.0]\n  min_motion_score: 2.0
still not ticking  i did this is this ok
Copy
You’re very close — that crop is likely too small and too sensitive to scaling/filter differences.

Your current 1-word template (Mew!) can fail if OBS/capture scales even slightly, because this matcher needs near pixel-exact shape at one scale.

What to change
1) Use a bigger template crop
Instead of just text, crop:

Mew!

plus left textbox border

plus some white box background

(about 2–3x larger than current crop)

2) First do a permissive test
Use this to confirm matching works at all:

template:
  enabled: true
  image_path: "C:\\Users\\rcolt\\OneDrive\\Desktop\\AutoShinyCounter-main\\templates\\mew_trigger.png"
  threshold: 0.70
detection:
  min_motion_score: 0.5
If it starts ticking, you know matching works — then raise threshold gradually to reduce false positives.

3) Verify template file actually loads
If path is wrong, template never loads (and signal is always false).
Detector only loads template if file exists at startup.

Run:

Test-Path "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\templates\mew_trigger.png"
Must be True.

4) Keep OBS/video scaling fixed
Template matching fails if feed scale changes between when you captured the template and when detector runs.

Why this happens
Signal requires _template_hit == True; otherwise no increment regardless of other settings.
And your matcher is single-scale only, so tiny template crops are fragile.

If you want, I can give you a “safe crop box” on your screenshot (exact region suggestion) that is much more likely to match consistently.

127.0.0.1 - - [09/Apr/2026 18:22:10] "GET /api/state HTTP/1.1" 200 -\nException in thread Thread-15 (detector_loop):\nTraceback (most recent call last):\n  File "C:\Python313\Lib\threading.py", line 1041, in _bootstrap_inner\n    self.run()\n    ~~~~~~~~^^\n  File "C:\Python313\Lib\threading.py", line 992, in run\n    self._target(*self._args, **self._kwargs)\n    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\app.py", line 53, in detector_loop\n    if running and detector.detect_new_battle():\n                   ~~~~~~~~~~~~~~~~~~~~~~~~~~^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 100, in detect_new_battle\n    signal = self._ocr_hit(frame) or self._template_hit(frame)\n                                     ~~~~~~~~~~~~~~~~~~^^^^^^^\n  File "C:\Users\rcolt\OneDrive\Desktop\AutoShinyCounter-main\detector.py", line 86, in _template_hit\n    result = cv2.matchTemplate(gray, self.template, cv2.TM_CCOEFF_NORMED)\ncv2.error: OpenCV(4.10.0) D:\a\opencv-python\opencv-python\opencv\modules\imgproc\src\templmatch.cpp:1175: error: (-215:Assertion failed) _img.size().height <= _templ.size().height && _img.size().width <= _templ.size().width in function 'cv::matchTemplate'\n\n127.0.0.1 - - [09/Apr/2026 18:22:10] "GET /api/state HTTP/1.1" 200 -\n127.0.0.1 - - [09/Apr/2026 18:22:11] "GET /api/state HTTP/1.1" 200 -
Copy
Summary
The crash you posted is a template-size mismatch in OpenCV (matchTemplate), which happens when the template image is larger than the current camera frame. I added a guard in BattleDetector to detect this condition and skip safely instead of crashing the detector thread.

Added a one-time warning message when template size is invalid so it’s clear what to fix (Use a smaller crop for template.image_path).

Added a defensive cv2.error catch around template matching so runtime errors don’t kill detection loop anymore.

Updated README template instructions to explicitly call out that template image must be smaller than captured frame resolution.

What you should do immediately on your machine:

Re-crop mew_trigger.png smaller (your current template is likely larger than the incoming feed at runtime).

Keep it to a tight unique patch (text + border) and ensure OBS/capture scale is fixed.

Restart python app.py after replacing the template.

Testing

✅ python -m compileall app.py detector.py state.py

Committed on current branch:

f72d6f9 — Guard template matching when template is larger than frame


Files (8)

README.md
README.md
New

app.py
app.py
New

config.example.yaml
config.example.yaml
New

detector.py
detector.py
New

requirements.txt
requirements.txt
New

state.py
state.py
New

index.html
templates/index.html
New

overlay.html
templates/overlay.html
New



Diff
Logs

README.md
README.md
New
+86
-0

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
  - `ocr.tesseract_cmd`: optional full path to `tesseract.exe` if PATH is not working
  - `ocr.roi`: portion of frame where battle text appears
  - `ocr.phrases`: fragments expected during battle intro (`wild`, `appeared`)
- Template mode:
  - `template.enabled: true` and set `template.image_path`
  - Use a cropped image of a consistent battle-start HUD element
  - Ensure template image is smaller than the captured frame resolution
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
app.py
app.py
New
+157
-0

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
        tesseract_cmd=cfg.get("ocr", {}).get("tesseract_cmd", ""),
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
config.example.yaml
config.example.yaml
New
+29
-0

# Copy this file to config.yaml and tune thresholds based on your game/capture feed.
camera_index: 0
poll_interval_ms: 250
cooldown_seconds: 3.0

# OCR mode checks for expected battle text fragments.
ocr:
  enabled: true
  # Optional explicit path for systems where tesseract is installed but not in PATH.
  # Windows example:
  # tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
  tesseract_cmd: ""
  roi: [0.05, 0.72, 0.90, 0.25] # x, y, w, h (relative to frame)
  phrases:
    - "wild"
    - "appeared"
  min_confidence: 0.55

# Template mode checks for visual match of a battle-start indicator image.
template:
  enabled: true
  image_path: ""
  threshold: 0.88

# Optional per-game encounter gating to prevent duplicate counts
# when battle intro remains on-screen for multiple polling cycles.
detection:
  motion_roi: [0.0, 0.0, 1.0, 1.0]
  min_motion_score: 12.0
detector.py
detector.py
New
+145
-0

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
requirements.txt
requirements.txt
New
+6
-0

Flask==3.1.0
opencv-python==4.10.0.84
numpy==2.1.3
pytesseract==0.3.13
Pillow==11.0.0
PyYAML==6.0.2
state.py
state.py
New
+46
-0

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
templates/index.html
templates/index.html
New
+68
-0

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Auto Shiny Tracker</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2rem; max-width: 900px; }
      .row { display: flex; gap: 2rem; align-items: flex-start; }
      .card { border: 1px solid #ddd; border-radius: 10px; padding: 1rem; flex: 1; }
      .value { font-size: 3rem; margin: 0.3rem 0; }
      button { margin-right: 0.5rem; }
      img { max-width: 280px; border-radius: 8px; border: 1px solid #ccc; }
      code { background: #f2f2f2; padding: 2px 4px; border-radius: 4px; }
    </style>
  </head>
  <body>
    <h1>Auto Shiny Tracker</h1>
    <p>Use <code>/overlay</code> in OBS Browser Source to display only the encounter widget.</p>

    <div class="row">
      <div class="card">
        <h2>{{ state.target_name or "Current Hunt" }}</h2>
        <p class="value" id="encounters">{{ state.encounters }}</p>
        <p>Status: <strong id="running">{{ "Running" if state.running else "Stopped" }}</strong></p>
        <p>Last Event (UTC): <span id="last_event">{{ state.last_event_at or "-" }}</span></p>
        <div>
          <button onclick="post('/api/start')">Start</button>
          <button onclick="post('/api/stop')">Stop</button>
          <button onclick="post('/api/increment')">+1 Manual</button>
          <button onclick="post('/api/reset')">Reset</button>
        </div>
      </div>
      <div class="card">
        <h3>Shiny Target</h3>
        {% if state.shiny_image_path %}
          <img src="{{ state.shiny_image_path }}" alt="target shiny" />
        {% else %}
          <p>No shiny image uploaded yet.</p>
        {% endif %}

        <form method="post" action="/api/target">
          <p><label>Target name <input name="target_name" placeholder="e.g. Shiny Charcadet" /></label></p>
          <button type="submit">Save target name</button>
        </form>

        <form method="post" action="/api/upload_shiny" enctype="multipart/form-data">
          <p><label>Upload shiny image <input name="shiny_image" type="file" accept="image/*" /></label></p>
          <button type="submit">Upload</button>
        </form>
      </div>
    </div>

    <script>
      async function post(path) {
        await fetch(path, { method: 'POST' });
      }

      async function refresh() {
        const res = await fetch('/api/state');
        const s = await res.json();
        document.getElementById('encounters').textContent = s.encounters;
        document.getElementById('running').textContent = s.running ? 'Running' : 'Stopped';
        document.getElementById('last_event').textContent = s.last_event_at || '-';
      }
      setInterval(refresh, 1000);
    </script>
  </body>
</html>
templates/overlay.html
templates/overlay.html
New
+46
-0

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Shiny Overlay</title>
    <style>
      body { margin: 0; background: transparent; font-family: Arial, sans-serif; }
      .overlay { color: white; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9); padding: 24px; }
      .count { font-size: 72px; font-weight: 700; }
      .target { font-size: 30px; margin-bottom: 8px; }
      img { margin-top: 12px; max-height: 220px; border-radius: 8px; }
    </style>
  </head>
  <body>
    <div class="overlay">
      <div class="target" id="target">{{ state.target_name or "Current Hunt" }}</div>
      <div class="count" id="count">{{ state.encounters }}</div>
      {% if state.shiny_image_path %}
      <img id="shiny" src="{{ state.shiny_image_path }}" alt="shiny target" />
      {% endif %}
    </div>

    <script>
      async function refresh() {
        const res = await fetch('/api/state');
        const s = await res.json();
        document.getElementById('count').textContent = s.encounters;
        document.getElementById('target').textContent = s.target_name || 'Current Hunt';

        const existing = document.getElementById('shiny');
        if (s.shiny_image_path && !existing) {
          const img = document.createElement('img');
          img.id = 'shiny';
          img.src = s.shiny_image_path;
          img.alt = 'shiny target';
          document.querySelector('.overlay').appendChild(img);
        } else if (s.shiny_image_path && existing && existing.src !== s.shiny_image_path) {
          existing.src = s.shiny_image_path;
        } else if (!s.shiny_image_path && existing) {
          existing.remove();
        }
      }
      setInterval(refresh, 1000);
    </script>
  </body>
</html>
