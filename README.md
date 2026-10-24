# Veni, Vidi, Vici (VVV) ⚔️
Tactical warfare mod for **vanilla Crusader Kings III**.

**Version:** 0.1.2-alpha | **Target:** CK3 1.20.x

## What is implemented
- Custom **2D three-lane battlefield sandbox** inside the CK3 map GUI.
- A friendly regiment token can move between the left, centre and right lanes.
- Orders: deploy left/centre/right, hold, charge, advance a drill turn.
- Save-persistent character variables for lane, round, morale, momentum and risk.
- A player-only decision to initialize the exercise.
- A separate deterministic Python tactics **rules lab**, with unit tests.

**IMPORTANT:** This is not yet connected to live CK3 armies. CK3 combat still resolves normally. No active battles, regiments or casualties are modified by this alpha.

## Installation
1. Run `python -m tools.package` and extract `dist/VVV-0.1.2.zip` into `Documents/Paradox Interactive/Crusader Kings III/mod/` (so `mod/VVV/descriptor.mod` exists).
2. Check that `VVV.mod` is alongside the `VVV` folder. This package excludes development tools, tests, documentation and Git files.
3. Enable the mod in the CK3 launcher and load a vanilla campaign.
4. **For UI testing only**, start CK3 with `-debug_mode`. The compact `Tactics` button appears on the map **only in debug mode**, never in ordinary gameplay. Open it, then press **Reset drill**.
5. Check `logs/error.log` if the interface fails to show. This first implementation still requires live-game smoke testing.

## Offline development tests (Python 3.10+)
```bash
python -m unittest discover -s tests -v
python -m tools.tactics
```
Python is a stand-alone testbed; it does **not** execute inside CK3.

See [Architecture](docs/ARCHITECTURE.md), [Testing](docs/TESTING.md), [Roadmap](docs/ROADMAP.md), and [Engine limitations](docs/LIMITATIONS.md).

For a private Steam Workshop upload, follow [the upload checklist](docs/UPLOAD.md).

## Visual update (v0.1.1)
- Main tactics window anchored at the screen **center** with a smaller **Tactics** map button.
- Original parchment battlefield graphic, enemy and friendly regiment counter art, front-line labels and terrain sectors.
- Reset prompt while no drill is initialized. **Click Reset drill** once to spawn the blue counter; the initial 0/0/0/0 display is expected before initialization.
- These assets belong to VVV and must be present in the packaged mod under `gfx/interface/vvv/`.
- **Divine Intervention compatibility:** no vanilla GUI files are replaced, but UI overlap and scripted GUI interactions still require a combined-mod smoke test.

## v0.1.2 interface refresh
- 1090 × 606 centered window with **distinct left instruction, middle illustrated battlefield and right order/status regions**.
- Newly generated, opaque **RGB/truecolor field and army counter textures** replace the subdued paletted graphics that were hard to read.
- Uses CK3 standard clickable buttons for orders and scripted-UI lane state, leaving normal battles untouched.
- **No global Tactics button in regular games.** Debugging with `-debug_mode` exposes a temporary opener to test the layout; battle-window integration needs a separate, version-specific vanilla GUI hook.
- If your game displays the map but does not update drill values when pressing Reset, send `logs/error.log`. That is a scripting issue, not a graphic issue.
