# Architecture

The scripted widget `vvv_battlefield` owns the board. A client UI variable toggles its visibility. A local installer adds a reusable button to the native battle view; a debug-only map button provides independent access while developing.

The terrain is one opaque DXT1 DDS. Six separate DXT5 textures contain formations and blank number plaques. Native text displays six saved strength variables. Nine conditional blue widgets cover three troop types × three lane positions; only one per troop type is visible. Clicking a blue formation changes the selected type. Flank orders swap lane assignments to prevent overlap.

Player-character state:

- `vvv_board_ready`, `vvv_drill_active`
- `vvv_selected_unit`: 0 archers, 1 levies, 2 light infantry
- `vvv_archers_lane`, `vvv_levies_lane`, `vvv_light_infantry_lane`: 0 left, 1 centre, 2 right
- `vvv_lane`: selected formation's lane, retained for alpha continuity
- `vvv_red_<troop>_count` and `vvv_blue_<troop>_count`
- `vvv_round`, `vvv_morale`, `vvv_momentum`, `vvv_risk`

Opening the board calls `vvv_prepare_board_effect`, which initializes a new or old-alpha save once. Reset explicitly restores all example state.

`tools/build_art.py` compiles the two checked-in source images. `tools/preview_ui.py` reads actual GUI coordinates, default script values, localizations and DDSs to produce an offline layout check. Its window/button skins and fonts are approximations.

The installer and package builder run outside CK3. The independent `tools/tactics.py` rules lab remains separate from CK3's runtime.

Real battle participants, combat scopes, pausing and casualty reconciliation are not connected to the drill.
