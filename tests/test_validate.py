import unittest
from pathlib import Path
import shutil
import tempfile

from tools.validate import ROOT, balanced, validate


class ValidatorTests(unittest.TestCase):
    def test_brace_comments(self):
        self.assertTrue(balanced('x = { text = "}" # }\n value = 3 }'))
        self.assertFalse(balanced('x = { y = { }'))

    def test_all_project_files(self):
        self.assertEqual(validate(), [])

    def test_missing_unsupported_and_corrupt_custom_textures_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'mod'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(
                '.git', 'art', 'docs', 'dist', '__pycache__'))
            texture = root / 'gfx/interface/vvv/plains.dds'
            data = texture.read_bytes()
            texture.unlink()
            self.assertTrue(any('missing GUI texture' in issue for issue in validate(root)))
            texture.write_bytes(data[:128])
            self.assertTrue(any('truncated DDS pixels' in issue for issue in validate(root)))
            texture.write_bytes(data)
            wrong_size = bytearray(data)
            wrong_size[20:24] = bytes(4)
            texture.write_bytes(wrong_size)
            self.assertTrue(any('incorrect DDS linear size' in issue for issue in validate(root)))
            texture.write_bytes(data)
            gui = root / 'gui/vvv_battlefield.gui'
            gui.write_text(gui.read_text().replace('plains.dds', 'plains.png'))
            self.assertTrue(any('must be DDS' in issue for issue in validate(root)))


if __name__ == "__main__":
    unittest.main()
