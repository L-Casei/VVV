"""Build a clean, local installation archive; never uploads anything."""
from zipfile import ZIP_DEFLATED, ZipFile

from tools.validate import ROOT, validate


def build():
    issues = validate()
    if issues:
        raise SystemExit("\n".join(issues))
    destination = ROOT / "dist" / "VVV-0.1.3.zip"
    destination.parent.mkdir(exist_ok=True)
    files = [ROOT / "descriptor.mod", ROOT / "thumbnail.png"]
    # Optional local setup helper, standard-library Python only. CK3 ignores it.
    files += [ROOT / "InstallBattleButton.cmd", ROOT / "tools/__init__.py",
              ROOT / "tools/validate.py", ROOT / "tools/install_battle_button.py"]
    for directory, extension in (("common", ".txt"), ("events", ".txt"),
                                 ("gui", ".gui"), ("gui", ".txt"),
                                 ("localization", ".yml"), ("gfx", ".dds")):
        files.extend(sorted((ROOT / directory).rglob("*" + extension)))
    with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
        for source in files:
            archive.write(source, "VVV/" + source.relative_to(ROOT).as_posix())
        archive.write(ROOT / "launcher/VVV.mod", "VVV.mod")
    print(destination)
    return destination


if __name__ == "__main__":
    build()
