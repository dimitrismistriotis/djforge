"""Demo Rich features.

Can also be used as a template for other scripts.

Run with:

```shell
poetry run python manage.py runscript rich_demo --script-args argument1 argument2
```
"""

from random import randint

from rich import inspect
from rich import print as rich_print
from rich.console import Console
from rich.highlighter import Highlighter
from rich.table import Table


class RainbowHighlighter(Highlighter):
    """Highlighter that colors every character differently."""

    def highlight(self, text):
        """Highlight text."""
        for index in range(len(text)):
            text.stylize(f"color({randint(16, 255)})", index, index + 1)


def _table_example() -> None:
    """From Language's examples."""
    table = Table(title="Star Wars Movies")

    table.add_column("Released", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right", style="green")

    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
    table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

    console = Console()
    console.print(table, justify="center")


def run(*args) -> None:
    """Show different Rich features."""
    inspect(args, methods=True)
    print()
    _table_example()
    print()
    rainbow = RainbowHighlighter()
    rich_print(rainbow("I must not fear. Fear is the mind-killer."))
