import unittest

from validate_repo import validation_errors


class RepoLayout(unittest.TestCase):
    def test_repo_is_valid(self) -> None:
        self.assertEqual(validation_errors(), [])


if __name__ == "__main__":
    unittest.main()
