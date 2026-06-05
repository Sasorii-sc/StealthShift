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

def profilleri_listele():
    if not os.path.exists(PROFILES_DIR):
        return []
    return [d for d in os.listdir(PROFILES_DIR) if os.path.isdir(os.path.join(PROFILES_DIR, d))]

def profil_kaydet(profil_adi, veri):
    profil_yolu = os.path.join(PROFILES_DIR, profil_adi)
    os.makedirs(profil_yolu, exist_ok=True)
    with open(os.path.join(profil_yolu, "fingerprint.json"), "w", encoding="utf-8") as f:
        json.dump(veri, f, indent=4, ensure_ascii=False)
    print(f"Profil '{profil_adi}' kaydedildi.")

def profil_yukle(profil_adi):
    profil_yolu = os.path.join(PROFILES_DIR, profil_adi, "fingerprint.json")
    if not os.path.exists(profil_yolu):
        return None
    with open(profil_yolu, "r", encoding="utf-8") as f:
        return json.load(f)

def profil_sil(profil_adi):
    profil_yolu = os.path.join(PROFILES_DIR, profil_adi)
    if os.path.exists(profil_yolu):
        shutil.rmtree(profil_yolu)
        print(f"Profil '{profil_adi}' silindi.")
        return True
    print(f"Profil '{profil_adi}' bulunamadi.")
    return False

