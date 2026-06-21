"""Entry point: `python3 -m hyper` opens the window; `--check` runs the
slice-1 acceptance loop headlessly."""
import sys


def main() -> int:
    if "--check" in sys.argv:
        from . import check
        return check.run()
    if "--frame" in sys.argv:
        from . import preview
        return preview.run()
    from . import window
    window.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
