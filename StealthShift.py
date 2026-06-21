import asyncio
import io
import random
import json
import os
import shutil
import sys
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

PROFILES_DIR = "profiles"


def list_profiles():
    if not os.path.exists(PROFILES_DIR):
        return []
    return [d for d in os.listdir(PROFILES_DIR) if os.path.isdir(os.path.join(PROFILES_DIR, d))]


def save_profile(profile_name, data):
    profile_path = os.path.join(PROFILES_DIR, profile_name)
    os.makedirs(profile_path, exist_ok=True)
    with open(os.path.join(profile_path, "fingerprint.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Profile '{profile_name}' saved.")


def load_profile(profile_name):
    profile_path = os.path.join(PROFILES_DIR, profile_name, "fingerprint.json")
    if not os.path.exists(profile_path):
        return None
    with open(profile_path, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_profile(profile_name):
    profile_path = os.path.join(PROFILES_DIR, profile_name)
    if os.path.exists(profile_path):
        shutil.rmtree(profile_path)
        print(f"Profile '{profile_name}' deleted.")
        return True
    print(f"Profile '{profile_name}' not found.")
    return False


# finger print randomizer
def generate_random_data(proxy=None):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/149.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/149.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/149.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/149.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/149.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/149.0.0.0 Safari/537.36"
    ]

    selected_ua = random.choice(user_agents)

    if "Windows" in selected_ua:
        platform = "Win32"
    elif "Mac" in selected_ua:
        platform = "MacIntel"
    else:
        platform = "Linux x86_64"

    width = random.choice([1366, 1536, 1920, 2560])
    height = random.choice([768, 864, 1080, 1440])

    def detect_proxy_country(proxy_str):
        if not proxy_str:
            return None
        try:
            import re
            import urllib.request
            import json
            ip_match = re.search(r'@?(\d+\.\d+\.\d+\.\d+)', proxy_str)
            if ip_match:
                ip = ip_match.group(1)
                url = f"http://ip-api.com/json/{ip}"
                with urllib.request.urlopen(url, timeout=3) as response:
                    data = json.loads(response.read().decode())
                    if data.get('status') == 'success':
                        return data.get('countryCode')
        except:
            pass
        return None

    country_code = detect_proxy_country(proxy) if proxy else None

    country_lang_tz = {
        "US": {"lang": "en-US", "tz": "America/New_York", "accepted": ["en-US", "en"], "ui": "en"},
        "GB": {"lang": "en-GB", "tz": "Europe/London", "accepted": ["en-GB", "en-US", "en"], "ui": "en"},
        "DE": {"lang": "de-DE", "tz": "Europe/Berlin", "accepted": ["de-DE", "de", "en-US"], "ui": "de"},
        "FR": {"lang": "fr-FR", "tz": "Europe/Paris", "accepted": ["fr-FR", "fr", "en-US"], "ui": "fr"},
        "NL": {"lang": "nl-NL", "tz": "Europe/Amsterdam", "accepted": ["nl-NL", "nl", "en-US"], "ui": "nl"},
    }

    if country_code and country_code in country_lang_tz:
        lang_tz = country_lang_tz[country_code]
        selected_lang = lang_tz["lang"]
        selected_tz = lang_tz["tz"]
        accepted_languages = lang_tz["accepted"]
        ui_language = lang_tz["ui"]
    else:
        lang_tz_pairs = [
            {"lang": "en-US", "tz": "America/New_York", "accepted": ["en-US", "en"], "ui": "en"},
            {"lang": "tr-TR", "tz": "Europe/Istanbul", "accepted": ["tr-TR", "tr", "en-US"], "ui": "tr"},
            {"lang": "de-DE", "tz": "Europe/Berlin", "accepted": ["de-DE", "de", "en-US"], "ui": "de"},
            {"lang": "fr-FR", "tz": "Europe/Paris", "accepted": ["fr-FR", "fr", "en-US"], "ui": "fr"},
            {"lang": "es-ES", "tz": "Europe/Madrid", "accepted": ["es-ES", "es", "en-US"], "ui": "es"}
        ]

        selected = random.choice(lang_tz_pairs)
        selected_lang = selected["lang"]
        selected_tz = selected["tz"]
        accepted_languages = selected["accepted"]
        ui_language = selected["ui"]

    cpu_cores = random.choice([2, 4, 8, 16])
    ram_gb = random.choice([4, 8, 16, 32])
    touch_points = random.choice([0, 1])

    webgl_pairs = [
        ("NVIDIA Corporation", "ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0)"),
        ("NVIDIA Corporation", "ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Super Direct3D11 vs_5_0 ps_5_0)"),
        ("NVIDIA Corporation", "ANGLE (NVIDIA, NVIDIA GeForce RTX 4070 Direct3D11 vs_5_0 ps_5_0)"),
        ("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0, D3D11)"),
        ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0, D3D11)"),
        ("AMD", "ANGLE (AMD, AMD Radeon RX 6600 Direct3D11 vs_5_0 ps_5_0)"),
        ("AMD", "ANGLE (AMD, AMD Radeon RX 5700 XT Direct3D11 vs_5_0 ps_5_0)"),
        ("Intel Inc.", "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)"),
        ("Intel Inc.", "ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0)"),
    ]

    selected_pair = random.choice(webgl_pairs)
    selected_webgl_vendor = selected_pair[0]
    selected_webgl_renderer = selected_pair[1]

    canvas_noise = random.uniform(0.009, 0.01)
    audio_noise = random.uniform(0.0005, 0.001)

    plugins_list = [
        {"name": "Chrome PDF Plugin", "filename": "internal-pdf-viewer", "description": "Portable Document Format"},
        {"name": "Chrome PDF Viewer", "filename": "mhjfbmdgcfjbbpaeojofohoefgiehjai", "description": ""},
        {"name": "Native Client", "filename": "internal-nacl-plugin", "description": ""}
    ]

    font_list = [
        "Arial", "Arial Black", "Helvetica", "Times New Roman", "Courier New",
        "Verdana", "Georgia", "Trebuchet MS", "Impact", "Comic Sans MS",
        "Tahoma", "Palatino Linotype", "Lucida Console",
        "MS Sans Serif", "Calibri", "Cambria"
    ]
    random_fonts = random.sample(font_list, random.randint(6, 10))

    webgl2_capabilities = {
        "max_texture_size": random.choice([4096, 8192, 16384]),
        "max_vertex_attribs": random.choice([16, 24, 32]),
        "max_uniform_buffer_bindings": random.choice([32, 48, 64])
    }

    voice_count = random.randint(0, 5)
    available_languages = list(set(["tr-TR", "en-US", "de-DE", "fr-FR", "es-ES"]))
    random_supported_languages = random.sample(available_languages, random.randint(1, 3))

    permissions = {
        "geolocation": random.choice(["granted", "denied", "prompt"]),
        "notifications": random.choice(["granted", "denied", "prompt"]),
        "camera": random.choice(["granted", "denied", "prompt"]),
        "microphone": random.choice(["granted", "denied", "prompt"]),
        "midi": random.choice(["granted", "denied", "prompt"]),
        "clipboard-read": random.choice(["granted", "denied", "prompt"]),
        "clipboard-write": random.choice(["granted", "denied", "prompt"])
    }

    return {
        "ua": selected_ua,
        "width": width,
        "height": height,
        "lang": selected_lang,
        "accepted_languages": accepted_languages,
        "ui_language": ui_language,
        "tz": selected_tz,
        "platform": platform,
        "cpu": cpu_cores,
        "ram": ram_gb,
        "touch_points": touch_points,
        "webgl_vendor": selected_webgl_vendor,
        "webgl_renderer": selected_webgl_renderer,
        "canvas_noise": canvas_noise,
        "audio_noise": audio_noise,
        "plugins": plugins_list,
        "fonts": random_fonts,
        "webgl2": webgl2_capabilities,
        "speech_languages": random_supported_languages,
        "speech_voice_count": voice_count,
        "permissions": permissions
    }


