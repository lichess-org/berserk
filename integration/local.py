#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "watchdog",
# ]
# ///
#
# coding: utf-8
# Licence: GNU AGPLv3

""""""

from __future__ import annotations

import argparse
import logging
import logging.handlers
import subprocess
import sys
import time

from watchdog.events import PatternMatchingEventHandler, FileSystemEvent
from watchdog.observers import Observer

from argparse import RawTextHelpFormatter

from pathlib import Path
from typing import Any, Callable, Dict, List

#############
# Constants #
#############


SCRIPT_DIR = Path(__file__).resolve(strict=True).parent
LOG_PATH = f"{__file__}.log"

BDIT_IMAGE = "ghcr.io/lichess-org/lila-docker:main"
BDIT_LILA = "bdit_lila"
BDIT_NETWORK = "bdit_lila-network"
BDIT_APP_IMAGE = "bzrk"
BDIT_APP = "bdit_app"

########
# Logs #
########

log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)
format_string = "%(asctime)s | %(levelname)-8s | %(message)s"

# 125000000 bytes = 12.5Mb
handler = logging.handlers.RotatingFileHandler(
    LOG_PATH, maxBytes=12500000, backupCount=3, encoding="utf8"
)
handler.setFormatter(logging.Formatter(format_string))
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

handler_2 = logging.StreamHandler(sys.stdout)
handler_2.setFormatter(logging.Formatter(format_string))
handler_2.setLevel(logging.INFO)
if __debug__:
    handler_2.setLevel(logging.DEBUG)
log.addHandler(handler_2)

###########
# Classes #
###########


def run(
    cmd: List[str], check: bool = True, *args: Any, **kwargs: Any
) -> subprocess.CompletedProcess[Any]:
    """
    Executes a shell command, checks for success, and returns its stdout.

    Args:
        args: A list of strings representing the command and its arguments.

    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit code.
    """
    log.debug(f"Running command: {' '.join(cmd)}")
    res = subprocess.run(cmd, *args, check=check, text=True, **kwargs)
    return res


def doc(dic: Dict[str, Callable[..., Any]]) -> str:
    """Produce documentation for every command based on doc of each function"""
    doc_string = ""
    for name_cmd, func in dic.items():
        doc_string += f"{name_cmd}: {func.__doc__}\n\n"
    return doc_string


def cleanup_lila() -> None:
    """Remove Lila Docker container and network unconditionally."""
    log.info(f"Cleaning up Lila container...")
    run(["docker", "rm", "--force", BDIT_LILA])


def cleanup_containers() -> None:
    """Remove Docker containers and network unconditionally."""
    log.info(f"Cleaning up containers...")
    run(["docker", "rm", "--force", BDIT_APP])
    cleanup_lila()
    run(["docker", "network", "rm", "--force", BDIT_NETWORK])
    log.info("Cleanup complete.")


def run_lila():
    run(
        [
            "docker",
            "run",
            "--name",
            BDIT_LILA,
            "--network",
            BDIT_NETWORK,
            "-d",
            BDIT_IMAGE,
        ]
    )


def get_project_python_version() -> str | None:
    try:
        with open(SCRIPT_DIR.parent / ".python-version", "r") as f:
            return f.read().strip()
    except:
        return None


class ChangeHandler(PatternMatchingEventHandler):
    def __init__(self, on_change_callback: Callable[[], None]) -> None:
        super().__init__(
            patterns=["*.py"],
            ignore_patterns=[],
            ignore_directories=True,
            case_sensitive=False,
        )
        self._already_running = False
        self._on_change_callback = on_change_callback

    def on_any_event(self, event: FileSystemEvent):
        # feels like race-conditions are waiting to happen here...
        if not self._already_running:
            self._already_running = True
            self._on_change_callback()
            self._already_running = False


def integration_test(python_version: str, watch: bool) -> None:
    """Run the Berserk Docker Image Test (BDIT)."""
    log.info("Running integration tests")

    project_root = SCRIPT_DIR.parent

    cleanup_containers()

    run(["docker", "network", "create", BDIT_NETWORK])
    log.info(f"Created network: {BDIT_NETWORK}")
    run_lila()
    log.info(f"Started Lila container: {BDIT_LILA}")

    # Build the application image (always rebuild to ensure latest changes)
    dockerfile_path = SCRIPT_DIR / "Dockerfile"
    log.info(
        f"Building Docker image: {BDIT_APP_IMAGE} from {project_root} using {dockerfile_path}"
    )

    def build_and_run_test_image():
        run(
            [
                "docker",
                "build",
                "-f",
                str(dockerfile_path),
                str(project_root),
                "--build-arg",
                f"MY_UV_PYTHON_VERSION={python_version}",
                "-t",
                BDIT_APP_IMAGE,
            ]
        )
        log.info(f"Running app container: {BDIT_APP} with image {BDIT_APP_IMAGE}")
        run(
            [
                "docker",
                "run",
                "--rm",  # Always remove after execution
                "--name",
                BDIT_APP,
                "--network",
                BDIT_NETWORK,
                BDIT_APP_IMAGE,
            ],
        )
        log.info("App container finished successfully.")

    # Initial test
    build_and_run_test_image()

    if watch:
        # the tests need a fresh lila everytime, due to some actions not being idempotent
        # like kid mode or bot upgrade
        cleanup_lila()
        run_lila()
        log.info(
            "Entering watch mode. Monitoring files in 'berserk/' and 'integration/tests/'. Press Ctrl+C to stop."
        )

        def safe_build_and_run_test_image():
            try:
                build_and_run_test_image()
            except subprocess.CalledProcessError as e:
                log.error(f"Error during build or test run: {e}")
            cleanup_lila()
            run_lila()

        event_handler = ChangeHandler(safe_build_and_run_test_image)
        observer = Observer()
        observer.schedule(event_handler, str(project_root / "berserk"), recursive=True)
        observer.schedule(
            event_handler, str(project_root / "integration" / "tests"), recursive=True
        )
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            log.info("Watch mode stopped by user.")
        finally:
            observer.stop()
            observer.join()
    cleanup_containers()


def main() -> None:
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "--watch",
        "-w",
        action="store_true",
        help="Keep BDIT_LILA container around, and run BDIT_APP when files change in berserk or integration/tests",
    )
    parser.add_argument(
        "--python",
        "-py",
        type=str,
        default=get_project_python_version(),
        help="Python version to use in the Docker image",
    )
    args = parser.parse_args()
    integration_test(args.python, args.watch)


########
# Main #
########

if __name__ == "__main__":
    print("#" * 80)
    main()
