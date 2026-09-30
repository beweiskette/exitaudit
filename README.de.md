# ExitAudit

Vergleicht einen Markdown-/CSV-Export mit dem migrierten Ordner und meldet fehlende Dateien, veränderte Inhalte, defekte lokale Links und verlorene Tabellenzeilen.

Erste nutzbare Version 0.1.0. Python ab 3.11, MIT-Lizenz. Vollständige Schnittstellen und Beispiele stehen in der [englischen README](README.md).

## Installation

Im geklonten Repo eine virtuelle Umgebung anlegen:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
```

## Beispiel

```sh
exitaudit compare examples/source examples/target --out outputs/check
```

Berichte entstehen als `report.json` und `report.html` im gewählten Ausgabeordner. Rückgabecode 0 bedeutet bestanden, 1 bedeutet Befunde, 2 einen Eingabe- oder Laufzeitfehler. Die Beispieldaten sind künstlich.

Alles bleibt lokal. Berichte enthalten relative Dateinamen, aber keine Dokumenttexte oder CSV-Zellwerte. Nicht lesbare und unsichere Eingaben bleiben sichtbar ungeprüft. Der Linkparser deckt gängige Markdown-Links ab; Formatierung, HTML-Links, Anker und eingebettete Anwendungsobjekte bleiben ausserhalb des Umfangs.

Tests: `python -m pytest -q`. Für Docker- und Browsertests gelten die zusätzlichen Voraussetzungen in der englischen README. Das Werkzeug lädt keine Berichte hoch und ruft keine Modell-API auf.
