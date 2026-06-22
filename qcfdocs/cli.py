"""``qcf-docs`` command-line entry point.

Subcommands:
    notebooks   Regenerate docs/*.md from the chapter .ipynb (nbconvert, as-is).
    build       Build the branded static site from docs/*.md into site/.
"""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qcf-docs", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("notebooks", help="regenerate docs/*.md from the chapter notebooks")
    sub.add_parser("build", help="build the static site into site/")

    args = parser.parse_args(argv)

    if args.command == "notebooks":
        from . import notebooks
        paths = notebooks.regenerate()
        print(f"Regenerated {len(paths)} markdown files into {notebooks.DOCS_DIR}/")
    elif args.command == "build":
        from . import build as build_mod
        paths = build_mod.build()
        print(f"Built {len(paths)} chapter pages into {build_mod.SITE_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
