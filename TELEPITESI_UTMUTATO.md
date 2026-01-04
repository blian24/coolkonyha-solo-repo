# Telepítési Útmutató - CoolKonyha Assistant

Ez a dokumentum lépésről lépésre bemutatja, hogyan kell beüzemelni a CoolKonyha AI Asszisztenst.

## 1. Előfeltételek

A rendszer használatához szükséged lesz az alábbiakra:

1.  **Google Gemini API Kulcs:**
    *   Látogass el a [Google AI Studio](https://aistudio.google.com/) oldalra.
    *   Kattints a "Get API Key" gombra.
    *   Másold ki a kapott kulcsot.

2.  **Google Cloud Hozzáférés (credentials.json):**
    *   Hozz létre egy projektet a [Google Cloud Console](https://console.cloud.google.com/)-on.
    *   Engedélyezd a **Gmail API**, **Google Drive API** és **Google Sheets API** szolgáltatásokat.
    *   Hozz létre egy **Service Account**-ot.
    *   Töltsd le a hozzá tartozó JSON kulcsot, nevezd át `credentials.json`-re, és másold be ebbe a mappába.

3.  **Python Telepítése:**
    *   Töltsd le és telepítsd a Python legújabb verzióját a [python.org](https://www.python.org/downloads/) oldalról.
    *   **FONTOS:** A telepítésnél pipáld be az "Add Python to PATH" opciót!

## 2. Konfiguráció

1.  Nyisd meg a `.streamlit/secrets.toml` fájlt egy szövegszerkesztővel (pl. Notepad).
2.  Másold be a Gemini API kulcsodat a `GOOGLE_API_KEY` sorhoz.
3.  (Opcionális) Generálj új jelszó hash-eket az admin és user felhasználókhoz, ha módosítani szeretnéd az alapértelmezett jelszavakat.

## 3. Indítás

1.  Kattints duplán a `run_coolkonyha.bat` fájlra.
2.  A program automatikusan telepíti a szükséges kiegészítőket (ez az első alkalommal pár percig tarthat).
3.  Ha minden sikeres, megnyílik a böngésződben a `http://localhost:8501` cím, ahol bejelentkezhetsz.

### 3.1 Gyorsbelépés (Magic Links)
Ha nem szeretnél minden alkalommal bejelentkezni (csak fejlesztéshez ajánlott!), használd az alábbi linkeket:
*   **Admin belépés:** [http://localhost:8501/?auto_login=admin](http://localhost:8501/?auto_login=admin)
*   **User belépés:** [http://localhost:8501/?auto_login=user](http://localhost:8501/?auto_login=user)

## 4. Hibaelhárítás

*   **Nem indul el:** Ellenőrizd, hogy a `credentials.json` és a `secrets.toml` fájlok a helyükön vannak-e.
*   **Jelszó hiba:** Ha elfelejtetted a jelszót, töröld a `secrets.toml` fájlt, és indítsd újra a programot (vagy állítsd vissza a biztonsági mentésből).
*   **Telepítési hiba (WinError 32):** Ha a telepítés közben "A folyamat nem fér hozzá a fájlhoz..." hibát kapsz:
    1.  Zárd be a parancssor ablakot.
    2.  Próbáld meg újra futtatni a `run_coolkonyha.bat` fájlt.
    3.  Ha továbbra sem működik, töröld ki a `venv` mappát, és indítsd újra a folyamatot.

## 5. Költségek

*   Szoftver: Ingyenes
*   AI Használat: kb. 2.000 - 6.000 Ft / hó (használattól függően)
*   Üzemeltetés: kb. 5.000 Ft / hó