# -------------------- RASTGELE VERİLER --------------------
def rastgele_veriler(proxy=None):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36"
    ]
    secilen_ua = random.choice(user_agents)

    if "Windows" in secilen_ua:
        platform = "Win32"
    elif "Mac" in secilen_ua:
        platform = "MacIntel"
    else:
        platform = "Linux x86_64"

    genislik = random.choice([1366, 1536, 1920, 2560])
    yukseklik = random.choice([768, 864, 1080, 1440])

    def proxy_ulke_bul(proxy_str):
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

    ulke_kodu = proxy_ulke_bul(proxy) if proxy else None
    
    ulke_dil_tz = {
        "TR": {"lang": "tr-TR", "tz": "Europe/Istanbul", "accepted": ["tr-TR", "tr", "en-US"], "ui": "tr"},
        "US": {"lang": "en-US", "tz": "America/New_York", "accepted": ["en-US", "en"], "ui": "en"},
        "GB": {"lang": "en-GB", "tz": "Europe/London", "accepted": ["en-GB", "en-US", "en"], "ui": "en"},
        "DE": {"lang": "de-DE", "tz": "Europe/Berlin", "accepted": ["de-DE", "de", "en-US"], "ui": "de"},
        "FR": {"lang": "fr-FR", "tz": "Europe/Paris", "accepted": ["fr-FR", "fr", "en-US"], "ui": "fr"},
        "ES": {"lang": "es-ES", "tz": "Europe/Madrid", "accepted": ["es-ES", "es", "en-US"], "ui": "es"},
        "IT": {"lang": "it-IT", "tz": "Europe/Rome", "accepted": ["it-IT", "it", "en-US"], "ui": "it"},
        "NL": {"lang": "nl-NL", "tz": "Europe/Amsterdam", "accepted": ["nl-NL", "nl", "en-US"], "ui": "nl"},
    }
    
    if ulke_kodu and ulke_kodu in ulke_dil_tz:
        dil_tz = ulke_dil_tz[ulke_kodu]
        secilen_dil = dil_tz["lang"]
        secilen_tz = dil_tz["tz"]
        kabul_diller = dil_tz["accepted"]
        ui_dili = dil_tz["ui"]
    else:
        dil_tz_pairs = [
            {"lang": "en-US", "tz": "America/New_York", "accepted": ["en-US", "en"], "ui": "en"},
            {"lang": "tr-TR", "tz": "Europe/Istanbul", "accepted": ["tr-TR", "tr", "en-US"], "ui": "tr"},
            {"lang": "de-DE", "tz": "Europe/Berlin", "accepted": ["de-DE", "de", "en-US"], "ui": "de"},
            {"lang": "fr-FR", "tz": "Europe/Paris", "accepted": ["fr-FR", "fr", "en-US"], "ui": "fr"},
            {"lang": "es-ES", "tz": "Europe/Madrid", "accepted": ["es-ES", "es", "en-US"], "ui": "es"}
        ]
        secili = random.choice(dil_tz_pairs)
        secilen_dil = secili["lang"]
        secilen_tz = secili["tz"]
        kabul_diller = secili["accepted"]
        ui_dili = secili["ui"]

    cpu_cekirdekleri = random.choice([2, 4, 8, 16])
    ram_gb = random.choice([4, 8, 16, 32])
    dokunma_noktasi = random.choice([0, 1])

    webgl_vendor_list = ["NVIDIA Corporation"]
    webgl_renderer_list = [
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 4060 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 4070 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 4080 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 4090 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 1660 Direct3D11 vs_5_0 ps_5_0)",
    ]
    secilen_webgl_vendor = random.choice(webgl_vendor_list)
    secilen_webgl_renderer = random.choice(webgl_renderer_list)

    canvas_gurultu = random.uniform(0.001, 0.005)   # düşük gürültü, dengeli
    audio_gurultu = random.uniform(0.0005, 0.001)

    eklentiler = [
        {"name": "Chrome PDF Plugin", "filename": "internal-pdf-viewer", "description": "Portable Document Format"},
        {"name": "Chrome PDF Viewer", "filename": "mhjfbmdgcfjbbpaeojofohoefgiehjai", "description": ""},
        {"name": "Native Client", "filename": "internal-nacl-plugin", "description": ""}
    ]

    font_listesi = ["Arial", "Helvetica", "Times New Roman", "Courier New", "Verdana", "Georgia", "Comic Sans MS"]
    rastgele_fontlar = random.sample(font_listesi, random.randint(5, 7))

    webgl2_capabilities = {
        "max_texture_size": random.choice([4096, 8192, 16384]),
        "max_vertex_attribs": random.choice([16, 24, 32]),
        "max_uniform_buffer_bindings": random.choice([32, 48, 64])
    }

    ses_sayisi = random.randint(0, 5)
    mevcut_diller = list(set(["tr-TR", "en-US", "de-DE", "fr-FR", "es-ES"]))
    rastgele_desteklenen_diller = random.sample(mevcut_diller, random.randint(1, 3))

    batarya_seviyesi = random.uniform(0.05, 1.0)
    sarj_ediliyor = random.choice([True, False])
    sarj_suresi = random.randint(0, 3600) if sarj_ediliyor else random.randint(0, 7200)
    desarj_suresi = random.randint(0, 7200) if not sarj_ediliyor else random.randint(0, 3600)

    izinler = {
        "geolocation": random.choice(["granted", "denied", "prompt"]),
        "notifications": random.choice(["granted", "denied", "prompt"]),
        "camera": random.choice(["granted", "denied", "prompt"]),
        "microphone": random.choice(["granted", "denied", "prompt"]),
        "midi": random.choice(["granted", "denied", "prompt"]),
        "clipboard-read": random.choice(["granted", "denied", "prompt"]),
        "clipboard-write": random.choice(["granted", "denied", "prompt"])
    }

    return {
        "ua": secilen_ua,
        "width": genislik,
        "height": yukseklik,
        "dil": secilen_dil,
        "kabul_diller": kabul_diller,
        "ui_dili": ui_dili,
        "tz": secilen_tz,
        "platform": platform,
        "cpu": cpu_cekirdekleri,
        "ram": ram_gb,
        "dokunma": dokunma_noktasi,
        "webgl_vendor": secilen_webgl_vendor,
        "webgl_renderer": secilen_webgl_renderer,
        "canvas_noise": canvas_gurultu,
        "audio_noise": audio_gurultu,
        "plugins": eklentiler,
        "fonts": rastgele_fontlar,
        "webgl2": webgl2_capabilities,
        "speech_languages": rastgele_desteklenen_diller,
        "speech_voice_count": ses_sayisi,
        "battery_level": batarya_seviyesi,
        "battery_charging": sarj_ediliyor,
        "battery_charging_time": sarj_suresi,
        "battery_discharging_time": desarj_suresi,
        "permissions": izinler
    }

