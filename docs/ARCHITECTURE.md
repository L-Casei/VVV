# Architecture

```text
game GUI scripted_widgets registration
 |-> map HUD toggle (client-only UI variable)
 |-> symbolic 2D field panel
      |-> scripted_gui commands, character-scoped
           |-> scripted_effects -> vvv_* player variables (saved)
Decision -> briefing event -> initialize drill

Offline rules lab (not CK3 runtime):
 tools/tactics.py + tests/
```

**Player-character state:** `vvv_drill_active`, `vvv_lane` (0 left, 1 center, 2 right), `vvv_round`, `vvv_morale`, `vvv_momentum`, `vvv_risk`. The GUI positions a single mock regiment based on the lane number. No real military units are read, selected or modified.

The bridge to real battles is intentionally absent until on_combat_start root scopes, pausing behavior and casualty reconciliation are tested in a real CK3 build.
