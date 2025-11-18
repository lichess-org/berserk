#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "requests",
#     "urllib3",
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

from subprocess import CalledProcessError
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from argparse import RawTextHelpFormatter

# from dataclasses import dataclass
# from datetime import datetime
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


def run(args: List[str]) -> str:
    """
    Executes a shell command, checks for success, and returns its stdout.

    Args:
        args: A list of strings representing the command and its arguments.

    Returns:
        The standard output of the command as a string.

    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit code.
    """
    log.debug(f"Running command: {' '.join(args)}")
    result = subprocess.run(args, check=True, text=True, capture_output=True)
    return result.stdout


def is_docker_container_running(container_name: str) -> bool:
    """Checks if a Docker container is currently running."""
    try:
        output = run(["docker", "inspect", "-f", "{{.State.Running}}", container_name]).strip()
        return output.lower() == "true"
    except CalledProcessError:
        return False


def doc(dic: Dict[str, Callable[..., Any]]) -> str:
    """Produce documentation for every command based on doc of each function"""
    doc_string = ""
    for name_cmd, func in dic.items():
        doc_string += f"{name_cmd}: {func.__doc__}\n\n"
    return doc_string


def cleanup_containers(full_cleanup: bool) -> None:
    """Remove Docker containers and network conditionally.

    :param full_cleanup: If True, remove BDIT_LILA and BDIT_NETWORK. Always attempts to remove BDIT_APP.
    """
    log.info(f"Cleaning up containers (full_cleanup={full_cleanup})...")

    try:
        run(["docker", "rm", "--force", BDIT_APP])
        log.info(f"Removed container: {BDIT_APP}")
    except CalledProcessError as e:
        if "No such container" in e.stderr:
            log.debug(f"Container {BDIT_APP} not found, skipping removal.")
        else:
            log.warning(f"Failed to remove {BDIT_APP}: {e.stderr}")

    if full_cleanup:
        try:
            run(["docker", "rm", "--force", BDIT_LILA])
            log.info(f"Removed container: {BDIT_LILA}")
        except CalledProcessError as e:
            if "No such container" in e.stderr:
                log.debug(f"Container {BDIT_LILA} not found, skipping removal.")
            else:
                log.warning(f"Failed to remove {BDIT_LILA}: {e.stderr}")

        try:
            run(["docker", "network", "rm", BDIT_NETWORK])
            log.info(f"Removed network: {BDIT_NETWORK}")
        except CalledProcessError as e:
            if "no such network" in e.stderr:
                log.debug(f"Network {BDIT_NETWORK} not found, skipping removal.")
            else:
                log.warning(f"Failed to remove {BDIT_NETWORK}: {e.stderr}")
    else:
        log.info(f"Leaving {BDIT_LILA} and {BDIT_NETWORK} intact.")
    log.info("Cleanup complete.")


class ChangeHandler(PatternMatchingEventHandler):
    def __init__(self, project_root: Path):
        super().__init__(
            patterns=["*.py"],
            ignore_patterns=[],
            ignore_directories=True,
            case_sensitive=False,
        )
        self._should_run_test = False
        self._project_root = project_root

    def on_any_event(self, event):
        # Filter for changes in berserk or integration/tests directories
        try:
            relative_path = Path(event.src_path).relative_to(self._project_root)
            if relative_path.parts[0] == "berserk" or (relative_path.parts[0] == "integration" and relative_path.parts[1] == "tests"):
                log.debug(f"Detected change in {event.src_path}: {event.event_type}")
                self.trigger_test()
        except ValueError:
            # Event outside project_root, ignore
            pass

    def trigger_test(self):
        self._should_run_test = True

    def should_run_test(self):
        return self._should_run_test

    def reset_trigger(self):
        self._should_run_test = False


