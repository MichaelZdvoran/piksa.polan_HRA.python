# Mapa struktury projektu

## Spouštěcí tok

```text
src/main.py
└── firewater.game.Game
    ├── handle_events()
    ├── update()
    ├── draw()
    └── run()
```

## Soubory

- `src/main.py`: jednoduchý vstupní bod, spustí `Game().run()`.
- `src/firewater/constants.py`: rozměry okna, FPS, fyzika, barvy a enumy `PlayerType` a `GameState`.
- `src/firewater/game.py`: hlavní pygame okno, herní smyčka, přepínání stavů, input, aktualizace a vykreslení.
- `src/firewater/levels.py`: definice 5 asymetrických levelů a pomocné metody pro platformy, mince, dveře a kuše.
- `src/firewater/players.py`: logika hráčů, fyzika, kolize, sběr mincí a animované vykreslení Vody/Ohně.
- `src/firewater/obstacles.py`: platformy, mince, nepřátelé, kuše, projektily, hazardy a dveře.
- `src/firewater/ui.py`: tlačítka, HUD, menu, nastavení, pauza a animované pozadí menu.
- `src/firewater/utils.py`: datová třída `Vector2`.
- `src/firewater/goals.py`: starší třída `Goal`; aktuální levely používají `Door` z `obstacles.py`.
- `assets/icon.ico`: ikona pro sestavené `.exe`.
- `scripts/build_exe.ps1`: build skript pro PyInstaller.
- `docs/legacy_single_file_prototype.py`: starší jednosouborový prototyp pro porovnání.

## Dědičnost

```text
Obstacle
└── MovingPlatform

Button
└── LevelSelectButton

Enemy
├── FastEnemy
├── HeavyEnemy
├── VerticalEnemy
├── JumperEnemy
└── ZigZagEnemy
```

## Účel tříd

- `Game`: řídí hlavní smyčku, menu, nastavení, pauzu, výběr levelů, průběh hry, konec levelu a game over.
- `Level`: vytváří 5 asymetrických levelů a drží kolekce herních objektů.
- `Player`: řeší ovládání, gravitaci, kolize, sběr mincí a animované vykreslení vodní nebo ohnivé postavy.
- `Obstacle`: statická pevná překážka nebo speciální platforma podle typu.
- `MovingPlatform`: pohyblivá překážka, která dědí z `Obstacle`.
- `Coin`: sběratelný předmět pro konkrétní typ hráče.
- `Enemy`: patrolující nepřítel s kolizí proti hráči.
- `FastEnemy`: rychlejší horizontální nepřítel.
- `HeavyEnemy`: větší a pomalejší nepřítel.
- `VerticalEnemy`: nepřítel pohybující se nahoru a dolů.
- `JumperEnemy`: patrolující nepřítel s pravidelným skákáním.
- `ZigZagEnemy`: nepřítel kombinující horizontální pohyb s vlněním.
- `Crossbow` a `Projectile`: střelecká překážka a její projektily.
- `HazardPool`: láva, voda nebo kyselina; podle typu hráče rozhoduje, jestli je nebezpečná.
- `Door`: cílové dveře, které se odemknou po sesbírání mincí.
- `Button` a `LevelSelectButton`: UI prvky menu.
- `HUD`: vykresluje menu, HUD, výběr levelu, pauzu, nastavení, dokončení levelu a game over.
- `draw_fire_water_background()`: kreslí animované pozadí hlavního menu v tématu oheň/voda.
- `Vector2`: jednoduchá datová třída pro výpočty pozice a rychlosti.
- `GameState`: enum stavů `MENU`, `LEVEL_SELECT`, `PLAYING`, `LEVEL_COMPLETE`, `GAME_OVER`, `SETTINGS`, `PAUSED`.
- `PlayerType`: enum typů hráčů `WATER` a `FIRE`.

## Herní obsah

```text
Levely: 5
Hráči: Water a Fire
Hazardy: lava, water, acid
UI stavy: menu, výběr levelu, hraní, pauza, nastavení, dokončení levelu, game over
Nastavení: TIMER ON/OFF
Build: PyInstaller one-file exe se souborem assets/icon.ico
```

```text
Level 1: 14 platforem, 9 mincí, 3 hazardy, 2 nepřátelé, 1 kuše
Level 2: 14 platforem, 9 mincí, 4 hazardy, 2 nepřátelé, 1 kuše
Level 3: 14 platforem, 8 mincí, 5 hazardů, 3 nepřátelé, 2 kuše
Level 4: 16 platforem, 8 mincí, 5 hazardů, 3 nepřátelé, 2 kuše
Level 5: 18 platforem, 10 mincí, 6 hazardů, 4 nepřátelé, 3 kuše
```

## Polymorfismus

Polymorfismus je použitý hlavně přes shodné metody `draw()` a `update()`:

```python
for obstacle in self.level.obstacles:
    obstacle.draw(self.screen)
```

V seznamu mohou být instance `Obstacle` i `MovingPlatform`. Hra volá stejnou metodu, ale konkrétní objekt rozhodne, jak se vykreslí.

Další příklad je `LevelSelectButton.draw()`, které přepisuje `Button.draw()`. Objekt se stále používá jako tlačítko, ale vykreslení se změní podle toho, jestli je level odemčený.

Enemy třídy používají dědičnost ze základní třídy `Enemy`. Hra nad nimi volá stejné metody `update()`, `draw()` a `check_collision()`, ale jednotlivé podtřídy mají jiné chování.
