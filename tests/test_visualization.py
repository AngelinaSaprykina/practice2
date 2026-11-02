import unittest

try:
    from src.visualization import build_dot_graph
except ModuleNotFoundError:
    from visualization import build_dot_graph

class TestVisualization(unittest.TestCase):
    """Проверка визуализации графа."""

    def test_build_dot_graph(self):
        """Проверить формирование связей."""
        graph = {
            "A": ["B", "C"],
            "B": ["D", "E"],
            "C": ["F"],
            "D": [],
            "E": ["F"],
            "F": []
        }

        visited = {
            "A": 0,
            "B": 1,
            "C": 1,
            "D": 2,
            "E": 2,
            "F": 2
        }

        dot_text = build_dot_graph(graph, visited)

        self.assertIn("digraph G", dot_text)
        self.assertIn('"A" -> "B";', dot_text)
        self.assertIn('"A" -> "C";', dot_text)
        self.assertIn('"B" -> "D";', dot_text)
        self.assertIn('"B" -> "E";', dot_text)
        self.assertIn('"C" -> "F";', dot_text)
        self.assertIn('"E" -> "F";', dot_text)

if __name__ == "__main__":
    unittest.main()