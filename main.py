#!/usr/bin/env python3
"""Sudoku CLI entry point."""

from __future__ import annotations

import argparse

from modes import daily_puzzle, random_puzzle, level_puzzle
from engine.utils import is_valid_level


def _prompt_mode() -> str:
    mode = input("Choose mode [daily/random/level]: ").strip().lower()
    return mode


def _prompt_level() -> int | None:
    raw = input("Enter level (non-negative integer): ").strip()
    if not raw:
        return None
    try:
        val = int(raw)
    except ValueError:
        print("Invalid level: must be an integer.")
        return None
    if val < 0:
        print("Invalid level: must be >= 0.")
        return None
    if not is_valid_level(val):
        print(f"Level {val} not found in available data.")
        return None
    return val


def _interactive() -> int:
    mode = _prompt_mode()
    if mode not in {"daily", "random", "level"}:
        print("Invalid mode.")
        return 2

    level = None
    if mode == "level":
        level = _prompt_level()
        if level is None:
            return 2
        return level_puzzle.run(level=level)
    else:
        maybe = _prompt_level()
        if maybe is not None:
            level = maybe
        if mode == "daily":
            return daily_puzzle.run(level=level)
        if mode == "random":
            return random_puzzle.run(level=level)
    return 2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sudoku", description="Sudoku 9x9 CLI")
    group = p.add_mutually_exclusive_group()
    group.add_argument(
        "-d", "--daily", action="store_true", help="Play the daily puzzle"
    )
    group.add_argument(
        "-r", "--random", action="store_true", help="Play a random puzzle"
    )
    p.add_argument(
        "-l",
        "--level",
        type=int,
        help=(
            "Integer level id. If used without --daily or --random, "
            "plays a random puzzle from that level."
        ),
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    no_args = not (args.daily or args.random or args.level is not None)
    if no_args:
        return _interactive()

    if args.daily:
        if args.level is not None and not is_valid_level(args.level):
            parser.error(f"Invalid level: {args.level}")
        return daily_puzzle.run(level=args.level)

    if args.random:
        if args.level is not None and not is_valid_level(args.level):
            parser.error(f"Invalid level: {args.level}")
        return random_puzzle.run(level=args.level)

    if args.level is not None:
        if not is_valid_level(args.level):
            parser.error(f"Invalid level: {args.level}")
        return level_puzzle.run(level=args.level)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
