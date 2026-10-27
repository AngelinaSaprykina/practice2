import unittest

from src.cargo_reader import load_manifest
from src.cargo_reader import get_direct_dependencies


class TestCargo(unittest.TestCase):
    """Проверить получение зависимостей."""

    def test_load_manifest(self):
        """Проверить чтение Cargo.toml."""
        manifest = load_manifest(
            "tests/test_cargo.toml",
            "1.0.0",
            True
        )

        self.assertEqual(manifest["package"]["name"], "A")

    def test_direct_dependencies(self):
        """Проверить список зависимостей."""
        manifest = load_manifest(
            "tests/test_cargo.toml",
            "1.0.0",
            True
        )

        dependencies = get_direct_dependencies(manifest, "A")

        self.assertEqual(
            dependencies,
            [
                ("pretty_assertions", "1.4"),
                ("serde", "1.0"),
                ("serde_json", "1.0")
            ]
        )

    def test_wrong_package(self):
        """Проверить ошибку при неправильном имени."""
        manifest = load_manifest(
            "tests/test_cargo.toml",
            "1.0.0",
            True
        )

        with self.assertRaises(ValueError):
            get_direct_dependencies(manifest, "B")


if __name__ == "__main__":
    unittest.main()
