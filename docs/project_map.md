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
- `Level`: vytváří mapy levelů a drží kolekce herních objektů.
- `Player`: řeší ovládání, gravitaci, kolize, sběr mincí a vykreslení hráče.
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
- `HUD`: vykresluje menu, HUD, dokončení levelu a game over.
- `Vector2`: jednoduchá datová třída pro výpočty pozice a rychlosti.

## Polymorfismus

Polymorfismus je použitý hlavně přes shodné metody `draw()` a `update()`:

```python
for obstacle in self.level.obstacles:
    obstacle.draw(self.screen)
```

V seznamu mohou být instance `Obstacle` i `MovingPlatform`. Hra volá stejnou metodu, ale konkrétní objekt rozhodne, jak se vykreslí.

Další příklad je `LevelSelectButton.draw()`, které přepisuje `Button.draw()`. Objekt se stále používá jako tlačítko, ale vykreslení se změní podle toho, jestli je level odemčený.

Enemy třídy používají dědičnost ze základní třídy `Enemy`. Hra nad nimi volá stejné metody `update()`, `draw()` a `check_collision()`, ale jednotlivé podtřídy mají jiné chování.
