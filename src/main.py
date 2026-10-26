import argparse
from pathlib import Path
from urllib.parse import urlparse

def create_parser():
    """Создать парсер параметров командной строки."""
    parser = argparse.ArgumentParser(
        description="Анализ зависимостей пакетов"
    )

    parser.add_argument(
        "--package",
        required=True,
        help="имя анализируемого пакета"
    )
    parser.add_argument(
        "--repository",
        required=True,
        help="URL репозитория или путь к тестовому файлу"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="работать с тестовым репозиторием"
    )
    parser.add_argument(
        "--version",
        required=True,
        help="версия пакета"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="имя файла с изображением графа"
    )
    parser.add_argument(
        "--ascii-tree",
        action="store_true",
        help="выводить зависимости как ASCII-дерево"
    )
    parser.add_argument(
        "--filter",
        default="",
        help="подстрока для фильтрации пакетов"
    )

    return parser

def is_url(value):
    """Проверить, является ли строка URL-адресом."""
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_args(args, parser):
    """Проверить параметры пользователя."""
    if not args.package.strip():
        parser.error("имя пакета не может быть пустым")

    if args.test:
        if not Path(args.repository).is_file():
            parser.error("файл тестового репозитория не найден")
    elif not is_url(args.repository):
        parser.error("неверный URL репозитория")

    if not args.version.strip():
        parser.error("версия пакета не может быть пустой")

    if not args.output.strip():
        parser.error("имя выходного файла не может быть пустым")

    if args.filter and not args.filter.strip():
        parser.error("фильтр не может состоять только из пробелов")

def print_config(args):
    """Вывести параметры в формате ключ-значение."""
    print("Параметры программы:")
    print(f"package: {args.package}")
    print(f"repository: {args.repository}")
    print(f"test_mode: {args.test}")
    print(f"version: {args.version}")
    print(f"output: {args.output}")
    print(f"ascii_tree: {args.ascii_tree}")
    print(f"filter: {args.filter}")

def main():
    """Запустить приложение."""
    parser = create_parser()
    args = parser.parse_args()

    validate_args(args, parser)
    print_config(args)

if __name__ == "__main__":
    main()