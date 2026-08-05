import json
import os
import random
import re
import time
from playwright.sync_api import sync_playwright

LÖSUNGEN_DATEI = "lösungen.json"

# wert [FEHLER_QUOTE = 0]  muss erhöht werden ansonsten Detection gefahr!
FEHLER_QUOTE = 0  
LOESEN_KLICK_NACH_FEHLER_CHANCE = 0  
DENKPAUSE_NACH_FEHLER = (0.0, 0.0)

ZEIT_POOLS = [
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1
]

DEFAULT_TEXT = "t"


def lade_lösungen():
    if os.path.exists(LÖSUNGEN_DATEI):
        try:
            with open(LÖSUNGEN_DATEI, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def speichere_lösung(frage, antwort):
    if not frage or antwort is None:
        return
    daten = lade_lösungen()
    daten[frage.strip()] = str(antwort).strip()
    with open(LÖSUNGEN_DATEI, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)
    print(f"[Save]={str(antwort).strip()}")

if not os.path.exists(LÖSUNGEN_DATEI):
    with open(LÖSUNGEN_DATEI, "w", encoding="utf-8") as f:
        json.dump({}, f)

def generiere_zustands_schlüssel(page, schritt_counter):
    h2_element = page.locator("h2, h1").first
    if not h2_element.is_visible():
        return None
    haupt_frage = h2_element.text_content().strip()

    kontext_elemente = page.locator("svg tspan, svg text, tspan, .label, label").all()
    unter_texte = []
    for el in kontext_elemente:
        try:
            txt = el.text_content().strip()
            if txt and txt not in unter_texte and txt not in haupt_frage and len(txt) < 60:
                unter_texte.append(txt)
        except Exception:
            pass

    kontext_str = " | ".join(unter_texte) if unter_texte else "STD"
    return f"{haupt_frage} [{kontext_str}] ({schritt_counter})"

def extrahiere_reine_antwort(roh_text):
    if roh_text is None:
        return ""
    
    text = str(roh_text).replace(DEFAULT_TEXT, "").replace("\n", "").strip()
    text = re.sub(r'(Flächen|Kanten|Kanen|Ecken|Spitzen|Spizen):', '', text, flags=re.IGNORECASE).strip()
    
    zahlen = re.findall(r'\d+', text)
    if zahlen:
        return zahlen[-1]
    
    return text

def tipp_text_sauber(page, text):
    eingabe_element = page.locator(".input, .cursor, [contenteditable='true'], input").first
    if eingabe_element.is_visible():
        try:
            eingabe_element.click(force=True)
            time.sleep(0.05)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.keyboard.press("Delete")
            for _ in range(5):
                page.keyboard.press("Backspace")
        except Exception:
            pass
        time.sleep(0.05)
        page.keyboard.type(str(text), delay=60)

def klicke_weiter_oder_enter(page):
    weiter_btn = page.locator("div.button, button, .btn", has_text="Weiter").first
    if weiter_btn.is_visible():
        weiter_btn.click()
    else:
        page.keyboard.press("Enter")


def bot_run(modus="lernen"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://anton.app")

        input("\n[ENTER]\n")

        letzte_basis_frage = ""
        schritt_counter = 1

        while True:
            try:
                h2_elem = page.locator("h2, h1").first
                if not h2_elem.is_visible():
                    time.sleep(0.3)
                    continue

                aktueller_tspan = ""
                tspan_elem = page.locator("svg tspan, svg text, tspan").first
                if tspan_elem.is_visible():
                    aktueller_tspan = tspan_elem.text_content().strip()

                aktuelle_basis = f"{h2_elem.text_content().strip()}_{aktueller_tspan}"

                if aktuelle_basis != letzte_basis_frage:
                    schritt_counter = 1
                    letzte_basis_frage = aktuelle_basis

                frage_key = generiere_zustands_schlüssel(page, schritt_counter)

                # ==================== MODUS 1: LERNEN ====================
                if modus == "lernen":
                    eingabe_feld = page.locator(".input, .cursor, [contenteditable='true'], input").first

                    if eingabe_feld.is_visible():
                        tipp_text_sauber(page, DEFAULT_TEXT)
                        time.sleep(0.1)
                        page.keyboard.press("Enter")
                        time.sleep(0.4)

                    loesen_btn = page.locator("div.button, button", has_text="Lösen").first
                    
                    if loesen_btn.is_visible():
                        loesen_btn.click()
                        time.sleep(0.6)

                        antwort_text = ""
                        eingabe_box = page.locator(".input, .cursor, .input-field, [contenteditable='true']").first
                        if eingabe_box.is_visible():
                            parent = eingabe_box.locator("xpath=..")
                            antwort_text = parent.text_content().strip()

                        if not antwort_text:
                            spans = page.locator("span:not([style*='line-through'])").all()
                            texte = [s.text_content().strip() for s in spans if s.text_content().strip()]
                            if texte:
                                antwort_text = texte[-1]

                        reine_antwort = extrahiere_reine_antwort(antwort_text)

                        if frage_key and reine_antwort != "":
                            speichere_lösung(frage_key, reine_antwort)
                            schritt_counter += 1

                        klicke_weiter_oder_enter(page)
                        time.sleep(0.8)
                    else:
                        klicke_weiter_oder_enter(page)
                        time.sleep(0.6)

                # ==================== MODUS 2: LÖSEN ====================
                elif modus == "lösen":
                    lösungen = lade_lösungen()

                    if frage_key in lösungen:
                        echte_antwort = lösungen[frage_key]
                        
                        basis_zeit = random.choice(ZEIT_POOLS)
                        jitter = random.uniform(-0.5, 1.5)
                        wartezeit = max(1.0, basis_zeit + jitter)
                        
                        time.sleep(wartezeit)

                        # Hier ist einfach nur fur die test das macht alles sofort 
                        tipp_text_sauber(page, echte_antwort)
                        time.sleep(0.3)
                        klicke_weiter_oder_enter(page)

                        schritt_counter += 1
                        time.sleep(random.uniform(0.8, 1.5))
                    else:
                        klicke_weiter_oder_enter(page)
                        time.sleep(1.0)

            except KeyboardInterrupt:
                break
            except Exception:
                time.sleep(0.5)

        browser.close()

if __name__ == "__main__":
    auswahl = input("[1/2]: ")
    if auswahl == "1":
        bot_run(modus="lernen")
    else:
        bot_run(modus="lösen")
