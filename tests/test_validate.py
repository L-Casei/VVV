import unittest
from tools.validate import balanced, validate


class ValidatorTests(unittest.TestCase):
    def test_brace_comments(self):
        self.assertTrue(balanced('x = { text = "}" # }\n value = 3 }'))
        self.assertFalse(balanced('x = { y = { }'))

    def test_all_project_files(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
