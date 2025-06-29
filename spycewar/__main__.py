"""Module that contains the main entry point for the application."""

import sys

from spycewar.app import App


def main(args: list[str] | None = None) -> int:
    """Run the main entry point for the application.

    Args:
        args: Arguments from the CLI. Defaults to None.
    """
    if args is None:
        args = sys.argv[1:]
    app = App()
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
