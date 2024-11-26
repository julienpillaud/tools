import math
import pathlib
import platform
import subprocess
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()
console = Console()

labels = [
    ("Directory: ", "magenta"),
    ("Number of files: ", "green"),
    ("Number of lines: ", "green"),
    ("Total size: ", "blue"),
]
max_label_width = max(len(label) for label, _ in labels)

exclude_patterns = {
    ".git",
    ".idea",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "__init__.py",
    "uv.lock",
}


def collect_files(
    path: pathlib.Path,
    exclude_patterns: set[str],
) -> list[pathlib.Path]:
    return [
        file
        for file in path.rglob("*")
        if file.is_file() and all(x not in file.parts for x in exclude_patterns)
    ]


def format_files(files: list[pathlib.Path]) -> str:
    return "\n".join(f"# {file}\n{file.read_text()}" for file in files)


def format_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0.00 B"

    units = ["B", "KB", "MB", "GB"]
    size = float(size_bytes)
    unit_index = min(int(math.log(size, 1024)), len(units) - 1)

    size /= 1024**unit_index
    return f"{size:.2f} {units[unit_index]}"


def copy_to_clipboard(content: str) -> None:
    if platform.system() == "Darwin":
        subprocess.run(["pbcopy"], input=content.encode(), check=True)
    elif "WSL" in platform.uname().release:
        subprocess.run(
            ["/mnt/c/Windows/System32/clip.exe"], input=content.encode(), check=True
        )


def format_text(label: str, value: str, label_style: str) -> str:
    return f"[{label_style}]{label:<{max_label_width + 5}}[/{label_style}]{value}"


def format_output(
    values: list[str],
    files: list[pathlib.Path],
    verbose: bool = False,
) -> str:
    lines = [
        format_text(label=label[0], value=value, label_style=label[1])
        for label, value in zip(labels, values)
    ]

    if verbose and files:
        lines.append("\n[yellow]Files processed:[/yellow]")
        lines.extend(f"  {file}" for file in sorted(files))

    return "\n".join(lines)


@app.command()
def main(
    path: Annotated[pathlib.Path, typer.Argument()],
    exclude: Annotated[list[str] | None, typer.Option("--exclude", "-e")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    if exclude:
        exclude_patterns.update(exclude)

    files = collect_files(path=path, exclude_patterns=exclude_patterns)

    if not files:
        console.print("[yellow]:warning: No Python files found![/yellow]")
        raise typer.Exit(1)

    content = format_files(files)
    copy_to_clipboard(content)

    total_lines = len(content.splitlines())
    total_size = len(content.encode())
    values = [
        str(path.resolve()),
        str(len(files)),
        str(total_lines),
        format_size(total_size),
    ]
    console.print(
        Panel.fit(
            format_output(values, files, verbose),
            title=":rocket: Python Files concatenated",
            border_style="blue",
        )
    )


if __name__ == "__main__":
    app()
