import pathlib
from typing import Annotated

import typer
from pikepdf import Pdf

app = typer.Typer()


@app.command()
def main(
    file: Annotated[pathlib.Path, typer.Argument()],
    password: Annotated[str, typer.Argument()],
):
    output = file.parent / f"{file.stem}_unlocked.pdf"
    with Pdf.open(file, password=password) as pdf:
        pdf.save(output)


if __name__ == "__main__":
    app()