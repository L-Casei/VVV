# Roadmap

## 0.1 (this commit)
- [x] Vanilla CK3 descriptors, decision and tutorial event
- [x] Standalone native 2D lane panel
- [x] Orders change a unit marker and saved character state
- [x] Independent rules-lab with tests
- [ ] Validate syntax and scale in CK3 1.20.x itself

## 0.2
- [ ] Separate mock regiments (selection, occupancy and movement)
- [ ] Real terrain templates and morale-based routes
- [ ] Attacks from flanks and ordered reserves
- [ ] Automatic drill AI

## 0.3 feasibility gate
- [ ] Observe `on_combat_start` scopes with debug logs
- [ ] Test pausing/advancing real battles and reading their regiments
- [ ] Test result override and proper casualty reconciliation
- [ ] Decide if a fully native overlay is possible or if an external tactical engine is needed

## 0.4+
- [ ] Commander position, wounds, capture, death risk
- [ ] Combat AI doctrines, weather and terrain
- [ ] Manual/auto switch and stability for saves

## v0.1.2 visual acceptance gate
- [x] Rebuild 3-column panel hierarchy around one readable tactical board
- [x] Replace palette artwork with opaque 24-bit field and formation plates
- [x] Hide the global opener except in debug mode
- [ ] In-game screenshot confirmation (CK3 GUI scripting cannot be verified by GitHub CI)
- [ ] Locate and inspect the *actual* CK3 battle view GUI, then place Tactics beside battle actions rather than on world-map HUD
- [ ] Test coexistence with Divine Intervention
