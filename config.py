"""Konfiguration der Ratsinformationssysteme im Emscher-Lippe-Raum."""

from enum import Enum
from dataclasses import dataclass


class SystemTyp(Enum):
    SESSIONNET = "sessionnet"
    RATSINFO = "ratsinfo"
    ALLRIS = "allris"
    GREMIENINFO = "gremieninfo"
    NICHT_UNTERSTUETZT = "nicht_unterstuetzt"


class Kreis(Enum):
    """Kreise und kreisfreie Städte im Emscher-Lippe-Raum."""
    UEBERREGIONAL = "Überregional"
    GELSENKIRCHEN = "Gelsenkirchen"
    BOTTROP = "Bottrop"
    RECKLINGHAUSEN = "Kreis Recklinghausen"


@dataclass
class Stadt:
    name: str
    einwohner: int
    url: str
    typ: SystemTyp
    kreis: Kreis


def erkenne_systemtyp(url: str) -> SystemTyp:
    """Erkennt den Systemtyp anhand der URL."""
    if "si0046" in url:
        return SystemTyp.SESSIONNET
    if "ratsinfomanagement.net" in url:
        return SystemTyp.RATSINFO
    return SystemTyp.NICHT_UNTERSTUETZT


STAEDTE = [
    # Überregional (RVR)
    Stadt("Regionalverband Ruhr (RVR)", 0, "https://ris.rvr.ruhr/si0046.asp", SystemTyp.SESSIONNET, Kreis.UEBERREGIONAL),

    # Gelsenkirchen (kreisfrei)
    Stadt("Gelsenkirchen", 261000, "https://ratsinformation.gelsenkirchen.de", SystemTyp.ALLRIS, Kreis.GELSENKIRCHEN),

    # Bottrop (kreisfrei)
    Stadt("Bottrop", 116000, "https://ratsinfo-bottrop.de", SystemTyp.RATSINFO, Kreis.BOTTROP),

    # Kreis Recklinghausen
    Stadt("Kreis Recklinghausen", 620000, "https://kvrecklinghausen.gremien.info", SystemTyp.GREMIENINFO, Kreis.RECKLINGHAUSEN),
    Stadt("Castrop-Rauxel", 73000, "https://castroprauxel.gremien.info", SystemTyp.GREMIENINFO, Kreis.RECKLINGHAUSEN),
    Stadt("Datteln", 34000, "https://datteln.gremien.info", SystemTyp.GREMIENINFO, Kreis.RECKLINGHAUSEN),
    Stadt("Dorsten", 75000, "https://dorsten.gremien.info", SystemTyp.GREMIENINFO, Kreis.RECKLINGHAUSEN),
    Stadt("Gladbeck", 76000, "https://gladbeck.gremien.info", SystemTyp.GREMIENINFO, Kreis.RECKLINGHAUSEN),
    Stadt("Haltern am See", 37000, "https://haltern.gremien.info", SystemTyp.GREMIENINFO, Kreis.RECKLINGHAUSEN),
    Stadt("Herten", 61000, "https://herten.gremien.info", SystemTyp.GREMIENINFO, Kreis.RECKLINGHAUSEN),
    Stadt("Marl", 84000, "https://marl.gremien.info", SystemTyp.GREMIENINFO, Kreis.RECKLINGHAUSEN),
    Stadt("Oer-Erkenschwick", 29000, "https://oer-erkenschwick.gremien.info", SystemTyp.GREMIENINFO, Kreis.RECKLINGHAUSEN),
    Stadt("Recklinghausen", 112000, "https://stadt-recklinghausen.gremien.info", SystemTyp.GREMIENINFO, Kreis.RECKLINGHAUSEN),
    Stadt("Waltrop", 29000, "https://waltrop.gremien.info", SystemTyp.GREMIENINFO, Kreis.RECKLINGHAUSEN),
]


def get_staedte_nach_typ(typ: SystemTyp) -> list[Stadt]:
    """Gibt alle Städte eines bestimmten Systemtyps zurück."""
    return [s for s in STAEDTE if s.typ == typ]


def get_staedte_nach_kreis(kreis: Kreis) -> list[Stadt]:
    """Gibt alle Städte eines Kreises zurück."""
    return [s for s in STAEDTE if s.kreis == kreis]


def get_unterstuetzte_staedte() -> list[Stadt]:
    """Gibt alle Städte mit unterstütztem Systemtyp zurück."""
    return [s for s in STAEDTE if s.typ != SystemTyp.NICHT_UNTERSTUETZT]
