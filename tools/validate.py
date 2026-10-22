"""Lightweight VVV static project validator (not CK3's parser)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def balanced(text):
    depth = 0
    quoted = False
    comment = False
    escaped = False
    for ch in text:
        if comment:
            if ch == "\n":
                comment = False
            continue
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == "#":
            comment = True
        elif ch == '"':
            quoted = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and not quoted


def validate(root=ROOT):
    problems = []
    thumbnail = root / "thumbnail.png"
    if not thumbnail.is_file():
        problems.append("missing thumbnail.png")
    else:
        data = thumbnail.read_bytes()
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            problems.append("thumbnail.png is not a PNG")
        if len(data) >= 1_000_000:
            problems.append("thumbnail.png must stay below 1 MB")
    for name in ("descriptor.mod", "launcher/VVV.mod"):
        path = root / name
        if not path.is_file():
            problems.append(f"missing {name}")
        elif not re.search(r'^picture\s*=\s*"thumbnail.png"\s*$',
                           path.read_text(encoding="utf-8-sig"), re.MULTILINE):
            problems.append(f"missing thumbnail reference in {name}")
    for name in ("descriptor.mod", "common/decisions/vvv_decisions.txt",
                 "gui/vvv_battlefield.gui", "gui/scripted_widgets/vvv_widgets.txt"):
        if not (root / name).is_file():
            problems.append(f"missing {name}")
    for base in ("common", "events", "gui"):
        for path in (root / base).rglob("*"):
            if path.is_file() and path.suffix in (".txt", ".gui"):
                if not balanced(path.read_text(encoding="utf-8")):
                    problems.append(f"unbalanced {path}")
    for path in (root / "localization").rglob("*.yml"):
        data = path.read_bytes()
        if not data.startswith(b"\xef\xbb\xbf"):
            problems.append(f"missing BOM {path}")
        keys = re.findall(r"(?m)^\s+([a-zA-Z0-9_.]+):0", data.decode("utf-8-sig"))
        if len(keys) != len(set(keys)):
            problems.append(f"duplicate localization {path}")
    return problems


if __name__ == "__main__":
    issues = validate()
    for issue in issues:
        print("ERROR:", issue)
    if issues:
        raise SystemExit(1)
    print("VVV static source checks passed; not a substitute for a CK3 game test.")
