# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projektbeschreibung

**Politikradar Emscher-Lippe** – Dashboard für Ratstermine im Emscher-Lippe-Raum. Schwester-Projekt von `ratsinfo_ms/` (Politikradar Münsterland). Gleiche Codebasis, eigene `config.py` mit 15 Gremien.

- **Repo:** `github.com/mastermint-63/Politikradar-Emscher-Lippe`
- **Live:** `https://el-raete.reporter.ruhr`
- **Schwester-Projekt:** `../ratsinfo_ms/` – dort ist die vollständige Architektur-Dokumentation

## Ausführung

```bash
python3 app.py                    # 3 Monate ab heute, öffnet Browser
python3 app.py --no-browser       # Ohne Browser (für Cronjobs)
python3 app.py 2026 3             # Ab März 2026

./ratsinfos_upd_el.sh             # Manuell aktualisieren (Scraping + Push + Benachrichtigung)
tail -20 launchd.log              # Letzte Aktualisierungen anzeigen
```

## Automatische Aktualisierung

- **launchd-Job:** `de.politikradar.el.update` – täglich 06:30 Uhr
- **Plist:** `~/Library/LaunchAgents/de.politikradar.el.update.plist`
- **Python:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`

```bash
launchctl start de.politikradar.el.update   # Manuell auslösen
launchctl list | grep politikradar          # Status prüfen
```

## Gremien (config.py)

| Kreis-Enum | Inhalt |
|------------|--------|
| `UEBERREGIONAL` | RVR (`ruhrparlament.de`), VRR (`zvis.vrr.de`), Kreis Recklinghausen (`kvrecklinghausen.gremien.info`) |
| `EMSCHERLIPPE` | Bottrop, Castrop-Rauxel, Datteln, Dorsten, Gelsenkirchen, Gladbeck, Haltern, Herten, Marl, Oer-Erkenschwick, Recklinghausen, Waltrop |

## Scraper-Besonderheiten (EL-spezifisch)

**GremienInfoScraper** hat hier einen JSON-Fallback (nicht in ratsinfo_ms):
- Primär: iCal via `api.php?id=calendar&action=webcalendar`
- Fallback bei HTTP 500: JSON via `api.php?id=calendar&action=get&from=YYYY-MM&to=YYYY-MM`
- Grund: Castrop-Rauxel (`castroprauxel.gremien.info`) hat defekten iCal-Endpunkt

**SessionNetScraper** hat hier `verify=False` (nicht in ratsinfo_ms):
- Grund: Historisches SSL-Problem (ursprünglich für RVR eingebaut)

**Gelsenkirchen** – ALLRIS ohne `/public/`-Suffix:
- URL: `https://ratsinformation.gelsenkirchen.de` (AllrisScraper konstruiert `/si010` daraus)

**RVR** – more!rubin, nicht SessionNet wie der URL-Pfad suggeriert:
- URL: `https://www.ruhrparlament.de` → `GremienInfoScraper`

**Bottrop** – eigene Domain wie Bocholt im MS-Projekt:
- URL: `https://ratsinfo-bottrop.de` → `RatsinfoScraper`

## Einzelnen Scraper testen

```python
from config import STAEDTE
from scraper import GremienInfoScraper

stadt = next(s for s in STAEDTE if 'Castrop' in s.name)
scraper = GremienInfoScraper(stadt.name, stadt.url)
for t in scraper.hole_termine(2026, 3):
    print(f"{t.datum.strftime('%d.%m.%Y')} {t.uhrzeit} – {t.gremium}")
```

## Wichtige Architektur-Hinweise

Gelten identisch wie in `../ratsinfo_ms/CLAUDE.md`:
- HTML/CSS/JS ist in Python f-strings eingebettet → geschweifte Klammern verdoppeln (`{{`, `}}`)
- Bereits generierte `termine_*.html` werden bei app.py-Änderungen **nicht** automatisch neu generiert
- Auto-Scroll und Sticky Filterleiste: Details in `../ratsinfo_ms/CLAUDE.md`

## Deployment

GitHub Actions deployed automatisch bei Push von `termine_*.html` oder `index.html`.

```bash
gh run list --repo mastermint-63/Politikradar-Emscher-Lippe --workflow=deploy.yml
```
