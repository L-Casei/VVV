# CK3 tactical drill v0.1.1 test checklist

## Already verified by user's screenshot
- The v0.1.0 custom CK3 panel opens on the map, and the standalone button appears.
- Window positioning on 1366×727 was unsatisfactory (too far left).
- An uninitialized drill shows all counters at 0 and no own regiment marker.

## Required for updated 0.1.1
1. Reload CK3 with v0.1.1 installed, ideally with `-debug_mode -develop`.
2. Verify compact **Tactics** button and **centered** field panel, on a 1366×727 monitor.
3. Verify the map image is visible and red formation counters render.
4. Press **Reset drill**: one blue formation must appear in the centre; morale starts at 80.
5. Press left/right/centre; blue formation should move between three fixed slots.
6. Charge and hold should adjust the numbers. Next turn increases turn count.
7. Verify Spanish localization and correct closing/reopening behavior.
8. Enable **Divine Intervention** alongside VVV, load a new game, and repeat steps 2–6.
9. Fight a normal CK3 battle; combat must stay unchanged.
10. Inspect `Documents/Paradox Interactive/Crusader Kings III/logs/error.log`, especially errors referencing `vvv_`, `GuiScope`, `Window_Background`, or the PNG assets.

### Before reporting a failure
If the blue counter does not spawn after clicking Reset, send the first VVV-related error lines and the game version. The panel rendering does not prove that scripted GUI effects are executing.

## Static verification (Python 3.10+)
```bash
python -m unittest discover -s tests -v
python -m tools.package
```
