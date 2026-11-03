## practice2
Разработать инструмент визуализации графа зависимостей для менеджера пакетов

## Этап 1

На первом этапе реализовано CLI-приложение.

Программа получает параметры через командную строку:

- имя пакета;
- репозиторий;
- режим тестового репозитория;
- версию пакета;
- имя выходного файла;
- режим ASCII-дерева;
- подстроку для фильтрации.

Также реализована проверка параметров и вывод конфигурации
в формате ключ-значение.

## Запуск

run.bat

или:

python src/main.py --package A --repository tests/test_repo.txt
--test --version 1.0 --output graph.svg --ascii-tree --filter X

## Тесты

python -m unittest discover -s tests

## Этап 2. Получение зависимостей

На этом этапе добавлено получение прямых зависимостей Rust-пакета. Программа загружает файл Cargo.toml из GitHub-репозитория, проверяет имя и версию пакета и выводит список его зависимостей.

Также добавлен тестовый режим, в котором программа читает Cargo.toml из локального файла. Для работы с TOML и загрузки данных используются стандартные библиотеки Python.

Пример запуска:

python src/main.py --package A --repository tests/test_cargo.toml --test --version 1.0.0 --output graph.svg

## Тесты

В файле tests/test_main.py проверяются следующие случаи:

test_load_manifest. Проверяет чтение файла Cargo.toml.

test_direct_dependencies. Проверяет получение списка прямых зависимостей.

test_wrong_package. Проверяет обработку ошибки, если имя пакета не совпадает с указанным.

## Этап 3. Построение графа зависимостей

На этом этапе реализован обход графа зависимостей с помощью алгоритма BFS с рекурсией. Программа начинает с указанного пакета и последовательно находит связанные с ним пакеты.

Добавлены ограничение максимальной глубины обхода, фильтрация пакетов по подстроке и обработка циклических зависимостей. Для проверки используется тестовый граф из файла tests/test_repo.txt.

Также добавлен вывод найденных пакетов в виде ASCII-дерева.

## Пример запуска:

Запуск тестов

Для запуска всех автоматических тестов нужно выполнить команду из корневой папки проекта:

python -m unittest discover -s tests -v

# Запуск тестового графа

Для проверки построения графа используется команда:

python -m src.main --package A --repository tests/test_repo.txt --test --version 1.0.0 --output graph.svg --max-depth 3 --ascii-tree

Для проверки ограничения глубины можно указать --max-depth 1. Для проверки фильтрации используется параметр --filter, после которого указывается нужная подстрока.

# Этап 5. Визуализация графа зависимостей

На пятом этапе добавлена визуализация графа зависимостей с помощью Graphviz.

В файле visualization.py реализованы две функции:

build_dot_graph() формирует описание графа в формате DOT и сохраняет все связи между найденными пакетами.

save_svg() запускает Graphviz и сохраняет результат в формате SVG.

В main.py добавлен вызов визуализации и вывод DOT-описания в консоль. Также сохранён вывод зависимостей в виде ASCII-дерева.

Проверка на реальных пакетах

# Для проверки использовались три Rust-пакета.

1. ripgrep, версия 14.1.0

python -m src.main --package ripgrep --repository https://github.com/BurntSushi/ripgrep --version 14.1.0 --output ripgrep.svg --max-depth 3 --ascii-tree
start ripgrep.svg

2. bat, версия 0.24.0

python -m src.main --package bat --repository https://github.com/sharkdp/bat --version 0.24.0 --output bat.svg --max-depth 3 --ascii-tree
start bat.svg

3. fd-find, версия 10.2.0

python -m src.main --package fd-find --repository https://github.com/sharkdp/fd --version 10.2.0 --output fd.svg --max-depth 3 --ascii-tree
start fd.svg

# Тестирование

python -m src.main --package A --repository tests/test_repo.txt --test --version 1.0.0 --output graph.svg --max-depth 3 --ascii-tree

для вывода изображения: explorer.exe graph.svg

Для запуска всех тестов:

python -m unittest discover -s tests -v

Сравнение с Cargo

Для сравнения результатов используется штатная команда Cargo:

cargo tree --depth 3

Сравниваются состав зависимостей, версии пакетов и связи между ними.