def generate_stealth_js(data):
    ua = data["ua"]
    platform = data.get("platform", "Win32")
    lang_primary = data.get("lang", "en-US")
    languages = data.get("accepted_languages", [lang_primary, "en"])
    lang = languages[0]
    canvas_noise = data.get("canvas_noise", 0.002)
    webgl_vendor = data.get("webgl_vendor", "NVIDIA Corporation")
    webgl_renderer = data.get("webgl_renderer", "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)")
    cpu = data.get("cpu", 4)
    ram = data.get("ram", 8)
    touch_points = data.get("touch_points", 0)
    width = data.get("width", 1920)
    height = data.get("height", 1080)

    plugins_list = data.get("plugins", [
        {"name": "Chrome PDF Plugin", "filename": "internal-pdf-viewer", "description": "Portable Document Format"},
        {"name": "Chrome PDF Viewer", "filename": "mhjfbmdgcfjbbpaeojofohoefgiehjai", "description": ""},
        {"name": "Native Client", "filename": "internal-nacl-plugin", "description": ""}
    ])

    languages_json = json.dumps(languages)
#so tbh ONLY THIS partf of the program is taken from ai, im ngl i couldnt deal w this
    js_code = f"""
    (function() {{
        // navigator overrides
        Object.defineProperty(navigator, 'userAgent', {{get: () => '{ua}'}});
        Object.defineProperty(navigator, 'appVersion', {{get: () => '{ua}'}});
        Object.defineProperty(navigator, 'platform', {{get: () => '{platform}'}});
        Object.defineProperty(navigator, 'languages', {{get: () => {languages_json}}});
        Object.defineProperty(navigator, 'language', {{get: () => '{lang}'}});
        Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
        Object.defineProperty(navigator, 'hardwareConcurrency', {{get: () => {cpu}}});
        Object.defineProperty(navigator, 'deviceMemory', {{get: () => {ram}}});
        Object.defineProperty(navigator, 'maxTouchPoints', {{get: () => {touch_points}}});

        // screen dimensions
        Object.defineProperty(screen, 'width', {{get: () => {width}}});
        Object.defineProperty(screen, 'height', {{get: () => {height}}});
        Object.defineProperty(screen, 'availWidth', {{get: () => {width}}});
        Object.defineProperty(screen, 'availHeight', {{get: () => {height - 40}}});

        if (!window.chrome) window.chrome = {{}};
        window.chrome.runtime = {{}};
        window.chrome.app = {{}};
        window.chrome.csi = function() {{ return {{}}; }};
        window.chrome.loadTimes = function() {{ return {{}}; }};

        // plugin list
        const pluginData = {json.dumps(plugins_list)};

        function PluginArray() {{}}
        PluginArray.prototype = {{
            length: pluginData.length,
            item: function(i) {{ return this[i]; }},
            namedItem: function(name) {{
                for (let i = 0; i < this.length; i++) {{
                    if (this[i].name === name) return this[i];
                }}
                return null;
            }}
        }};

        const plugins = new PluginArray();

        for (let i = 0; i < pluginData.length; i++) {{
            const p = pluginData[i];
            const plugin = {{
                name: p.name,
                filename: p.filename,
                description: p.description,
                length: 1
            }};
            plugin[0] = {{
                type: 'application/pdf',
                suffixes: 'pdf',
                description: '',
                enabledPlugin: plugin
            }};
            plugins[i] = plugin;
        }}

        Object.defineProperty(navigator, 'plugins', {{get: () => plugins}});

        // mime types stub
        Object.defineProperty(navigator, 'mimeTypes', {{get: () => ({{ length: 1 }})}});

        // webgl vendor/renderer spoof
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {{
            if (parameter === 37445) return '{webgl_vendor}';
            if (parameter === 37446) return '{webgl_renderer}';
            return getParameter.call(this, parameter);
        }};

        const originalGetExtension = WebGLRenderingContext.prototype.getExtension;
        WebGLRenderingContext.prototype.getExtension = function(name) {{
            if (name === 'WEBGL_debug_renderer_info') {{
                return {{
                    getParameter: function(param) {{
                        if (param === 37445) return '{webgl_vendor}';
                        if (param === 37446) return '{webgl_renderer}';
                        return null;
                    }}
                }};
            }}
            return originalGetExtension.call(this, name);
        }};

        function applyCanvasNoise(imageData) {{
            const data = imageData.data;
            const noiseLevel = {canvas_noise} * 255;
            for (let i = 0; i < data.length; i += 4) {{
                data[i]     = Math.min(255, Math.max(0, data[i]     + (Math.random() * 2 - 1) * noiseLevel));
                data[i + 1] = Math.min(255, Math.max(0, data[i + 1] + (Math.random() * 2 - 1) * noiseLevel));
                data[i + 2] = Math.min(255, Math.max(0, data[i + 2] + (Math.random() * 2 - 1) * noiseLevel));
            }}
            return imageData;
        }}

        const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function(type, quality) {{
            try {{
                const ctx = this.getContext('2d');
                if (ctx) {{
                    const imageData = ctx.getImageData(0, 0, this.width, this.height);
                    ctx.putImageData(applyCanvasNoise(imageData), 0, 0);
                }}
            }} catch(e) {{}}
            return originalToDataURL.call(this, type, quality);
        }};

        const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
        CanvasRenderingContext2D.prototype.getImageData = function(sx, sy, sw, sh) {{
            const imageData = originalGetImageData.call(this, sx, sy, sw, sh);
            return applyCanvasNoise(imageData);
        }};

        console.log('[stealth] ready, noise={canvas_noise}');
    }})();
    """

    return js_code


