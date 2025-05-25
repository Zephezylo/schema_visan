# Schema Visan

Ett litet schemaläggningsprogram för föräldrakooperativ. Programmet är
skrivet i Python och använder endast standardbiblioteket. Från och med
denna version kan även ett enkelt Excel-ark användas som källa för
föräldrarnas önskemål.

## Komma igång

1. Säkerställ att du har Python 3 installerat.
2. Uppdatera `config.json` med period, stängda dagar och föräldrars
   inställningar. Vill du läsa in önskemål från ett Excel-ark anger du
   sökvägen under nyckeln `excel_file` i konfigurationen.
3. Kör `python main.py` för att generera ett schema i terminalen.
4. Alternativt kan du starta ett enkelt GUI med `python gui.py`.

## Struktur

- `models.py` – datamodeller för föräldrar och dagregler.
- `scheduler.py` – funktion för att skapa schemat.
- `main.py` – läser in konfiguration och skriver ut schemat.
- `gui.py` – mycket enkel Tkinter-applikation.
- `excel_import.py` – minimal inläsning av Excel-filer (xlsx).
- `config.json` – exempelkonfiguration som kan redigeras.

Programmet är avsett som en bas som kan vidareutvecklas.
