"""Entry point: `python3 -m engine` opens the window; `--check` runs the acceptance
harness headlessly; `--run-blocks <file> --cap <name>` runs a carried scenario block
file against this checkout's engine (the base/tip subprocess the scenario gate invokes)."""
import sys


def main() -> int:
    if "--check" in sys.argv:
        from . import check
        return check.run()
    if "--run-blocks" in sys.argv:
        from . import scenario
        i = sys.argv.index("--run-blocks")
        cap = sys.argv[sys.argv.index("--cap") + 1] if "--cap" in sys.argv else "carried"
        return scenario.run_blocks_file(sys.argv[i + 1], cap)
    if "--materialize" in sys.argv:
        import json
        from . import channels, tree
        print(json.dumps(channels.materialize(tree._root())))
        return 0
    if "--frame" in sys.argv:
        from . import preview
        return preview.run()
    from . import window
    window.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
