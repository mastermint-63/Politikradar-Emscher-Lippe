"""Scraper für more!rubin-Systeme auf gremien.info (via iCal-WebCalendar-Export)."""

import requests
from datetime import datetime
from .ratsinfo import RatsinfoScraper
from .base import Termin


class GremienInfoScraper(RatsinfoScraper):
    """Scraper für more!rubin-basierte Ratsinformationssysteme auf gremien.info."""

    def __init__(self, stadt_name: str, base_url: str):
        super().__init__(stadt_name, base_url)
        self.ical_url = f"{self.base_domain}/api.php?id=calendar&action=webcalendar"
        self.json_url = f"{self.base_domain}/api.php?id=calendar&action=get&view=default"

    def hole_termine(self, jahr: int, monat: int) -> list[Termin]:
        """Holt Termine via iCal; fällt bei HTTP 500 auf JSON-API zurück."""
        try:
            response = requests.get(self.ical_url, headers=self.HEADERS, timeout=30)
            if response.status_code == 500:
                return self._hole_termine_json(jahr, monat)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return self._parse_ical(response.text, jahr, monat)
        except requests.HTTPError:
            return self._hole_termine_json(jahr, monat)

    def _hole_termine_json(self, jahr: int, monat: int) -> list[Termin]:
        """Holt Termine über die JSON-Kalender-API (Fallback bei defektem iCal-Endpunkt)."""
        monat_str = f"{jahr}-{monat:02d}"
        url = f"{self.json_url}&from={monat_str}&to={monat_str}"
        response = requests.get(url, headers=self.HEADERS, timeout=30)
        response.raise_for_status()
        daten = response.json()

        termine = []
        for meeting in daten.get("meetings", []):
            try:
                datum = datetime.strptime(meeting["datum"], "%Y-%m-%d")
            except (ValueError, KeyError):
                continue

            if datum.year != jahr or datum.month != monat:
                continue

            beginn = meeting.get("beginn", "00:00:00")
            try:
                h, m, _ = beginn.split(":")
                datum = datum.replace(hour=int(h), minute=int(m))
                uhrzeit = f"{int(h):02d}:{int(m):02d} Uhr"
            except (ValueError, AttributeError):
                uhrzeit = ""

            gremium = meeting.get("titel", "Unbekannt")[:100]
            ort = meeting.get("room", {}).get("name", "")[:100]
            link = meeting.get("full_url", f"{self.base_domain}/meeting/{meeting.get('id', '')}")

            termine.append(Termin(
                stadt=self.stadt_name,
                datum=datum,
                uhrzeit=uhrzeit,
                gremium=gremium,
                ort=ort,
                link=link
            ))

        return termine