def integration_test(_watch: bool) -> None:
    """Run the Berserk Docker Image Test (BDIT)."""
    log.info("Running integration tests")

    project_root = SCRIPT_DIR.parent

    # Initial cleanup: Always remove BDIT_APP. For BDIT_LILA/BDIT_NETWORK, depends on watch mode.
    cleanup_containers(full_cleanup=not _watch)

    # Ensure BDIT_NETWORK exists
    try:
        run(["docker", "network", "create", BDIT_NETWORK])
        log.info(f"Created network: {BDIT_NETWORK}")
    except CalledProcessError as e:
        if "network with name bdit_lila-network already exists" in e.stderr:
            log.debug(f"Network {BDIT_NETWORK} already exists.")
        else:
            log.error(f"Failed to create network {BDIT_NETWORK}: {e.stderr}")
            raise

    # Ensure BDIT_LILA is running.
    if not is_docker_container_running(BDIT_LILA):
        log.info(f"Starting Lila container: {BDIT_LILA} with image {BDIT_IMAGE}")
        try:
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
        except CalledProcessError as e:
            if "conflict: container name" in e.stderr:
                log.warning(
                    f"Container {BDIT_LILA} already exists but was not reported as running. Attempting to restart..."
                )
                run(["docker", "rm", "--force", BDIT_LILA])
                run(  # Retry after force removal
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
            else:
                log.error(f"Failed to start Lila container {BDIT_LILA}: {e.stderr}")
                raise

    # Build the application image (always rebuild to ensure latest changes)
    dockerfile_path = SCRIPT_DIR / "Dockerfile"
    uv_cache_dir = run(["uv", "cache", "dir"]).strip()
    log.info(
        f"Building Docker image: {BDIT_APP_IMAGE} from {project_root} using {dockerfile_path}"
    )
    run(
        [
            "docker",
            "build",
            "-f",
            str(dockerfile_path),
            str(project_root),
            "--build-arg",
            f"UV_CACHE_DIR={uv_cache_dir}",
            "-t",
            BDIT_APP_IMAGE,
        ]
    )

    def run_app_test():
        """Helper to run the BDIT_APP container."""
        log.info(f"Running app container: {BDIT_APP} with image {BDIT_APP_IMAGE}")
        try:
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
                ]
            )
            log.info("App container finished successfully.")
        except CalledProcessError as e:
            log.error(f"App container {BDIT_APP} failed with exit code {e.returncode}:")
            log.error(f"stdout: {e.stdout}")
            log.error(f"stderr: {e.stderr}")
            if _watch:
                log.info("Continuing in watch mode...")
            else:
                raise

    if _watch:
        log.info("Entering watch mode. Monitoring files in 'berserk/' and 'integration/tests/'. Press Ctrl+C to stop.")

        event_handler = ChangeHandler(project_root)
        observer = Observer()
        observer.schedule(event_handler, project_root / "berserk", recursive=True)
        observer.schedule(event_handler, project_root / "integration" / "tests", recursive=True)
        observer.start()

        try:
            # Run initial test
            run_app_test()
            while True:
                if event_handler.should_run_test():
                    event_handler.reset_trigger()
                    log.info("File change detected, rebuilding and re-running app container...")
                    # Rebuild the app image on change
                    run(
                        [
                            "docker",
                            "build",
                            "-f",
                            str(dockerfile_path),
                            str(project_root),
                            "--build-arg",
                            f"UV_CACHE_DIR={uv_cache_dir}",
                            "-t",
                            BDIT_APP_IMAGE,
                        ]
                    )
                    run_app_test()
                time.sleep(1)
        except KeyboardInterrupt:
            log.info("Watch mode stopped by user.")
        finally:
            observer.stop()
            observer.join()
            log.info(f"Watch mode exited. To clean up {BDIT_LILA} and {BDIT_NETWORK}, run without --watch.")

    else:
        # Non-watch mode: run once, then perform full cleanup
        run_app_test()
        cleanup_containers(full_cleanup=True)

    log.info("✅ Done")


def main() -> None:
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "--watch",
        "-w",
        action="store_true",
        help="Keep BDIT_LILA container around, and run BDIT_APP when files change in berserk or integration/tests",
    )
    args = parser.parse_args()
    integration_test(args.watch)


########
# Main #
########

if __name__ == "__main__":
    print("#" * 80)
    main()
