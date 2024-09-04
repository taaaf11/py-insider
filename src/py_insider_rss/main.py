from __future__ import annotations

import sys
import typing
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

import feedparser

from .utils import print_entries_table, print_entry

if typing.TYPE_CHECKING:
    from argparse import Namespace

    from .types_ import Entry

URL = "https://blog.python.org/feeds/posts/default?alt=rss"


def load_entries() -> list[Entry]:
    """Get entries from blog."""

    feed = feedparser.parse(URL)
    entries = feed["entries"]
    entries = list(reversed(entries))
    return entries


def parse_opts() -> Namespace:
    """Parse command line options and return Namespace object."""

    o_parser = ArgumentParser(
        prog="pyinsider-rss",
        description="Read python insider blog inside your terminal.",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    add_opt = o_parser.add_argument
    ln_group = o_parser.add_mutually_exclusive_group()

    ln_group.add_argument(
        "-n",
        dest="number",
        metavar="NUMBER",
        default=0,
        type=int,
        help="Show an rss feed with number NUMBER. To see all numbers,"
        " run program without arguments.",
    )
    ln_group.add_argument(
        "-l",
        dest="latest",
        action="store_true",
        default=False,
        help='Show the latest rss feed.',
    )
    add_opt(
        "-p",
        dest="paginate",
        action="store_true",
        default=False,
        help="Paginate the output.",
    )
    add_opt(
        "-s",
        dest="styles",
        action="store_true",
        default=False,
        help="Enable styles with paginator.",
    )

    options = o_parser.parse_args()
    return options


def main() -> None:
    options = parse_opts()
    entries = load_entries()

    if len(sys.argv) == 1:
        print_entries_table(entries, options.paginate, options.styles)
        sys.exit(0)

    if options.number ^ options.latest:
        c_entry_map = dict(enumerate(entries, start=1))

        if options.latest:
            latest_entry_n = sorted(c_entry_map)[-1]
            options.number = latest_entry_n

        entry = c_entry_map.get(options.number)
        print_entry(entry, options.paginate, options.styles)


if __name__ == "__main__":
    main()
