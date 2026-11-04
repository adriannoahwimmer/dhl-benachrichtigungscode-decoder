#!/usr/bin/env python3
"""
DHL / Deutsche Post Benachrichtigungscode — Decoder & Generator
================================================================
Analysiert den 16-stelligen *Benachrichtigungscode* von der gelben
Benachrichtigungskarte ("Information zu Ihrer Sendung").

ACHTUNG: Das ist NICHT der zeitbasierte Abholcode aus der App
(beginnt mit "A", 10-stellig, erneuert sich alle 120 Sekunden).

Aufbau (16 Stellen):
  [1-3]  Tag des Jahres der Zustellung (001-366)
  [4]    Wochentag (Montag=0 ... Sonntag=6)
  [5-15] die letzten 11 Ziffern der Sendungsnummer
  [16]   Prüfziffer (GS1-/mod-10-Verfahren über Stelle 1-15)

Prüfziffer: Stellen 1-15 von rechts abwechselnd ×1, ×3 gewichten,
summieren, Prüfziffer = (10 - Summe mod 10) mod 10.

Reverse-engineered aus eigenen Benachrichtigungskarten. Keine
Verbindung zu DHL/Deutsche Post. Nur zu Bildungszwecken.
"""
from __future__ import annotations
import datetime as dt

def check_digit(body15: str) -> int:
    """GS1-/mod-10-Prüfziffer über 15 Stellen (von rechts ×1,×3)."""
    s = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(reversed(body15)))
    return (10 - s % 10) % 10

def generate(tracking: str, delivery_date: dt.date) -> str:
    """Baut den 16-stelligen Code aus Sendungsnummer + Zustelldatum."""
    tracking = "".join(ch for ch in tracking if ch.isdigit())
    doy = f"{delivery_date.timetuple().tm_yday:03d}"
    weekday = str(delivery_date.weekday())          # Mo=0 ... So=6
    last11 = tracking[-11:]
    body = doy + weekday + last11
    return body + str(check_digit(body))

def decode(code: str) -> dict:
    """Zerlegt einen 16-stelligen Code und prüft die Prüfziffer."""
    code = "".join(ch for ch in code if ch.isdigit())
    if len(code) != 16:
        raise ValueError(f"Code muss 16 Ziffern haben, hat {len(code)}.")
    body, cd = code[:15], int(code[15])
    doy = int(code[:3]); weekday = int(code[3]); last11 = code[4:15]
    wdays = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
    return {
        "tag_des_jahres": doy,
        "wochentag_ziffer": weekday,
        "wochentag_name": wdays[weekday] if 0 <= weekday <= 6 else "?",
        "sendungsnr_ende_11": last11,
        "pruefziffer": cd,
        "pruefziffer_erwartet": check_digit(body),
        "pruefziffer_ok": cd == check_digit(body),
    }

# --- Test-Vektoren (reale Karten, Personendaten entfernt) --------------
TEST_VECTORS = [
    ("3045817897053451", "00340433881789705345"),
    ("3045376541158376", "00340434637654115837"),
]

if __name__ == "__main__":
    import sys, json
    if len(sys.argv) == 1:
        print("Selbsttest:")
        for code, trk in TEST_VECTORS:
            d = decode(code)
            print(f"  {code}  Prüfziffer ok: {d['pruefziffer_ok']}  "
                  f"({d['wochentag_name']}, Sendungsnr. ...{d['sendungsnr_ende_11']})")
        print(f"\n  31.10.2026 ist ein {['Mo','Di','Mi','Do','Fr','Sa','So'][dt.date(2026,10,31).weekday()]}"
              f" (Ziffer {dt.date(2026,10,31).weekday()})")
        print("\nNutzung:")
        print("  python decode.py decode 3045817897053451")
        print("  python decode.py gen 00340433881789705345 2026-10-31")
    elif sys.argv[1] == "decode":
        print(json.dumps(decode(sys.argv[2]), ensure_ascii=False, indent=2))
    elif sys.argv[1] == "gen":
        print(generate(sys.argv[2], dt.date.fromisoformat(sys.argv[3])))
