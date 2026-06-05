# StealthShift
I`m still working on this project, so do not expect a fully non-detected browser, but this is a good alternative to paid ones.
Feel free to make a pull request

[Python 3.9+] | [MIT License] | Windows / Linux

StealthShift is a FREE, open-source antidetect browser that randomises your browser fingerprint to bypass tracking, captchas and bot detection. It is a privacy-focused alternative to commercial tools like Dolphin Antidetect.

> **Disclaimer**  
> This software is provided for **educational purposes only**. Automating web browsers may violate the Terms of Service of some websites. Use it at your own risk.

---

## Features

**Full Fingerprint Randomisation**
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

**Profile Management**
- Create, save, load and delete profiles
- Each profile stores its own fingerprint in a local JSON file
- Unlimited profiles (only limited by your disk space)

**Proxy Support**
- HTTP / HTTPS / SOCKS5 proxies per profile (optional)

**Stealth Mode**
- Hides navigator.webdriver
- Adds real-looking window.chrome object
- Spoofs WebGL debug extension
- Provides fake plugin and mimeType lists

**Two Interfaces**
- Terminal menu for quick control
- Modern desktop UI built with Electron (ocean theme)

**Completely Free & Open Source**
- No subscriptions
- No cloud storage
- Your data stays on YOUR machine

---

## How It Works

StealthShift intercepts JavaScript APIs before the page loads. It overrides:

- **navigator.userAgent** → Random Windows / Mac / Linux, Chrome 148
- **navigator.platform** → Win32, MacIntel or Linux x86_64
- **navigator.languages** → Matches selected locale (or proxy country)
- **Intl.DateTimeFormat** → Timezone matched with language
- **screen.width / height** → Random common resolution
- **WebGLRenderingContext.getParameter** → NVIDIA vendor + random RTX model
- **WEBGL_debug_renderer_info** → Same spoofed GPU data
- **HTMLCanvasElement.toDataURL** → Tiny random noise (red channel only)
- **AudioBuffer.getChannelData** → Minimal random noise
- **navigator.plugins** → Fake Chrome PDF / Native Client plugins
- **navigator.webdriver** → undefined

All randomised values are generated when a profile is created and saved to:
`profiles/<profile_name>/fingerprint.json`

You can edit that file to manually adjust any fingerprint component.

---

## Quick Start

**Prerequisites**
- Python 3.9 or higher
- (optional) Node.js and npm – for the Electron UI
- A Chromium-based browser (Chrome, Brave, Edge) – auto-detected
- **For Electron UI (desktop application):**

1. Install Node.js from https://nodejs.org/ (if not already installed)
2. Run these commands in the project folder:
npm install
npm start

**Installation**

1. Clone the repository
git clone https://github.com/Sasorii-sc/StealthShift.git
cd StealthShift

text

2. Install the only required Python library
pip install playwright

text

3. Install Playwright's Chromium
playwright install chromium

text

4. (Optional) Install Electron dependencies for the UI
npm install

text

**Running StealthShift**

Terminal mode (no UI):
python StealthShift.py

text

You will see a menu:

==================================================
STEALTHSHIFT - PROFILE MANAGEMENT
==================================================
1. Create and open new profile (random)
2. Load and open saved profile
3. List saved profiles
4. Delete profile
5. Exit

========================================

Electron UI mode:
npm start

text

The UI shows all saved profiles as cards. You can:
- Click "New Profile" – enter a name, optionally a proxy
- Click on any profile card – launches a spoofed browser
- Click the red "Delete" button to remove a profile

Both modes use the same profile storage.

---

## Configuration

**Manual Fingerprint Tuning**

Open `profiles/your_profile_name/fingerprint.json` with any text editor. You can change any value, for example:

- `"ua"` – User-Agent string
- `"tz"` – timezone (e.g. Europe/Istanbul)
- `"webgl_renderer"` – GPU renderer string
- `"canvas_noise"` – noise intensity (0.0 ... 0.05)

**Proxy Format**

When creating a profile you will be asked for a proxy. Use these formats:

- HTTP:   `http://user:pass@ip:port`
- HTTPS:  `https://user:pass@ip:port`
- SOCKS5: `socks5://user:pass@ip:port`

Leave empty to use your direct connection.

---

## Testing Your Fingerprint

Check how well StealthShift hides your real identity at:

- browserleaks.com
- creepjs.com
- amiunique.org

> Note: Headless detection is reduced to about 33% – comparable to many commercial antidetect browsers. Perfect 0% headless is very hard to achieve with unmodified Playwright/Chromium.

---

## Project Structure
StealthShift/
├── StealthShift.py # Main Python backend
├── main.js # Electron main process
├── index.html # Electron UI (ocean theme)
├── package.json # Node.js dependencies
├── requirements.txt # Only "playwright"
├── .gitignore # Ignores profiles/, node_modules/
├── profiles/ # Your saved profiles (created at runtime)
└── README.md

text

---

## Contributing

Issues and pull requests are welcome. Please keep the code simple and the dependencies minimal.

---

## License

MIT License – see the LICENSE file for details.

---

## Author

Sasori (Sasorii-sc)

---

*Made for privacy research and automation testing – free as in freedom.*
