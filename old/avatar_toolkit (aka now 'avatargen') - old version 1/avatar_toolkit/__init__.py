# __init__.py
# Entry point for the avatar toolkit package

__version__ = "1.0.0"


def get_exports():
    from .core import run_single
    from .config import DEFAULTS
    from .gui import launch_gui
    from .cli import main as cli_main
    from .batch import run_batch
    from .processing import process_image
    return {
        "run_single": run_single,
        "DEFAULTS": DEFAULTS,
        "launch_gui": launch_gui,
        "cli_main": cli_main,
        "run_batch": run_batch,
        "process_image": process_image,
    }


_exports = get_exports()

run_single = _exports["run_single"]
DEFAULTS = _exports["DEFAULTS"]
launch_gui = _exports["launch_gui"]
cli_main = _exports["cli_main"]
run_batch = _exports["run_batch"]
process_image = _exports["process_image"]

__all__ = list(_exports.keys())
