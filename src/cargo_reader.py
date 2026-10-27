
import tomllib
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen

DEPENDENCY_SECTIONS = (
    "dependencies",
    "dev-dependencies",
    "build-dependencies"
)

REQUEST_TIMEOUT = 10
HTTP_NOT_FOUND = 404
MIN_REPO_PARTS = 2


def get_repo_parts(repository):
    """Получить владельца и имя GitHub-репозитория."""
    parsed = urlparse(repository)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Неверный URL репозитория")

    if parsed.netloc not in ("github.com", "www.github.com"):
        raise ValueError("Поддерживаются GitHub-репозитории")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < MIN_REPO_PARTS:
        raise ValueError("Не указан владелец или репозиторий")

    owner = parts[0]
    repo = parts[1].removesuffix(".git")

    return owner, repo


def download_manifest(repository, package_name, version):
    """Загрузить Cargo.toml нужного пакета и версии."""
    owner, repo = get_repo_parts(repository)

    tags = [version]
    if not version.startswith("v"):
        tags.append("v" + version)

    folders = [
        "",
        package_name,
        package_name.replace("-", "_")
    ]

    for tag in tags:
        for folder in folders:
            path = f"{folder}/Cargo.toml" if folder else "Cargo.toml"
            url = (
                f"https://raw.githubusercontent.com/"
                f"{owner}/{repo}/{tag}/{path}"
            )

            try:
                with urlopen(url, timeout=REQUEST_TIMEOUT) as response:
                    text = response.read().decode("utf-8")
            except HTTPError as error:
                if error.code == HTTP_NOT_FOUND:
                    continue
                raise ValueError("Ошибка загрузки Cargo.toml") from error
            except (URLError, TimeoutError) as error:
                raise ValueError("Не удалось подключиться к GitHub") from error

            try:
                manifest = tomllib.loads(text)
            except tomllib.TOMLDecodeError:
                continue

            package = manifest.get("package", {})

            if package.get("name") != package_name:
                continue

            if package.get("version") != version:
                continue

            return text

    raise ValueError(
        f"Не найдена версия {version} пакета {package_name}"
    )


def load_manifest(repository, version, test_mode, package_name=None):
    """Прочитать и проверить Cargo.toml."""
    if test_mode:
        try:
            text = Path(repository).read_text(encoding="utf-8")
        except OSError as error:
            raise ValueError(
                "Не удалось прочитать тестовый файл"
            ) from error
    else:
        if not package_name:
            raise ValueError("Не указано имя пакета")

        text = download_manifest(repository, package_name, version)

    try:
        manifest = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise ValueError("Ошибка формата Cargo.toml") from error

    package = manifest.get("package", {})

    if package.get("version") != version:
        raise ValueError("Версия пакета не совпадает с указанной")

    return manifest


def add_dependencies(result, section):
    """Добавить зависимости из одного раздела."""
    for name, details in section.items():
        if isinstance(details, dict):
            version = details.get("version", "не указана")
        else:
            version = details

        result[name] = str(version)


def get_direct_dependencies(manifest, package_name):
    """Получить прямые зависимости пакета."""
    package = manifest.get("package", {})

    if package.get("name") != package_name:
        raise ValueError("Имя пакета не совпадает с Cargo.toml")

    dependencies = {}

    for section_name in DEPENDENCY_SECTIONS:
        add_dependencies(
            dependencies,
            manifest.get(section_name, {})
        )

    for target in manifest.get("target", {}).values():
        for section_name in DEPENDENCY_SECTIONS:
            add_dependencies(
                dependencies,
                target.get(section_name, {})
            )

    return sorted(dependencies.items())