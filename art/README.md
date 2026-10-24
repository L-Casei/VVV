# Tactical board artwork

The built-in image-generation tool created these project assets from the user's supplied battlefield reference. They are not copied from another mod.

Sources:

- `art/source/plains.png`: empty overhead plains background, 1774×887 RGB.
- `art/source/formations.png`: transparent 3×2 sprite atlas, 1536×1024 RGBA.

Compile with Pillow 11.3+:

```bash
python -m tools.build_art
```

Output: `gfx/interface/vvv/plains.dds` (1536×768, legacy DXT1) and six `<team>_<troop>.dds` sprites (256×224, legacy DXT5). The crop coordinates align the blank plaques; native GUI text supplies counts. Runtime packages exclude source PNGs.

The compiler normalizes the compressed surface's `dwPitchOrLinearSize` to its full byte count, as defined by Microsoft's [DDS header specification](https://learn.microsoft.com/windows/win32/direct3ddds/dds-header). Static validation checks it as well as the FourCC and pixel data size.

## Generation prompts

**Terrain — built-in image tool, reference image attached, opaque background:**

> Use case: precise-object-edit. Asset type: production background texture for the 2D CK3 Veni Vidi Vici tactical battlefield GUI. Input image 1 is the edit target and exact art reference. Make a clean EMPTY version of this same hand-painted overhead green plain battlefield. REMOVE ALL red and blue soldiers, all troop icons, badges, banners, numerical labels and every UI element. Seamlessly restore grass beneath them. Preserve the fine hand-painted medieval map aesthetic, olive green grass, rocks, clustered trees on the outer edges, narrow river at far right and small wooden bridge. Landscape output aspect ratio 2:1. Pure flat 2D overhead/plan view: no perspective horizon, no 3D camera. Keep the central 75% as very open lightly textured grass, with clear empty deployment areas in the upper and lower parts. The terrain is a plain: trees and rocks are decorative on edges only, no large terrain obstacles in the central arena. Full bleed terrain to all edges. No text, numbers, grid lines, panels, frames, soldiers, symbols or UI anywhere.

**Formations — built-in image tool, reference image attached, transparent background:**

> Use case: background-extraction. Asset type: transparent sprite atlas for a 2D CK3 medieval tactical game interface. Input image 1 is the style and content reference. Produce a clean uniform 3 column by 2 row sprite sheet on a genuinely transparent background, wide 3:2 canvas, six equally sized cells with generous transparent gaps, no objects crossing a cell boundary. Each cell is an independent regiment formation in the same style as the reference: small hand-painted flat symbolic medieval soldiers viewed as simple upright tokens, crisp dark outlines, muted gold metal highlights. TOP ROW RED troops, BOTTOM ROW BLUE troops. Column 1 archers: 3 rows of 6 tiny bow-and-quiver soldier symbols, bow medallion above. Column 2 levies: 3 rows of 8 tiny shield-and-sword soldiers, crossed swords medallion above. Column 3 light infantry: 3 rows of 6 tiny spearmen, spear medallion above. All six formations have a small centered circular bronze-rimmed troop-type medallion above their heads, with a blank dark rectangular bronze-rimmed number plaque just below the medallion and above the soldiers. Absolutely NO letters or numbers, leave those plaques blank for native game text. Keep all badge/plaque positions and sizes CONSISTENT across the six cells. Preserve clear red vs blue uniforms. Not realistic figures, not 3D units, no large humans, simple readable miniature army symbols faithful to the attached reference. Absolutely NO landscape, ground plane, backdrop, decorative frame around the sheet, separator lines, words, labels or numbers. Genuine transparent alpha between and behind every group. Each group neatly centered in its own cell.
