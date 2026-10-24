# Battle-window Tactics button

## Implementation

`tools/install_battle_button.py` reads **the user's installed** `game/gui/window_combat.gui` and writes the patched version to **VVV's** `gui/window_combat.gui`.

The insertion is a `vvv_battle_tactics_button` inside the native `buttons_window_control` row's `blockoverride "extra_buttons"`. The row handles placement beside the existing controls; there is no floating normal-play HUD button. The reusable VVV button type lives in `gui/vvv_battle_button.gui`.

The source scan checks balanced braces, one top-level `combat_window` and one window-control row. Strings and comments do not affect brace matching. Existing extra buttons are preserved. Applying the patch twice does not duplicate it. Unknown structures fail without writing.

The source/target paths must differ. A foreign existing override is never overwritten. A VVV override that differs from the current game source requires `--refresh`, which creates a backup first.

## Setup

On Windows, double-click `InstallBattleButton.cmd` in VVV. Python 3.10+ is required. Steam and additional Steam libraries are detected automatically.

Alternatively:

```bash
python -m tools.install_battle_button --game-dir "D:/SteamLibrary/steamapps/common/Crusader Kings III"
```

Use `--mod-dir` if installing into a different VVV folder. After a CK3 update:

```bash
python -m tools.install_battle_button --refresh
```

The generated override is ignored by Git. If generated before packaging, it is included in the local installation ZIP. A CI ZIP needs the installer run after extraction because CI has no CK3 installation.

## Scope and compatibility

The button is a child of the actual battle view, so its lifetime follows that view. It opens the example board, auto-initializes missing drill state, and does not mutate the battle.

There is no participation-only filter yet: a battle visible to the player can offer the drill button. The armies remain the declared examples rather than that battle's combatants.

Another mod replacing `window_combat.gui` needs a merged file. Divine Intervention's main GUI was inspected and is separate from this battle-window file, but combined behavior still requires a live-game smoke test.

## Verification status

The patcher has automated preservation, duplicate-prevention, rejection and filesystem tests. It was also applied offline to a public **1.18.2** reference combat GUI, which confirms the insertion structure, not compatibility with the user's current game. Runtime visibility, native type loading and button spacing must be verified in CK3 1.20.x.
