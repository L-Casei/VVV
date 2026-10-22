"""Build a clean, local installation archive; never uploads anything."""
from zipfile import ZIP_DEFLATED, ZipFile

from tools.validate import ROOT, validate


def build():
    issues = validate()
    if issues:
        raise SystemExit("\n".join(issues))
    destination = ROOT / "dist" / "VVV-0.1.0.zip"
    destination.parent.mkdir(exist_ok=True)
    files = [ROOT / "descriptor.mod", ROOT / "thumbnail.png"]
    for directory, extension in (("common", ".txt"), ("events", ".txt"),
                                 ("gui", ".gui"), ("gui", ".txt"),
                                 ("localization", ".yml")):
        files.extend(sorted((ROOT / directory).rglob("*" + extension)))
    with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
        for source in files:
            archive.write(source, "VVV/" + source.relative_to(ROOT).as_posix())
        archive.write(ROOT / "launcher/VVV.mod", "VVV.mod")
    print(destination)
    return destination


if __name__ == "__main__":
    build()
