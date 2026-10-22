# Technical honesty

This repository contains a **native CK3 GUI drill** and a separate Python combat prototype, not a full replacement battle engine.

- CK3 does not execute Python code from a mod.
- `on_combat_start`, `set_winner` and `force_win` exist in modern game scripting, but that does not prove we can pause real combat, intercept all casualties, or step it manually.
- Map GUI has fixed coordinates and requires an in-game smoke test. No live CK3 instance is available here.
- The lane board represents abstract positions rather than actual armies.
- Auto battles stay untouched by design. No vanilla files are overwritten.
