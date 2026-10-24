# Current limitations

- This is a native CK3 **example tactical board**, not a replacement battle engine.
- The displayed 1,500 blue and 950 red soldiers are fixed example strengths. Symbols illustrate formations and do not map one-to-one to soldiers.
- Commands change only drill variables. Real CK3 battles and casualties continue normally.
- Python does not run inside CK3. It is used for setup, packaging, artwork and a separate rules lab.
- The battle button needs a local override generated from the user's own game files. No complete vanilla combat GUI is redistributed.
- A mod replacing the same combat GUI needs a merged compatibility file.
- The plain's edge trees, river and bridge are decorative; no terrain collision or movement cost is implemented.
- The offline preview proves asset composition and source coordinates, not CK3 parser acceptance. No live CK3 instance is available in this environment.
- Exact layout at different UI scales, battle-control spacing and coexistence with Divine Intervention need an in-game check.
