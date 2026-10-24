# Tactics v0.1.3 acceptance test

## Automated checks

- Static Clausewitz brace/string balance and localization BOM/duplicate checks.
- Every custom GUI texture exists, uses a legacy DDS header, declares DXT1 or DXT5, and contains the expected minimum pixel data.
- Battle patch preserves native controls and existing extra buttons, refuses ambiguous/broken input and foreign overrides, and never edits the game file.
- Separate deterministic Python combat rules lab.
- Install ZIP contains the board, all seven DDS textures and local setup helper; it excludes art sources and development previews.

These checks cannot certify CK3's GUI parser or runtime behavior.

## In-game check

1. Update VVV and run `InstallBattleButton.cmd` (or `python -m tools.install_battle_button`) in its folder.
2. Fully exit and restart CK3; stale textures can remain cached.
3. Load a vanilla campaign and open an active battle. Tactics should be in the battle window's control row.
4. Open Tactics: the **1060×672** panel should be centered, with a **1024×512** field and six formations immediately visible.
5. Red counts, left to right: **150 / 600 / 200**. Blue counts: **200 / 1000 / 300**.
6. Check troop alpha: the grass must be visible between soldiers, with no opaque black rectangle.
7. Click each blue unit. Its gold underline and selected-unit footer should update.
8. Try each flank command. The selected formation trades places with the occupant; no two blue groups overlap.
9. Hold/Charge change drill metrics; Advance turn increments the turn. Reset restores the example deployment and morale 80.
10. Close and reopen: current drill state remains. Older 0.1.2 saves initialize the new board on first opening.
11. Verify native battle controls and ordinary combat still work. Repeat with Divine Intervention enabled.
12. Without `-debug_mode`, there must be **no standalone Tactics button on the map**.
13. Check 1366×768 and your normal resolution/UI scale. Inspect number alignment and control-row spacing.

The optional debug-mode map opener is retained to test art independently of the local battle hook. The offline preview approximates native skins/fonts and must not be treated as an in-game screenshot.

If something fails, inspect `Documents/Paradox Interactive/Crusader Kings III/logs/error.log` and capture the first VVV-related errors with a screenshot.
