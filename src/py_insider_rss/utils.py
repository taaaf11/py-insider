from __future__ import annotations

import typing

from rich.console import Console

from .parts import make_entries_table, make_info, make_summary

if typing.TYPE_CHECKING:
    from .types_ import Entry


def print_entry(entry: Entry, paging: bool, styles: bool) -> None:
    """Utility function for printing blog entry on
    screen.
    """

    info_text = make_info(entry)
    summary_md = make_summary(entry)
    elems = [info_text, summary_md]

    console = Console()

    if paging:
        with console.pager(styles=styles):
            console.print(*elems)
    else:
        console.print(*elems)


def print_entries_table(
    entries: list[Entry],
    paging: bool,
    styles: bool,
) -> None:
    """Utility function for printing a table with blog entries and
    their last updated date."""

    entries_table = make_entries_table(entries)

    console = Console()

    if paging:
        with console.pager(styles=styles):
            console.print(entries_table)
    else:
        console.print(entries_table)
