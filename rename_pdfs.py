import argparse
import csv
import re
import shutil
from datetime import datetime
from pathlib import Path

import pdfplumber
from tqdm import tqdm

HEADER_PATTERN = re.compile(
    r"(\d+)\s+([A-Z0-9\-]+)\s+(\d{2}\.\d{2}\.\d{4})\s+-\s+\d{2}\.\d{2}\.\d{4}"
)


def extract_fields(pdf_path: Path) -> tuple[str, str, str]:
    with pdfplumber.open(pdf_path) as pdf:
        text = pdf.pages[0].extract_text() or ""
    match = HEADER_PATTERN.search(text)
    if not match:
        raise ValueError("Header-Muster nicht gefunden")
    nr, reisecode, datum_str = match.group(1), match.group(2), match.group(3)
    datum = datetime.strptime(datum_str, "%d.%m.%Y").strftime("%d.%m.%Y")
    return datum, reisecode, nr


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    counter = 2
    while True:
        candidate = path.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def main():
    parser = argparse.ArgumentParser(description="PDF-Dateien umbenennen")
    parser.add_argument("--input", required=True, help="Eingabe-Ordner")
    parser.add_argument("--output", required=True, help="Ausgabe-Ordner für Erfolge")
    parser.add_argument("--fehler", required=True, help="Ausgabe-Ordner für Fehler")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    fehler_dir = Path(args.fehler)

    output_dir.mkdir(parents=True, exist_ok=True)
    fehler_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(input_dir.rglob("*.pdf"))
    if not pdf_files:
        print("Keine PDF-Dateien im Eingabe-Ordner gefunden.")
        return

    fehler_log_path = fehler_dir / "fehler_log.csv"
    erfolge = 0
    fehler = 0

    with open(fehler_log_path, "w", newline="", encoding="utf-8") as log_file:
        writer = csv.writer(log_file)
        writer.writerow(["original_datei", "fehler_grund"])

        for pdf_path in tqdm(pdf_files, desc="Verarbeite PDFs", unit="Datei"):
            try:
                datum, reisecode, nr = extract_fields(pdf_path)
                day, month, year = datum.split(".")
                ziel_dir = output_dir / year / month
                ziel_dir.mkdir(parents=True, exist_ok=True)
                new_name = f"{datum}_{reisecode}_{nr}.pdf"
                dest = unique_path(ziel_dir / new_name)
                shutil.copy2(pdf_path, dest)
                erfolge += 1
            except Exception as e:
                writer.writerow([pdf_path.name, str(e)])
                shutil.copy2(pdf_path, fehler_dir / pdf_path.name)
                fehler += 1

    print(f"\n--- Zusammenfassung ---")
    print(f"Gefundene PDFs:       {len(pdf_files)}")
    print(f"Erfolgreich:          {erfolge}")
    print(f"Fehlgeschlagen:       {fehler}")
    if fehler:
        print(f"Fehlerprotokoll:      {fehler_log_path}")


if __name__ == "__main__":
    main()
