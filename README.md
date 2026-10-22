# Veni, Vidi, Vici (VVV) ⚔️
Tactical warfare mod for **vanilla Crusader Kings III**.

**Version:** 0.1.0-alpha | **Target:** CK3 1.20.x

## What is implemented
- Custom **2D three-lane battlefield sandbox** inside the CK3 map GUI.
- A friendly regiment token can move between the left, centre and right lanes.
- Orders: deploy left/centre/right, hold, charge, advance a drill turn.
- Save-persistent character variables for lane, round, morale, momentum and risk.
- A player-only decision to initialize the exercise.
- A separate deterministic Python tactics **rules lab**, with unit tests.

**IMPORTANT:** This is not yet connected to live CK3 armies. CK3 combat still resolves normally. No active battles, regiments or casualties are modified by this alpha.

## Installation
1. Run `python -m tools.package` and extract `dist/VVV-0.1.0.zip` into `Documents/Paradox Interactive/Crusader Kings III/mod/` (so `mod/VVV/descriptor.mod` exists).
2. Check that `VVV.mod` is alongside the `VVV` folder. This package excludes development tools, tests, documentation and Git files.
3. Enable the mod in the CK3 launcher and load a vanilla campaign.
4. Click **VVV: Tactics** on the map, then **Reset drill**. Or use the *Tactical Field Exercise* decision.
5. Check `logs/error.log` if the interface fails to show. This first implementation still requires live-game smoke testing.

## Offline development tests (Python 3.10+)
```bash
python -m unittest discover -s tests -v
python -m tools.tactics
```
Python is a stand-alone testbed; it does **not** execute inside CK3.

See [Architecture](docs/ARCHITECTURE.md), [Testing](docs/TESTING.md), [Roadmap](docs/ROADMAP.md), and [Engine limitations](docs/LIMITATIONS.md).

For a private Steam Workshop upload, follow [the upload checklist](docs/UPLOAD.md).
