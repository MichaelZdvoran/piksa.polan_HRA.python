# Fire & Water: Puzzle Adventure

Jednoduchá kooperativní plošinovka pro dva hráče vytvořená v Pythonu pomocí knihovny Pygame. Hráči ovládají postavy Ohně a Vody, sbírají mince své barvy a snaží se společně dostat k východu.

## Vlastnosti
- **Kooperace:** Oba hráči musí spolupracovat, aby odemkli dveře do další úrovně.
- **Mechaniky:** Pohyblivé plošiny, nebezpečné kaluže (lávu/vodu), nepřátelé a kuše.
- **Úrovně:** Celkem 5 úrovní se stoupající obtížností.
- **OOP Architektura:** Kód je plně objektově orientovaný pro snadnou rozšiřitelnost.

## Požadavky
- Python 3.x
- Pygame

## Instalace a spuštění
1. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```
2. Spusťte hru:
   ```bash
   python src/main.py
   ```

## Ovládání
- **Voda:** Šipky (pohyb a skok)
- **Oheň:** Klávesy WASD (pohyb a skok)
- **Menu:** Myš a klávesa ESC

## Struktura projektu
- `src/`: Zdrojové kódy hry.
- `assets/`: Grafické podklady a ikony.

## Kompilace do .exe
Pro vytvoření spustitelného souboru s vlastní ikonou použijte příkaz:
```bash
pyinstaller --noconsole --onefile --icon=assets/icon.ico --add-data "src;src" src/main.py
```
```
Výsledný soubor naleznete ve složce `dist/`.

---
Autor: piksa.polan
Licence: MIT