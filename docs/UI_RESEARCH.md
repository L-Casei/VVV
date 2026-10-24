# UI research for v0.1.3

## Evidence

The supplied in-game screenshot shows labels and buttons, but none of the custom field/counter artwork. The previous GUI referenced PNG files and forced `spriteType = Texture`. The missing imagery is consistent with failed texture loading; without the user's game log, that specific engine error cannot be proven.

Inspected primary implementation sources:

- [Divine Intervention — DI_main.gui](https://github.com/Lithane97/Divine-Intervention-Base/blob/master/gui/DI_main.gui): native windows, standard buttons, UI-variable visibility, and multiple onclick actions.
- [CK3 reference combat view](https://github.com/jesec/ck3-mod-base/blob/master/base/game/gui/window_combat.gui): `combat_window`, DDS textures and the native window-control row.
- [CK3 reference button types](https://github.com/jesec/ck3-mod-base/blob/master/base/game/gui/shared/buttons.gui): `buttons_window_control` is a flowcontainer with an `extra_buttons` extension block.
- [CK3 reference window templates](https://github.com/jesec/ck3-mod-base/blob/master/base/game/gui/shared/windows.gui): native window layers/background conventions.

The public reference combat GUI's latest file change was **1.18.2, 2025-12-11** when inspected. It is useful for structure, not a verified 1.20 source. The installer therefore patches the user's current local file and checks for the expected structure instead of shipping that reference as an override.

## Resulting changes

1. Use standard texture-backed icons with legacy DDS DXT1 for opaque terrain and DXT5 for alpha sprites. Remove the unverified forced sprite type.
2. Give the board nearly the full width; put actions/status in a compact footer.
3. Keep the terrain, six formations and count text separate so future battle-data bindings can replace example values.
4. Use character-scoped scripted GUI actions, following the established native pattern.
5. Place the optional entry button in the battle view's native extra-button block, preserving its other controls.
6. Retain an explicitly debug-only fallback for investigating rendering separately from integration.

All VVV artwork in this update is generated for this project from the user's reference. No third-party mod art is copied.
