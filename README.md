# Fire & Water: Puzzle Adventure

Kooperativní 2D plošinovka pro dva hráče vytvořená v Pythonu a Pygame. Hráč Voda a hráč Oheň sbírají vlastní mince, vyhýbají se nebezpečným zónám a po odemčení dveří musí oba dojít do cíle v časovém limitu.

## Splněné požadavky

- Dokumentace je přímo v repozitáři v souboru `README.md`.
- Kód je objektově orientovaný a rozdělený do logických složek (`src/firewater`, `assets`, `docs`, `scripts`).
- Hra má připravený build do `.exe` pomocí PyInstalleru a používá vlastní ikonu `assets/icon.ico`.
- Mapa struktury projektu, dědičnosti a polymorfismu je níže a samostatně v `docs/project_map.md`.
- Hra obsahuje 5 komplexnějších levelů, z toho levely 4 a 5 používají větší herní plochu, více pohyblivých plošin, hazardů, kuší a kombinované cesty.
- Ve hře je 6 druhů nepřátel: `Enemy`, `FastEnemy`, `HeavyEnemy`, `VerticalEnemy`, `JumperEnemy`, `ZigZagEnemy`.
- Herní menu obsahuje nastavení, fullscreen režim a hra jde v průběhu pauznout.
- Okno hry jde měnit myší; hra se škáluje podle velikosti okna bez změny fyziky levelů.
- Hlavní menu má animované pozadí v tématu oheň/voda a ukázkové animované postavy.
- Hráči mají vlastní animovaný vzhled: Voda používá kapkový tvar, vlny a kapky; Oheň používá plamenný tvar, jiskry a běhové/skokové animace.
- Repozitář je připravený na průběžné commity; příkazy jsou v části Git workflow.

## Spuštění ze zdrojového kódu

```powershell
python -m pip install -r requirements.txt
python src\main.py
```

## Ovládání

- Voda: šipky vlevo/vpravo a šipka nahoru pro skok.
- Oheň: `A`, `D` a `W` pro skok.
- Menu: myš.
- Pauza během hry: `P` nebo `Esc`.
- V pauze lze pokračovat, restartovat level, vrátit se do menu nebo otevřít nastavení.

## Aktuální obsah hry

- 5 asymetrických levelů se zvyšující se obtížností.
- Statické platformy a horizontálně pohyblivé platformy.
- Sběratelné mince zvlášť pro Vodu a Oheň; dveře se odemknou až po sesbírání příslušných mincí.
- Hazardy: láva je nebezpečná pro Vodu, vodní bazény a zelené kyselinové bazény používají vodní typ hazardu a jsou nebezpečné pro Oheň.
- Kuše střílející projektily z okrajů levelu.
- Nepřátelé s různým pohybem: základní patrola, rychlá patrola, těžký pomalý nepřítel, vertikální pohyb, skákání a zig-zag pohyb.
- Stavy hry: hlavní menu, výběr levelu, hraní, pauza, nastavení, dokončení levelu a game over.
- Časový limit lze v nastavení vypnout.
- Fullscreen lze zapnout nebo vypnout v nastavení.
- Levely 1-3 používají základní herní plochu 1200x800, levely 4-5 větší plochu 1500x900.

### Přehled levelů

```text
Level 1: 13 platforem, 6 mincí, 2 hazardy, 0 nepřátel, 0 kuší
Level 2: 16 platforem, 10 mincí, 2 hazardy, 0 nepřátel, 0 kuší
Level 3: 16 platforem, 9 mincí, 0 hazardů, 2 nepřátelé, 2 kuše
Level 4: 17 platforem, 10 mincí, 3 hazardy, 4 nepřátelé, 4 kuše
Level 5: 18 platforem, 10 mincí, 6 hazardů, 4 nepřátelé, 3 kuše
```

## Nastavení

V hlavním menu je tlačítko `SETTINGS`. Stejné nastavení je dostupné i z pauzy během rozehraného levelu.

- `TIMER: ON/OFF`: zapíná nebo vypíná časový limit levelu.
- `FULLSCREEN: ON/OFF`: přepíná hru mezi oknem a fullscreen režimem.
- Okno v režimu bez fullscreen lze ručně zmenšovat a zvětšovat tažením za okraj.

## Build do .exe

```powershell
.\scripts\build_exe.ps1
```

Výsledek se vytvoří jako:

```text
dist\FireWaterPuzzleAdventure.exe
```