# -------------------- STEALTH JS (GELİŞMİŞ PLUGIN + WEBGL + CANVAS) --------------------
def generate_stealth_js(veri):
    ua = veri["ua"]
    platform = veri["platform"]
    languages = veri["kabul_diller"]
    lang = languages[0]
    canvas_noise = veri["canvas_noise"]
    webgl_vendor = veri["webgl_vendor"]
    webgl_renderer = veri["webgl_renderer"]
    cpu = veri["cpu"]
    ram = veri["ram"]
    dokunma = veri["dokunma"]
    width = veri["width"]
    height = veri["height"]
    
    languages_json = json.dumps(languages)
    
    js_code = f"""
    (function() {{
        // -------------------- NAVIGATOR --------------------
        Object.defineProperty(navigator, 'userAgent', {{get: () => '{ua}'}});
        Object.defineProperty(navigator, 'appVersion', {{get: () => '{ua}'}});
        Object.defineProperty(navigator, 'platform', {{get: () => '{platform}'}});
        Object.defineProperty(navigator, 'languages', {{get: () => {languages_json}}});
        Object.defineProperty(navigator, 'language', {{get: () => '{lang}'}});
        Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
        Object.defineProperty(navigator, 'hardwareConcurrency', {{get: () => {cpu}}});
        Object.defineProperty(navigator, 'deviceMemory', {{get: () => {ram}}});
        Object.defineProperty(navigator, 'maxTouchPoints', {{get: () => {dokunma}}});

        // -------------------- SCREEN --------------------
        Object.defineProperty(screen, 'width', {{get: () => {width}}});
        Object.defineProperty(screen, 'height', {{get: () => {height}}});
        Object.defineProperty(screen, 'availWidth', {{get: () => {width}}});
        Object.defineProperty(screen, 'availHeight', {{get: () => {height - 40}}});
        
        // -------------------- CHROME OBJECT (tam sürüm) --------------------
        if (!window.chrome) window.chrome = {{}};
        window.chrome.runtime = {{}};
        window.chrome.app = {{}};
        window.chrome.csi = function() {{ return {{}}; }};
        window.chrome.loadTimes = function() {{ return {{}}; }};

        // -------------------- PLUGINS (sahte, gerçek Chrome ile aynı) --------------------
        const pluginData = [
            {{name: "Chrome PDF Plugin", filename: "internal-pdf-viewer", description: "Portable Document Format"}},
            {{name: "Chrome PDF Viewer", filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai", description: ""}},
            {{name: "Native Client", filename: "internal-nacl-plugin", description: ""}}
        ];
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
                length: 1,
                item: function(i) {{ return this[i]; }},
                namedItem: function(name) {{
                    return this[0] && this[0].name === name ? this[0] : null;
                }}
            }};
            const mime = {{
                type: 'application/pdf',
                suffixes: 'pdf',
                description: '',
                enabledPlugin: plugin
            }};
            plugin.length = 1;
            plugin[0] = mime;
            plugins[i] = plugin;
        }}
        Object.defineProperty(navigator, 'plugins', {{get: () => plugins}});
        
        // -------------------- MIMETYPES --------------------
        Object.defineProperty(navigator, 'mimeTypes', {{get: () => ({{ length: 1, item: () => null }})}});

        // -------------------- WEBGL 1.0 + EXTENSION --------------------
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
        
        // -------------------- WEBGL 2.0 (opsiyonel) --------------------
        if (WebGL2RenderingContext) {{
            const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
            WebGL2RenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return '{webgl_vendor}';
                if (parameter === 37446) return '{webgl_renderer}';
                return getParameter2.call(this, parameter);
            }};
            const originalGetExtension2 = WebGL2RenderingContext.prototype.getExtension;
            WebGL2RenderingContext.prototype.getExtension = function(name) {{
                if (name === 'WEBGL_debug_renderer_info') {{
                    return {{
                        getParameter: function(param) {{
                            if (param === 37445) return '{webgl_vendor}';
                            if (param === 37446) return '{webgl_renderer}';
                            return null;
                        }}
                    }};
                }}
                return originalGetExtension2.call(this, name);
            }};
        }}
        
        // -------------------- CANVAS (sadece kırmızı kanal, düşük gürültü) --------------------
        const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function(type, quality) {{
            try {{
                const context = this.getContext('2d');
                const imageData = context.getImageData(0, 0, this.width, this.height);
                const data = imageData.data;
                const noise = {canvas_noise};
                for (let i = 0; i < data.length; i += 4) {{
                    data[i] = Math.min(255, Math.max(0, data[i] + noise * 255));
                }}
                context.putImageData(imageData, 0, 0);
            }} catch(e) {{}}
            return originalToDataURL.call(this, type, quality);
        }};
        
        console.log('StealthJS yüklendi, canvas_noise = {canvas_noise}');
    }})();
    """
    return js_code

