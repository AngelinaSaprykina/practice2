import unittest

from src.dependency_graph import load_test_graph
from src.dependency_graph import get_reachable_packages

class TestDependencyGraph(unittest.TestCase):
    """Проверить обход графа."""

    def test_load_graph(self):
        """Проверить чтение файла."""
        graph = load_test_graph("tests/test_repo.txt")

        self.assertEqual(graph["A"], ["B", "C"])
        self.assertEqual(graph["B"], ["D", "E"])

    def test_max_depth(self):
        """Проверить ограничение глубины."""
        graph = load_test_graph("tests/test_repo.txt")
        visited, parents = get_reachable_packages(graph, "A", 1)

        self.assertEqual(list(visited), ["A", "B", "C"])

    def test_cycle(self):
        """Проверить циклические зависимости."""
        graph = {"A": ["B"], "B": ["C"], "C": ["A"]}
        visited, parents = get_reachable_packages(graph, "A", 10)

        self.assertEqual(set(visited), {"A", "B", "C"})

    def test_filter(self):
        """Проверить фильтрацию."""
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": [],
            "D": []
        }

        visited, parents = get_reachable_packages(
            graph, "A", 3, "C"
        )

        self.assertEqual(set(visited), {"A", "B", "D"})

    def test_negative_depth(self):
        """Проверить отрицательную глубину."""
        with self.assertRaises(ValueError):
            get_reachable_packages({"A": []}, "A", -1)

    def test_missing_package(self):
        """Проверить отсутствующую вершину."""
        with self.assertRaises(ValueError):
            get_reachable_packages({"A": []}, "B", 3)


if __name__ == "__main__":
    unittest.main()
