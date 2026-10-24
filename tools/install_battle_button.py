"""Add Tactics to the locally installed CK3 combat window, without editing CK3.

The complete vanilla GUI is deliberately not redistributed in this repository.
The patch uses the user's current game file, preserving its other controls.
"""
import argparse
import os
from pathlib import Path
import re

from tools.validate import ROOT, balanced

MARKER = "# VVV battle-window hook"
BUTTON = "vvv_battle_tactics_button = {}"


def masked(text):
    """Hide strings/comments while preserving offsets and structural braces."""
    return re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*',
                  lambda match: " " * len(match[0]), text)


def patch_combat_window(source):
    if not balanced(source):
        raise ValueError("The combat GUI has unbalanced braces or strings; no file written.")
    code = masked(source)
    if re.search(r"\bvvv_battle_tactics_button\s*=", code):
        return source
    # Locate only top-level windows, ignoring nested widgets and misleading comments.
    depth = 0
    openings = {}
    for match in re.finditer(r"\bwindow\s*=\s*\{|[{}]", code):
        token = match[0]
        if token.startswith("window"):
            if depth == 0:
                openings[depth, match.end() - 1] = match.end() - 1
            depth += 1
        elif token == "{":
            depth += 1
        else:
            depth -= 1
    candidates = []
    for opening in openings.values():
        level = 1
        closing = None
        for index in range(opening + 1, len(code)):
            if code[index] == "{":
                level += 1
            elif code[index] == "}":
                level -= 1
                if level == 0:
                    closing = index
                    break
        if closing is None:
            continue
        # The root's name must precede any nested block.
        prefix = source[opening + 1:closing].split("{", 1)[0]
        prefix = re.sub(r"#[^\n]*", "", prefix)
        if re.search(r'\bname\s*=\s*"combat_window"', prefix):
            candidates.append((opening, closing))
    if len(candidates) != 1:
        raise ValueError("Expected exactly one top-level combat_window; no file written.")
    newline = "\r\n" if "\r\n" in source else "\n"
    opening, closing = candidates[0]
    controls = list(re.finditer(r"\bbuttons_window_control\s*=\s*\{", code[opening:closing]))
    if len(controls) != 1:
        raise ValueError("Expected one native battle window-control row; no file written.")
    control_opening = opening + controls[0].end() - 1

    def matching_close(start):
        level = 1
        for index in range(start + 1, closing):
            if code[index] == '{':
                level += 1
            elif code[index] == '}':
                level -= 1
                if level == 0:
                    return index
        raise ValueError("Unclosed battle window controls; no file written.")

    control_closing = matching_close(control_opening)
    existing = list(re.finditer(r'blockoverride\s+"extra_buttons"\s*\{',
                               source[control_opening:control_closing]))
    if len(existing) > 1:
        raise ValueError("Ambiguous extra_buttons override; no file written.")
    if existing:
        extra_opening = control_opening + existing[0].end() - 1
        closing = matching_close(extra_opening)
        insertion = f"\t\t\t{MARKER}{newline}\t\t\t{BUTTON}{newline}\t\t"
    else:
        closing = control_closing
        insertion = (f'\t\t{MARKER}{newline}\t\tblockoverride "extra_buttons"{newline}'
                     f'\t\t{{{newline}\t\t\t{BUTTON}{newline}\t\t}}{newline}\t')
    return source[:closing] + insertion + source[closing:]


def find_game_dir():
    candidates = []
    if os.environ.get("CK3_GAME_DIR"):
        candidates.append(Path(os.environ["CK3_GAME_DIR"]))
    steam_roots = [Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Steam"]
    if os.name == "nt":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
                steam_roots.append(Path(winreg.QueryValueEx(key, "SteamPath")[0]))
        except OSError:
            pass
    else:
        steam_roots += [Path.home() / ".steam/steam", Path.home() / ".local/share/Steam",
                        Path.home() / "Library/Application Support/Steam"]
    for steam in list(steam_roots):
        library_file = steam / "steamapps/libraryfolders.vdf"
        if library_file.is_file():
            libraries = re.findall(r'"path"\s*"([^"\n]+)"', library_file.read_text(encoding="utf-8"))
            steam_roots += [Path(path.replace("\\\\", "\\")) for path in libraries]
    for steam in steam_roots:
        candidates.append(steam / "steamapps/common/Crusader Kings III")
    for candidate in candidates:
        if (candidate / "game/gui/window_combat.gui").is_file():
            return candidate
        if (candidate / "gui/window_combat.gui").is_file():
            return candidate
    return None


def install(game_dir, mod_dir=ROOT, force=False):
    game_dir, mod_dir = Path(game_dir), Path(mod_dir)
    candidates = (game_dir / "game/gui/window_combat.gui", game_dir / "gui/window_combat.gui")
    source = next((path for path in candidates if path.is_file()), None)
    if source is None:
        raise ValueError("No game/gui/window_combat.gui found. Pass CK3's installation folder.")
    destination = mod_dir / "gui/window_combat.gui"
    if source.resolve() == destination.resolve():
        raise ValueError("The destination must be the VVV mod folder, never the game folder.")
    content = source.read_bytes().decode("utf-8-sig")
    patched = patch_combat_window(content)
    if destination.exists():
        current = destination.read_bytes().decode("utf-8-sig")
        if current == patched:
            print(f"Battle button is already up to date: {destination}")
            return destination
        if MARKER not in current or not balanced(current):
            raise ValueError("Existing GUI override is not managed by VVV; no file overwritten.")
        if not force:
            raise ValueError("The game GUI changed. Re-run with --refresh to back up and refresh VVV's override.")
        backup = destination.with_suffix(".gui.vvv-backup")
        if backup.exists():
            raise ValueError(f"Keep or move the previous backup first: {backup}")
        backup.write_bytes(destination.read_bytes())
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(b"\xef\xbb\xbf" + patched.encode("utf-8"))
    print(f"Installed battle-menu Tactics button: {destination}")
    print("CK3's own files were not changed. Restart CK3. Rebuild after game updates.")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-dir", type=Path, help="CK3 installation folder; Steam is auto-detected if omitted")
    parser.add_argument("--mod-dir", type=Path, default=ROOT, help="VVV folder containing descriptor.mod")
    parser.add_argument("--refresh", action="store_true", help="Back up and refresh an earlier VVV override")
    args = parser.parse_args()
    game_dir = args.game_dir or find_game_dir()
    if game_dir is None:
        parser.error('CK3 was not found. Use --game-dir "D:/SteamLibrary/steamapps/common/Crusader Kings III"')
    if not (args.mod_dir / "descriptor.mod").is_file():
        parser.error("--mod-dir must point to VVV, with descriptor.mod directly inside it")
    try:
        install(game_dir, args.mod_dir, args.refresh)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
