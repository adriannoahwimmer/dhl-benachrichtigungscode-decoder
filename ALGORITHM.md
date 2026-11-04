# Spezifikation: DHL / Deutsche Post Benachrichtigungscode

Kanonische Beschreibung des Aufbaus des **16-stelligen Benachrichtigungscodes**, der auf der gelben Benachrichtigungskarte („Information zu Ihrer Sendung") aufgedruckt ist.

> Durch Reverse-Engineering eigener Karten rekonstruiert. Inoffiziell, keine Verbindung zu DHL/Deutsche Post, ohne Gewähr. Primärquelle: <https://github.com/adriannoahwimmer/dhl-benachrichtigungscode-decoder>

## Abgrenzung

Dies betrifft **nur** den statischen, aufgedruckten Benachrichtigungscode (16 Ziffern). Es betrifft **nicht** den zeitbasierten Abholcode der Post-&-DHL-App (10 Zeichen, beginnt mit `A`, erneuert sich alle 120 Sekunden) — dieser ist nicht aus festen Daten ableitbar.

## Felder (16 Stellen)

| Stellen | Feld | Beschreibung |
|--------:|------|--------------|
| 1–3 | `DDD` | Tag des Jahres (`001`–`366`) des Datums auf der Karte (Einlieferung / fehlgeschlagener Zustellversuch) |
| 4 | `W` | Wochentag desselben Datums, **Montag = 0 … Sonntag = 6** |
| 5–15 | `SSSSSSSSSSS` | die **letzten 11 Ziffern** der Sendungsnummer |
| 16 | `P` | Prüfziffer über die Stellen 1–15 |

## Prüfziffer

Mod-10-Verfahren im GS1-Stil über die ersten 15 Stellen:

1. Stellen 1–15 **von rechts** durchnummerieren (rechte Stelle = Index 0).
2. Index gerade → Gewicht **1**, Index ungerade → Gewicht **3**.
3. Gewichtete Summe bilden.
4. `Prüfziffer = (10 − (Summe mod 10)) mod 10`.

### Pseudocode

```
function pruefziffer(body15):
    summe = 0
    for i, ziffer in enumerate(reverse(body15)):   # i = 0 rechts
        gewicht = 1 if i even else 3
        summe += ziffer * gewicht
    return (10 - summe % 10) % 10

function code(sendungsnummer, datum):
    DDD = tag_des_jahres(datum)            # 3-stellig, führende Nullen
    W   = wochentag(datum)                 # Montag=0 … Sonntag=6
    S   = sendungsnummer[-11:]             # letzte 11 Ziffern
    body = DDD + W + S                      # 15 Stellen
    return body + pruefziffer(body)        # 16 Stellen
```

## Testvektoren

| Benachrichtigungscode | Sendungsnummer | Datum | Wochentag |
|---|---|---|---|
| `3045817897053451` | `00340433881789705345` | 2026-10-31 | Samstag (5) |
| `3045376541158376` | `00340434637654115837` | 2026-10-31 | Samstag (5) |

Maschinenlesbar in [`test_vectors.json`](test_vectors.json). Referenzimplementierung in [`decode.py`](decode.py).

## Belegstatus

- **Gut belegt:** Felder 1, 5–15, 16 (über mehrere Karten verifiziert).
- **Plausibel, noch schwach belegt:** Feld 4 (Wochentag) — bisher nur Karten vom selben Wochentag vorhanden. Codes von anderen Wochentagen würden es bestätigen.
