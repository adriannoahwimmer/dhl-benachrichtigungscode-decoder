# DHL / Deutsche Post Benachrichtigungscode — Aufbau & Rechner

**Wie ist der 16-stellige Benachrichtigungscode auf der gelben DHL-/Deutsche-Post-Benachrichtigungskarte aufgebaut?** Dieses Projekt erklärt den Aufbau und bietet einen Rechner, mit dem du den Code selbst nachrechnen und zerlegen kannst — direkt im Browser.

➡️ **Rechner:** _(nach dem Push: GitHub Pages aktivieren → Link hier eintragen, z. B. `https://DEIN-NAME.github.io/dhl-benachrichtigungscode-decoder/`)_

> ⚠️ Inoffiziell & unabhängig. Keine Verbindung zu DHL oder Deutsche Post. Durch Reverse-Engineering **eigener** Benachrichtigungskarten entstanden, auf Basis weniger Beispiele — **ohne Gewähr**. Nur zu Bildungszwecken.

---

## Welche Karte / welcher Code ist gemeint?

| | |
|---|---|
| ✅ **Funktioniert** | Die **gelbe Benachrichtigungskarte** „Information zu Ihrer Sendung“ mit fest aufgedrucktem **16-stelligen** „Benachrichtigungscode zur Abholung“, z. B. `3045 8178 9705 3451`. Statisch → berechenbar. |
| ❌ **Funktioniert nicht** | Der **Abholcode in der Post & DHL App** für die Packstation: **10-stellig**, beginnt mit `A` (z. B. `A 616 867 731`), erneuert sich alle 120 Sekunden. Zeitbasiert → **nicht** aus festen Daten berechenbar. |

## Aufbau des 16-stelligen Codes

```
304 5 81789705345 1
└─┘ │ └─────────┘ │
 │  │      │      └── Prüfziffer über die 15 Stellen davor
 │  │      └───────── letzte 11 Ziffern der Sendungsnummer
 │  └──────────────── Wochentag (Mo=0 … So=6);  5 = Samstag
 └─────────────────── Tag des Jahres (001–366); 304 = 31. Oktober
```

| Stellen | Bedeutung | Beispiel |
|--------:|-----------|----------|
| 1–3 | Tag des Jahres der Zustellung (`001`–`366`) | `304` → 31.10. |
| 4 | Wochentag, Montag = 0 … Sonntag = 6 | `5` → Samstag |
| 5–15 | die letzten 11 Ziffern der Sendungsnummer | `81789705345` |
| 16 | Prüfziffer (GS1-/mod-10) | `1` |

### Prüfziffer-Algorithmus

Die ersten 15 Stellen von **rechts** abwechselnd mit **×1** und **×3** gewichten, summieren, dann:

```
Prüfziffer = (10 − Summe mod 10) mod 10
```

Das ist ein klassisches GS1-/mod-10-Verfahren, wie es in vielen Barcode-Standards vorkommt. Es erkennt Tippfehler — es ist **keine** Zugangssicherung.

## Nutzung (Python)

```bash
python decode.py                 # Selbsttest + Beispiele
python decode.py decode 3045817897053451
python decode.py gen 00340433881789705345 2026-10-31
```

```python
from decode import generate, decode
import datetime as dt

generate("00340433881789705345", dt.date(2026, 10, 31))  # -> '3045817897053451'
decode("3045817897053451")["pruefziffer_ok"]             # -> True
```

## Testvektoren

Reale Karten, Personendaten entfernt (siehe [`test_vectors.json`](test_vectors.json)):

| Benachrichtigungscode | Sendungsnummer | Zustelltag |
|---|---|---|
| `3045 8178 9705 3451` | `0034 0433 8817 8970 5345` | Sa, 31.10.2026 |
| `3045 3765 4115 8376` | `0034 0434 6376 5411 5837` | Sa, 31.10.2026 |

## Credits

Die Grundidee — dass sich der Code aus **Prüfziffer + Sendungsnummer + Tag der Einlieferung** zusammensetzt — kam von einer hilfsbereiten Person an der Packstation. **Props an dich!** 🙌 Falls du dich meldest, verlinke ich dich gern, so wie du es möchtest. Die genaue Formel und die Stellenaufteilung wurden daraus aus eigenen Benachrichtigungskarten rekonstruiert.

## Mithelfen

Der Aufbau basiert bisher nur auf wenigen Karten vom selben Tag. Besonders hilfreich: **Codes von anderen Wochentagen**, um die Wochentag-Stelle und die Prüfziffer über mehr Fälle zu bestätigen. Gerne ein Issue mit (anonymisiertem) Code + Sendungsnummer + Datum öffnen.

> 🔒 **Privatsphäre:** Beim Teilen von Fotos oder Codes bitte Name, Anschrift und die volle Sendungsnummer schwärzen.

## Haftungsausschluss

Der Benachrichtigungscode ist kein alleiniger Zugangsschlüssel: Die Abholung in der Filiale verlangt einen Ausweis, die Packstation den App-Code. Dieses Repo dient dem Verständnis des Zahlenaufbaus, nicht dazu, Identitäts- oder Abholnachweise zu umgehen.

## Lizenz

[MIT](LICENSE)

---

<sub>Schlagwörter: DHL Benachrichtigungscode berechnen · Deutsche Post Benachrichtigungskarte · Benachrichtigungscode Aufbau · Abholcode Packstation · Prüfziffer · Sendungsnummer decoder</sub>