# profile launchh with data
async def start_browser(data, profile_name=None, proxy=None):
    stealth_js = generate_stealth_js(data)

    async with async_playwright() as p:
        _lang = data.get('lang', 'en-US')
        _accepted = data.get('accepted_languages', [_lang])
        _ui_lang = data.get('ui_language', _lang.split('-')[0])
        _tz = data.get('tz', 'America/New_York')
#if any of these parameters are non-needed, i found these on overflow
        args = [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            f'--user-agent={data["ua"]}',
            f'--lang={_lang}',
            f'--accept-lang={_accepted[0]}',
            f'--ui-language={_ui_lang}',
            '--disable-component-extensions-with-background-pages',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-sync',
            '--disable-domain-reliability',
        ]

        if proxy:
            args.append(f'--proxy-server={proxy}')

        browser = await p.chromium.launch(headless=False, args=args)

        context = await browser.new_context(
            viewport={'width': data.get('width', 1920), 'height': data.get('height', 1080)},
            locale=_lang,
            timezone_id=_tz
        )

        await context.add_init_script(stealth_js)
        page = await context.new_page()
        await page.goto('https://browserleaks.com')

        print("\n" + "=" * 70)
        print(" STEALTHSHIFT - FINGERPRINT BROWSER")
        if profile_name:
            print(f"Profile: {profile_name}")
        print("=" * 70)
        print(f"User-Agent       : {data['ua']}")
        print(f"Window           : {data['width']}x{data['height']}")
        print(f"Language         : {data.get('lang','?')} (UI: {data.get('ui_language','?')})")
        print(f"Time Zone        : {data.get('tz','?')}")
        print(f"Platform         : {data.get('platform','?')}")
        print(f"CPU Cores        : {data.get('cpu','?')}")
        print(f"RAM              : {data.get('ram','?')} GB")
        print(f"WebGL Vendor     : {data.get('webgl_vendor','?')}")
        print(f"WebGL Renderer   : {data.get('webgl_renderer','?')}")
        print(f"Canvas Noise     : {data.get('canvas_noise',0):.6f}")
        print(f"Audio Noise      : {data.get('audio_noise',0):.6f}")
        print(f"Touch Support    : {'Yes' if data.get('touch_points') else 'No'}")
        print(f"Fonts            : {', '.join(data.get('fonts',[]))}")
        print(f"Plugins Count    : {len(data.get('plugins',[]))}")
        print(f"Speech Voices    : {data.get('speech_voice_count','?')}")
        print("\nBrowser is running. Close the window to exit.\n")

        try:
            while True:
                try:
                    await page.wait_for_event('close', timeout=1000)
                    break
                except:
                    if page.is_closed():
                        break
                    await asyncio.sleep(1)

            print("\nBrowser window closed.")
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
        finally:
            await browser.close()
            print("Browser closed.")


