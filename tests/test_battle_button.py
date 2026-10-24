import tempfile
import unittest
from pathlib import Path

from tools.install_battle_button import BUTTON, install, patch_combat_window


class BattleButtonTests(unittest.TestCase):
    def test_preserves_native_gui_and_is_idempotent(self):
        source = '\ufeffwindow = {\r\n name = "combat_window"\r\n # } comment\r\n widget = { text = "}" }\r\n buttons_window_control = { blockoverride "button_close" { onclick = "native" } }\r\n}\r\ntypes Native { type icon_a = icon { } }\r\n'
        result = patch_combat_window(source)
        self.assertEqual(result.count(BUTTON), 1)
        self.assertEqual(patch_combat_window(result), result)
        self.assertIn('widget = { text = "}" }', result)
        self.assertIn('types Native { type icon_a = icon { } }', result)
        self.assertIn('blockoverride "extra_buttons"', result)
        self.assertIn('blockoverride "button_close" { onclick = "native" }', result)

    def test_preserves_existing_extra_controls(self):
        source = 'window = { name = "combat_window" buttons_window_control = { blockoverride "extra_buttons" { native_button = {} } } }'
        result = patch_combat_window(source)
        self.assertEqual(result.count('blockoverride "extra_buttons"'), 1)
        self.assertIn('native_button = {}', result)
        self.assertEqual(result.count(BUTTON), 1)

    def test_rejects_unknown_or_broken_gui(self):
        for source in ('window = { name = "other" }', 'window = { name = "combat_window"',
                       'window = { name = "combat_window" } window = { name = "combat_window" }'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                patch_combat_window(source)

    def test_never_edits_game_or_foreign_override(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'game/gui/window_combat.gui'
            source.parent.mkdir(parents=True)
            data = b'window = { name = "combat_window" size = { 875 330 } buttons_window_control = {} }'
            source.write_bytes(data)
            destination = install(root, root / 'mod')
            self.assertEqual(source.read_bytes(), data)
            self.assertIn(BUTTON, destination.read_text(encoding='utf-8-sig'))
            self.assertEqual(install(root, root / 'mod'), destination)
            destination.write_text('window = { name = "someone_elses_window" }')
            with self.assertRaises(ValueError):
                install(root, root / 'mod', force=True)
            with self.assertRaises(ValueError):
                install(root, root / 'game')


if __name__ == '__main__':
    unittest.main()
