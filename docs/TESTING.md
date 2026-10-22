# Smoke tests

## Static (Python 3.10+)
```bash
python -m unittest discover -s tests -v
python -m tools.tactics
```

## CK3 (required before claiming game compatibility)
1. Install, load vanilla 867/1066, enable the mod.
2. Find **VVV: Tactics / VVV: Tactica** in the map HUD.
3. Open/close panel repeatedly, press **Reset drill**.
4. Ensure only one player regiment marker appears (middle lane).
5. Click deploy left/centre/right: token should change lanes.
6. Hold and charge should change the displayed morale/momentum/risk.
7. Advance turn and confirm turn counter updates.
8. Save/reload: drill character variables should persist. Window open state is client-local.
9. In Decisions, use **Tactical Field Exercise**. It should start the drill via event.
10. Start a normal CK3 battle: it must still be vanilla.
11. Run `-debug_mode` and read `Documents/Paradox Interactive/Crusader Kings III/logs/error.log`. Report any `VVV`, GUI or script errors with game version.

Source checks are not equivalent to the game's actual parser. UI still needs a first live smoke test.
