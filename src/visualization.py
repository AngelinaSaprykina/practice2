import subprocess

def build_dot_graph(graph, visited):
    """Сформировать описание графа в формате Graphviz."""
    lines = []
    lines.append("digraph G {")
    lines.append("    rankdir=LR;")
    lines.append("    nodesep=0.7;")
    lines.append("    ranksep=1.0;")
    lines.append(
        "    node [shape=box, fontsize=18, width=1.0, height=0.6];"
    )
    lines.append("    edge [penwidth=1.5, arrowsize=0.8];")

    for package in visited:
        lines.append(f'    "{package}";')

    for package in visited:
        for dependency in graph.get(package, []):
            if dependency in visited:
                lines.append(f'    "{package}" -> "{dependency}";')

    lines.append("}")

    return "\n".join(lines)

def save_svg(dot_text, output_file):
    """Сохранить граф в SVG."""
    try:
        subprocess.run(
            ["dot", "-Tsvg", "-o", output_file],
            input=dot_text,
            text=True,
            check=True
        )
    except FileNotFoundError as error:
        raise ValueError("Graphviz не найден") from error
    except subprocess.CalledProcessError as error:
        raise ValueError("Ошибка создания SVG") from error