# -------------------- TARAYICI BAŞLATMA --------------------
async def tarayici_baslat(veri, profil_adi=None, proxy=None):
    stealth_js = generate_stealth_js(veri)

    async with async_playwright() as p:
        args = [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            f'--user-agent={veri["ua"]}',
            f'--lang={veri["dil"]}',
            f'--accept-lang={veri["kabul_diller"][0]}',
            f'--ui-language={veri["ui_dili"]}',
            '--disable-features=UserAgentClientHint,ClientHints,ReduceUserAgent',
            '--disable-features=AutomationControlled',
            '--disable-component-extensions-with-background-pages',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-sync',
            '--disable-domain-reliability',
            '--force-fieldtrials=*ClientHints/Disabled/'
        ]
        if proxy:
            args.append(f'--proxy-server={proxy}')

        browser = await p.chromium.launch(headless=False, args=args)

        context = await browser.new_context(
            viewport={'width': veri["width"], 'height': veri["height"]},
            locale=veri["dil"],
            timezone_id=veri["tz"]
        )
        await context.add_init_script(stealth_js)
        page = await context.new_page()
        await page.goto('https://browserleaks.com')

        print("\n" + "="*70)
        print(" STEALTHSHIFT - FINGERPRINT TARAYICI")
        if profil_adi:
            print(f"Profil: {profil_adi}")
        print("="*70)
        print(f"User-Agent       : {veri['ua']}")
        print(f"Pencere          : {veri['width']}x{veri['height']}")
        print(f"Dil              : {veri['dil']} (UI: {veri['ui_dili']})")
        print(f"Zaman Dilimi     : {veri['tz']}")
        print(f"Platform         : {veri['platform']}")
        print(f"CPU Cekirdek     : {veri['cpu']}")
        print(f"RAM              : {veri['ram']} GB")
        print(f"WebGL Vendor     : {veri['webgl_vendor']}")
        print(f"WebGL Renderer   : {veri['webgl_renderer']}")
        print(f"Canvas Gurultu   : {veri['canvas_noise']:.6f}")
        print(f"Audio Gurultu    : {veri['audio_noise']:.6f}")
        print(f"Dokunmatik       : {'Evet' if veri['dokunma'] else 'Hayir'}")
        print(f"Fontlar          : {', '.join(veri['fonts'])}")
        print(f"Eklenti Sayisi   : {len(veri['plugins'])}")
        print(f"SpeechSynthesis : {veri['speech_voice_count']} ses")
        print(f"Batarya         : {'Sarjda' if veri['battery_charging'] else 'Pil ile'} ({veri['battery_level']:.0%})")
        print("="*70)
        print("\nTarayici acik. Kapatmak icin pencereyi kapatin.\n")

        try:
            while True:
                try:
                    await page.wait_for_event('close', timeout=1000)
                    break
                except:
                    if page.is_closed():
                        break
                    await asyncio.sleep(1)
            print("\nTarayici penceresi kapatildi.")
        except KeyboardInterrupt:
            print("\nProgram durduruldu.")
        finally:
            await browser.close()
            print("Tarayici tamamen kapatildi.")

# -------------------- TERMİNAL MENÜSÜ --------------------
def ana_menu():
    print("\n" + "="*50)
    print("STEALTHSHIFT - PROFIL YONETIMI")
    print("="*50)
    print("1. Yeni profil olustur ve ac (rastgele)")
    print("2. Kayitli profili yukle ve ac")
    print("3. Kayitli profilleri listele")
    print("4. Profil sil")
    print("5. Cikis")
    print("="*50)

