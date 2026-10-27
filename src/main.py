import argparse

try:
    from src.dependency_graph import load_test_graph
    from src.dependency_graph import get_reachable_packages
    from src.dependency_graph import print_packages
except ModuleNotFoundError:
    from dependency_graph import load_test_graph
    from dependency_graph import get_reachable_packages
    from dependency_graph import print_packages

DEFAULT_MAX_DEPTH = 3


def create_parser():
    """Создать парсер параметров."""
    parser = argparse.ArgumentParser(
        description="Анализ зависимостей пакетов"
    )

    parser.add_argument("--package", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--ascii-tree", action="store_true")
    parser.add_argument(
        "--max-depth",
        type=int,
        default=DEFAULT_MAX_DEPTH
    )
    parser.add_argument("--filter", default="")

    return parser


def main():
    """Запустить программу."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.package.strip():
        parser.error("Не указано имя пакета")

    if not args.version.strip():
        parser.error("Не указана версия пакета")

    if args.max_depth < 0:
        parser.error("Глубина не может быть отрицательной")

    try:
        if args.test:
            graph = load_test_graph(args.repository)
            start = args.package
        else:
            try:
                from src.cargo_reader import load_lock_graph
            except ImportError:
                from cargo_reader import load_lock_graph

            graph, start = load_lock_graph(
                args.repository,
                args.version,
                args.package
            )

        visited, parents = get_reachable_packages(
            graph,
            start,
            args.max_depth,
            args.filter
        )

    except (ValueError, ImportError) as error:
        parser.error(str(error))

    print_packages(
        visited,
        parents,
        start,
        args.ascii_tree
    )


if __name__ == "__main__":
    main()