Build používá `assets/icon.ico`. Pokud se mění název aplikace nebo ikona, upravte `scripts/build_exe.ps1`.

## Struktura projektu

```text
.
├── assets/
│   └── icon.ico
├── dist/
│   └── FireWaterPuzzleAdventure.exe
├── docs/
│   ├── project_map.md
│   └── legacy_single_file_prototype.py
├── scripts/
│   └── build_exe.ps1
├── src/
│   ├── main.py
│   └── firewater/
│       ├── __init__.py
│       ├── constants.py
│       ├── game.py
│       ├── goals.py
│       ├── levels.py
│       ├── obstacles.py
│       ├── players.py
│       ├── ui.py
│       └── utils.py
├── requirements.txt
└── README.md
```

## Mapa tříd a OOP

```text
Game
├── vlastní pygame okno, resizable/fullscreen režim, hlavní smyčka, stavy hry
├── používá Level, Player, HUD, Button, LevelSelectButton
├── spravuje animované ukázkové postavy v menu
└── volá polymorfně update()/draw() nad objekty levelu

Level
├── skládá konkrétní levely
├── drží seznamy obstacles, coins, enemies, hazard_pools, moving_platforms, buttons, crossbows
├── vytváří asymetrické cesty, mince, hazardy, nepřátele a kuše pro 5 levelů
└── vytváří Door cíle pro hráče Water/Fire

Player
├── zapouzdřuje pozici, rychlost, input, kolize, sběr mincí a kreslení
├── typ hráče určuje ovládání a interakci s hazardy
└── kreslí rozdílnou animovanou vodní a ohnivou postavu

Obstacle
└── MovingPlatform : Obstacle
    ├── dědí obdélníkovou kolizi a základní platformu
    └── přidává pohyb přes update() a vlastní draw()

Button
└── LevelSelectButton : Button
    ├── dědí klikání/hover stav
    └── mění vykreslení podle uzamčení levelu

HUD
├── kreslí herní HUD, hlavní menu, výběr levelu, pauzu, nastavení, game over a dokončení levelu
└── používá draw_fire_water_background() pro animované menu v tématu oheň/voda

Coin, Crossbow, Projectile, HazardPool, Door, ActivationButton
├── samostatné herní objekty se zapouzdřenými daty a metodami
└── používají shodná rozhraní typu update(), draw() nebo check_collision()

Enemy
├── FastEnemy : Enemy
├── HeavyEnemy : Enemy
├── VerticalEnemy : Enemy
├── JumperEnemy : Enemy
└── ZigZagEnemy : Enemy

Vector2
└── datová třída pro vektorovou matematiku hráče

GameState
└── MENU, LEVEL_SELECT, PLAYING, LEVEL_COMPLETE, GAME_OVER, SETTINGS, PAUSED

PlayerType
└── WATER, FIRE
```

### Kde probíhá polymorfismus

- `Game._draw_game()` volá `draw(screen)` nad různými objekty (`Obstacle`, `MovingPlatform`, `Coin`, `Enemy`, `Crossbow`, `HazardPool`, `Door`). Každá třída kreslí jinak, ale hra s nimi pracuje přes stejný název metody.
- `Game.update()` volá `update()` nad nepřáteli, mincemi, hazardy, platformami, tlačítky a kušemi. Implementace se liší podle konkrétní třídy.
- Různé enemy třídy dědí ze základní třídy `Enemy`, ale každá má jiné chování v metodě `update()` nebo jiné parametry pohybu.
- `LevelSelectButton.draw()` přepisuje `Button.draw()`, takže používá dědičnost i polymorfismus.
- `MovingPlatform.draw()` přepisuje `Obstacle.draw()` a zároveň zůstává použitelná jako běžná překážka v kolizním seznamu `Level.obstacles`.

## Git workflow pro jasný progres

V tomto prostředí není příkaz `git` dostupný v PATH, ale jakmile je Git dostupný v terminálu, doporučené průběžné commity jsou:

```powershell
git add src requirements.txt
git commit -m "Reorganize game into src package"

git add assets scripts
git commit -m "Add executable build setup and icon"

git add README.md docs
git commit -m "Document OOP structure and project map"

git add dist\FireWaterPuzzleAdventure.exe
git commit -m "Build Windows executable"
```

Pokud škola nechce verzovat složku `dist`, poslední commit vynechte a odevzdejte `.exe` zvlášť.

## Závislosti

- Python 3.11 nebo novější
- Pygame
- PyInstaller pro sestavení `.exe`
