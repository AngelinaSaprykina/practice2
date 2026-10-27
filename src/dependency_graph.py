def load_test_graph(filename):
    """Прочитать тестовый граф."""
    graph = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or ":" not in line:
                    continue

                package, dependencies = line.split(":", 1)
                package = package.strip()

                if not is_valid_name(package):
                    raise ValueError("Неверное имя пакета")

                graph.setdefault(package, [])

                for dependency in dependencies.split():
                    if not is_valid_name(dependency):
                        raise ValueError("Неверное имя зависимости")

                    if dependency not in graph[package]:
                        graph[package].append(dependency)

                    graph.setdefault(dependency, [])

    except OSError as error:
        raise ValueError("Не удалось прочитать файл графа") from error

    return graph


def is_valid_name(name):
    """Проверить имя тестового пакета."""
    return name.isascii() and name.isalpha() and name.isupper()


def bfs_recursive(graph, queue, visited, parents, max_depth, filter_text):
    """Рекурсивно обойти граф в ширину."""
    if not queue:
        return visited, parents

    current, depth = queue.pop(0)

    if depth < max_depth:
        for neighbor in graph.get(current, []):
            if neighbor in visited:
                continue

            name = neighbor.split("@", 1)[0]

            if filter_text and filter_text in name:
                continue

            visited[neighbor] = depth + 1
            parents[neighbor] = current
            queue.append((neighbor, depth + 1))

    return bfs_recursive(
        graph, queue, visited, parents, max_depth, filter_text
    )


def get_reachable_packages(graph, start, max_depth, filter_text=""):
    """Получить зависимости в пределах глубины."""
    if max_depth < 0:
        raise ValueError("Глубина не может быть отрицательной")

    if start not in graph:
        raise ValueError(f"Пакет {start} не найден")

    visited = {start: 0}
    parents = {}

    return bfs_recursive(
        graph, [(start, 0)], visited, parents, max_depth, filter_text
    )


def print_branch(package, children, prefix, last):
    """Вывести ветку ASCII-дерева."""
    connector = "\\-- " if last else "|-- "
    print(prefix + connector + package)

    if last:
        prefix += "    "
    else:
        prefix += "|   "

    for index, child in enumerate(children[package]):
        is_last = index == len(children[package]) - 1
        print_branch(child, children, prefix, is_last)


def print_packages(visited, parents, start, ascii_tree):
    """Вывести найденные пакеты."""
    if not ascii_tree:
        for package, depth in visited.items():
            print(f"{package} (глубина {depth})")
        return

    children = {package: [] for package in visited}

    for package, parent in parents.items():
        children[parent].append(package)

    print(start)

    for index, child in enumerate(children[start]):
        is_last = index == len(children[start]) - 1
        print_branch(child, children, "", is_last)