#menu
def main_menu():
    print("\n" + "=" * 50)
    print("STEALTHSHIFT - PROFILE MANAGER")
    print("=" * 50)
    print("1. Create & run new random profile")
    print("2. Load existing profile")
    print("3. List profiles")
    print("4. Delete profile")
    print("5. Exit")
    print("=" * 50)


def select_profile():
    profiles = list_profiles()
    if not profiles:
        print("No profiles found. Create one first.")
        return None

    print("\nSaved profiles:")
    for i, p in enumerate(profiles, 1):
        print(f"   {i}. {p}")

    try:
        choice = int(input("Select profile number (0 cancel): "))
        if choice == 0:
            return None
        return profiles[choice - 1]
    except:
        print("Invalid selection.")
        return None


async def main():
    while True:
        main_menu()
        choice = input("Your choice: ").strip()

        if choice == "1":
            proxy = input("Proxy (optional): ").strip() or None
            data = generate_random_data(proxy)

            profile_name = input("Profile name (leave empty for auto): ").strip()
            if not profile_name:
                profile_name = f"profile_{len(list_profiles())+1}_{random.randint(100,999)}"

            save_profile(profile_name, data)
            await start_browser(data, profile_name, proxy)

        elif choice == "2":
            profile_name = select_profile()
            if profile_name:
                data = load_profile(profile_name)
                if data:
                    proxy = input("Proxy (optional): ").strip() or None
                    await start_browser(data, profile_name, proxy)
                else:
                    print(f"Profile '{profile_name}' could not be loaded.")

        elif choice == "3":
            profiles = list_profiles()
            if profiles:
                print("\nSaved profiles:")
                for p in profiles:
                    print(f"   - {p}")
            else:
                print("No profiles found.")

        elif choice == "4":
            profile_name = select_profile()
            if profile_name:
                confirm = input(f"Delete '{profile_name}'? (y/n): ")
                if confirm.lower() == 'y':
                    delete_profile(profile_name)

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")


