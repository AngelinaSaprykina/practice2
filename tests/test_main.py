import argparse
import unittest

from src.main import is_url
from src.main import validate_args


class TestConfig(unittest.TestCase):
    """Тесты параметров программы."""

    def test_correct_url(self):
        """Проверить правильный URL."""
        result = is_url("https://example.com/repository")
        self.assertTrue(result)

    def test_wrong_url(self):
        """Проверить неправильный URL."""
        result = is_url("repository")
        self.assertFalse(result)

    def test_correct_config(self):
        """Проверить правильные параметры."""
        parser = argparse.ArgumentParser()
        args = argparse.Namespace(
            package="serde",
            repository="https://example.com/repository",
            test=False,
            version="1.0",
            output="graph.svg",
            ascii_tree=False,
            filter=""
        )

        validate_args(args, parser)


if __name__ == "__main__":
    unittest.main()