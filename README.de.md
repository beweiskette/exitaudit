# ExitAudit

Vergleicht einen Markdown-/CSV-Export mit dem migrierten Ordner und meldet fehlende Dateien, verÃ¤nderte Inhalte, defekte lokale Links und verlorene Tabellenzeilen.

Erste nutzbare Version 0.1.0. Python ab 3.11, MIT-Lizenz. VollstÃ¤ndige Schnittstellen und Beispiele stehen in der [englischen README](README.md).

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

Berichte entstehen als `report.json` und `report.html` im gewÃ¤hlten Ausgabeordner. RÃ¼ckgabecode 0 bedeutet bestanden, 1 bedeutet Befunde, 2 einen Eingabe- oder Laufzeitfehler. Die Beispieldaten sind kÃ¼nstlich.

Alles bleibt lokal. Berichte enthalten relative Dateinamen, aber keine Dokumenttexte oder CSV-Zellwerte. Nicht lesbare und unsichere Eingaben bleiben sichtbar ungeprÃ¼ft. Der Linkparser deckt gÃ¤ngige Markdown-Links ab; Formatierung, HTML-Links, Anker und eingebettete Anwendungsobjekte bleiben ausserhalb des Umfangs.

Tests: `python -m pytest -q`. FÃ¼r Docker- und Browsertests gelten die zusÃ¤tzlichen Voraussetzungen in der englischen README. Das Werkzeug lÃ¤dt keine Berichte hoch und ruft keine Modell-API auf.

Dateinamen werden für den Vergleich in Unicode-NFC vereinheitlicht. Windows-Zeilenenden gelten bei Markdown als gleichwertig. Eindeutige Umbenennungen werden auch bei Dokumenten erkannt. Links in Codeblöcken und Inline-Code bleiben unberücksichtigt. CSV-Dateien dürfen grosse Zellen und eine abschliessende Leerzeile enthalten.
