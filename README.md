# StealthShift
Still working on this, do not expect a full non-undetected browser for now.
[Python 3.9+] | [MIT License] | Windows / Linux

StealthShift is a FREE, open-source antidetect browser that randomises your browser fingerprint to bypass tracking, captchas and bot detection. It is a privacy-focused alternative to commercial tools like Dolphin Antidetect.

IMPORTANT DISCLAIMER
This software is provided for EDUCATIONAL PURPOSES ONLY. Automating web browsers may violate the Terms of Service of some websites. Use it at your own risk.

================================================================================
FEATURES
================================================================================

FULL FINGERPRINT RANDOMISATION
- User-Agent (random Windows, Mac, Linux with Chrome 148)
- Platform (Win32, MacIntel, Linux x86_64)
- Language and timezone (matching pairs or proxy-based)
- Screen resolution
- WebGL vendor/renderer (NVIDIA GPUs with random RTX models)
- Canvas noise (only red channel, low intensity)
- Audio noise (low intensity)
- Hardware concurrency (2,4,8,16 cores)
- Device memory (4,8,16,32 GB)
- Fake Chrome plugins and mimeTypes
- Spoofed WebGL debug extension (WEBGL_debug_renderer_info)

PROFILE MANAGEMENT
- Create, save, load and delete profiles
- Each profile stores its own fingerprint in a local JSON file
- Unlimited profiles (only limited by your disk space)

PROXY SUPPORT
- HTTP / HTTPS / SOCKS5 proxies per profile (optional)

STEALTH MODE
- Hides navigator.webdriver
- Adds real-looking window.chrome object
- Spoofs WebGL debug extension
- Provides fake plugin and mimeType lists

TWO INTERFACES
- Terminal menu for quick control
- Modern desktop UI built with Electron (ocean theme)

COMPLETELY FREE & OPEN SOURCE
- No subscriptions
- No cloud storage
- Your data stays on YOUR machine

================================================================================
HOW IT WORKS
================================================================================

StealthShift intercepts JavaScript APIs before the page loads. It overrides:

API / Property                Spoofed value
----------------------------- --------------------------------------------------
navigator.userAgent           Random Windows / Mac / Linux, Chrome 148
navigator.platform            Win32, MacIntel or Linux x86_64
navigator.languages           Matches selected locale (or proxy country)
Intl.DateTimeFormat           Timezone matched with language
screen.width / height         Random common resolution
WebGLRenderingContext.getParameter   NVIDIA vendor + random RTX model
WEBGL_debug_renderer_info     Same spoofed GPU data
HTMLCanvasElement.toDataURL   Tiny random noise (red channel only)
AudioBuffer.getChannelData    Minimal random noise
navigator.plugins             Fake Chrome PDF / Native Client plugins
navigator.webdriver           undefined

All randomised values are generated when a profile is created and saved to:
profiles/<profile_name>/fingerprint.json

You can edit that file to manually adjust any fingerprint component.

================================================================================
QUICK START
================================================================================

PREREQUISITES
- Python 3.9 or higher
- (optional) Node.js and npm – for the Electron UI
- A Chromium-based browser (Chrome, Brave, Edge) – auto-detected

INSTALLATION

1. Clone the repository
   git clone https://github.com/Sasorii-sc/StealthShift.git
   cd StealthShift

2. Install the only required Python library
   pip install playwright

3. Install Playwright's Chromium
   playwright install chromium

4. (Optional) Install Electron dependencies for the UI
   npm install

RUNNING STEALTHSHIFT

Terminal mode (no UI)
   python StealthShift.py

You will see a menu:

   ==================================================
   STEALTHSHIFT - PROFILE MANAGEMENT
   ==================================================
   1. Create and open new profile (random)
   2. Load and open saved profile
   3. List saved profiles
   4. Delete profile
   5. Exit
   ==================================================

Electron UI mode
   npm start

The UI shows all saved profiles as cards. You can:
- Click "New Profile" – enter a name, optionally a proxy
- Click on any profile card – launches a spoofed browser
- Click the red "Delete" button to remove a profile

Both modes use the same profile storage.

================================================================================
CONFIGURATION
================================================================================

MANUAL FINGERPRINT TUNING

Open profiles/your_profile_name/fingerprint.json with any text editor. You can change any value, for example:

- "ua" – User-Agent string
- "tz" – timezone (e.g. Europe/Istanbul)
- "webgl_renderer" – GPU renderer string
- "canvas_noise" – noise intensity (0.0 ... 0.05)

PROXY FORMAT

When creating a profile you will be asked for a proxy. Use these formats:

- HTTP:   http://user:pass@ip:port
- HTTPS:  https://user:pass@ip:port
- SOCKS5: socks5://user:pass@ip:port

Leave empty to use your direct connection.

================================================================================
TESTING YOUR FINGERPRINT
================================================================================

Check how well StealthShift hides your real identity at:

- browserleaks.com
- creepjs.com
- amiunique.org

Note: Headless detection is reduced to about 33% – comparable to many commercial antidetect browsers. Perfect 0% headless is very hard to achieve with unmodified Playwright/Chromium.

================================================================================
PROJECT STRUCTURE
================================================================================

StealthShift/
├── StealthShift.py       # Main Python backend (profile & browser logic)
├── main.js               # Electron main process
├── index.html            # Electron UI (ocean theme)
├── package.json          # Node.js dependencies
├── requirements.txt      # Only "playwright"
├── .gitignore            # Ignores profiles/, node_modules/, etc.
├── profiles/             # Your saved profiles (created at runtime)
└── README.md

================================================================================
CONTRIBUTING
================================================================================

Issues and pull requests are welcome. Please keep the code simple and the dependencies minimal.

================================================================================
LICENSE
================================================================================

MIT License – see the LICENSE file for details.

================================================================================
AUTHOR
================================================================================

Sasori (Sasorii-sc)

================================================================================

Made for privacy research and automation testing – free as in freedom.