def profil_sec():
    profiller = profilleri_listele()
    if not profiller:
        print("Hic kayitli profil yok. Once 1. secenegi kullanarak profil olusturun.")
        return None
    print("\nKayitli profiller:")
    for i, p in enumerate(profiller, 1):
        print(f"   {i}. {p}")
    try:
        secim = int(input("Secmek istediginiz profilin numarasi (0 iptal): "))
        if secim == 0:
            return None
        return profiller[secim-1]
    except:
        print("Gecersiz secim.")
        return None

async def main():
    while True:
        ana_menu()
        secim = input("Seciminiz: ").strip()
        if secim == "1":
            proxy = input("Proxy (istege bagli, bos birak): ").strip() or None
            veri = rastgele_veriler(proxy)
            profil_adi = input("Profil adi (bos birakirsaniz otomatik isim verilecek): ").strip()
            if not profil_adi:
                profil_adi = f"profil_{len(profilleri_listele())+1}_{random.randint(100,999)}"
            profil_kaydet(profil_adi, veri)
            await tarayici_baslat(veri, profil_adi, proxy)
        elif secim == "2":
            profil_adi = profil_sec()
            if profil_adi:
                veri = profil_yukle(profil_adi)
                if veri:
                    proxy = input("Proxy (istege bagli, bos birak): ").strip() or None
                    await tarayici_baslat(veri, profil_adi, proxy)
                else:
                    print(f"Profil '{profil_adi}' yuklenemedi (dosya bozuk olabilir).")
        elif secim == "3":
            profiller = profilleri_listele()
            if profiller:
                print("\nKayitli profiller:")
                for p in profiller:
                    print(f"   - {p}")
            else:
                print("Hic profil yok.")
        elif secim == "4":
            profil_adi = profil_sec()
            if profil_adi:
                onay = input(f"'{profil_adi}' profilini silmek istediginize emin misiniz? (e/E): ")
                if onay.lower() == 'e':
                    profil_sil(profil_adi)
        elif secim == "5":
            print("Cikiliyor...")
            break
        else:
            print("Gecersiz secim, tekrar deneyin.")

# -------------------- KOMUT SATIRI ARGÜMANLARI (ELECTRON İÇİN) --------------------
if __name__ == "__main__":
    import sys
    import json
    import asyncio

    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            profiller = profilleri_listele()
            profil_listesi = []
            for profil_adi in profiller:
                veri = profil_yukle(profil_adi)
                if veri:
                    profil_listesi.append({
                        "adi": profil_adi,
                        "ua": veri.get("ua", "Bilinmiyor")[:60],
                        "dil": veri.get("dil", "Bilinmiyor"),
                        "tz": veri.get("tz", "Bilinmiyor")
                    })
            print(json.dumps(profil_listesi, ensure_ascii=False))
        elif sys.argv[1] == "--open" and len(sys.argv) > 2:
            profil_adi = sys.argv[2]
            veri = profil_yukle(profil_adi)
            if veri:
                asyncio.run(tarayici_baslat(veri, profil_adi))
            else:
                print(f"Profil '{profil_adi}' bulunamadi.")
        elif sys.argv[1] == "--create" and len(sys.argv) > 2:
            profil_adi = sys.argv[2]
            proxy = sys.argv[3] if len(sys.argv) > 3 else None
            veri = rastgele_veriler(proxy)
            profil_kaydet(profil_adi, veri)
            print(json.dumps({"status": "ok", "adi": profil_adi}))
        elif sys.argv[1] == "--delete" and len(sys.argv) > 2:
            profil_adi = sys.argv[2]
            if profil_sil(profil_adi):
                print(json.dumps({"status": "ok", "adi": profil_adi}))
            else:
                print(json.dumps({"status": "error", "message": "Profile not found"}))
        else:
            print("Kullanim:")
            print("  --list                 : Profilleri JSON formatinda listele")
            print("  --open <profil_adi>    : Profili ac")
            print("  --create <profil_adi>  : Yeni profil olustur")
            print("  --delete <profil_adi>  : Profili sil")
    else:
        asyncio.run(main())