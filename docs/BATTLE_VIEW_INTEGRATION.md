# Real battle button integration (not implemented yet)

**Requirement:** The player opens Tactics from the active CK3 **battle window**, not from the map or a permanent HUD element.

## Why the current alpha stays in debug mode
A standalone `gui/scripted_widgets` window is created on the world map. It cannot magically attach to any battle pane. Vanilla CK3 battle windows are game-version-specific, so blindly replacing their entire GUI file would create likely compatibility problems with other mods, including Divine Intervention.

## Implementation gate
1. Inspect the vanilla **1.20.x** battle view with `gui.debug`. This displays the exact `.gui` file and widget responsible for battle buttons.
2. Capture the widget hierarchy and the datacontext for the currently selected battle. Test whether it exposes the player's participation in that battle.
3. Insert a **Tactics** button next to the native battle commands. Prefer a type/template hook if available; otherwise make a version-pinned, explicitly documented compatibility override.
4. Gate the button to relevant battles (not every siege, and not inactive wars).
5. Open the same sandbox through the button. Only after battle visibility has been validated, connect combat scopes, unit data and results.
6. When that button works, remove the debug HUD widget entirely.

Do **not** claim the battle menu is integrated until a live CK3 test proves it.
