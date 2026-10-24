# Tactics v0.1.2 | UI acceptance test

## Context
This build responds to the unreadable, badly placed v0.1.1 interface in a live vanilla/Divine Intervention campaign.

## Start
1. Update the mod, **close and restart CK3** (textures can stay cached otherwise).
2. Launch CK3 with `-debug_mode` in its Steam launch options.
3. Start/load a vanilla campaign (you can leave Divine Intervention active in a second run).
4. Locate the small `Tactics` debug opener bottom-right. **It is hidden in normal mode.**
5. Open the 1090×606 central tactics panel. Check the battle map renders as a **light, opaque, readable** field rather than dark see-through shadow.
6. Confirm left instructions / centre terrain and banners / right commands don't overlap at 1366×768 and 1647×896 screen resolutions.
7. Press `Reset drill`; check centre blue marker appears, morale becomes 80, round is 0.
8. Press Deploy left, centre, right. Watch the blue marker change lanes.
9. Verify Hold / Charge modify sandbox variables; Next advances the round.
10. Fight a normal CK3 battle. It must remain vanilla.
11. Close the game, remove `-debug_mode`, restart. **There must be no persistent Tactics button in the world-map HUD.**

## Important limitations
This is **not yet** the final battle-window button. The correct version-dependent vanilla CK3 battle GUI file, battle model scope and interaction must be checked before overwriting the game GUI; this prototype deliberately avoids a fragile blind override.

If rendering or the drill actions fail, send the first relevant lines from `Documents/Paradox Interactive/Crusader Kings III/logs/error.log` plus a screenshot.