#this is for electron dont eveb pay attention, im still working on electron
if __name__ == "__main__":
    import sys
    import asyncio
    import json

    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            profiles = list_profiles()
            output = []

            for profile_name in profiles:
                data = load_profile(profile_name)
                if data:
                    output.append({
                        "name": profile_name,
                        "ua": data.get("ua", "Unknown")[:60],
                        "lang": data.get("lang", "Unknown"),
                        "tz": data.get("tz", "Unknown")
                    })

            print(json.dumps(output, ensure_ascii=False))

        elif sys.argv[1] == "--open" and len(sys.argv) > 2:
            profile_name = sys.argv[2]
            data = load_profile(profile_name)

            if data:
                asyncio.run(start_browser(data, profile_name))
            else:
                print(f"Profile '{profile_name}' not found.")

        elif sys.argv[1] == "--create" and len(sys.argv) > 2:
            profile_name = sys.argv[2]
            proxy = sys.argv[3] if len(sys.argv) > 3 else None

            data = generate_random_data(proxy)
            save_profile(profile_name, data)
            print(json.dumps({"status": "ok", "name": profile_name}))

        elif sys.argv[1] == "--delete" and len(sys.argv) > 2:
            profile_name = sys.argv[2]

            if delete_profile(profile_name):
                print(json.dumps({"status": "ok", "name": profile_name}))
            else:
                print(json.dumps({"status": "error", "message": "Profile not found"}))

        else:
            print("Usage:")
            print("  --list                 List profiles")
            print("  --open <name>          Open profile")
            print("  --create <name>        Create profile")
            print("  --delete <name>        Delete profile")
    else:
        asyncio.run(main())
