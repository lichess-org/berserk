#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
#
# coding: utf-8
# Licence: GNU AGPLv3

""""""

from __future__ import annotations

import argparse
import json
import logging
import logging.handlers
import os
import sys
import subprocess

from argparse import RawTextHelpFormatter
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional, List, Union, Tuple

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


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

RETRY_STRAT = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
ADAPTER = HTTPAdapter(max_retries=RETRY_STRAT)

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


def doc(dic: Dict[str, Callable[..., Any]]) -> str:
    """Produce documentation for every command based on doc of each function"""
    doc_string = ""
    for name_cmd, func in dic.items():
        doc_string += f"{name_cmd}: {func.__doc__}\n\n"
    return doc_string


def cleanup_containers() -> None:
    """Force remove existing Docker containers and network."""
    log.info("Cleaning up containers...")
    subprocess.run(["docker", "rm", "--force", BDIT_LILA], check=False, capture_output=True)
    subprocess.run(["docker", "rm", "--force", BDIT_APP], check=False, capture_output=True)
    subprocess.run(["docker", "network", "rm", BDIT_NETWORK], check=False, capture_output=True)
    log.info("Containers cleaned up.")


def integration_test() -> None:
    """Run the Berserk Docker Image Test (BDIT)."""
    log.info("Running integration tests")
    cleanup_containers()

    log.info(f"Creating network: {BDIT_NETWORK}")
    subprocess.run(["docker", "network", "create", BDIT_NETWORK], check=True)

    dockerfile_path = SCRIPT_DIR / "Dockerfile"
    project_root = SCRIPT_DIR.parent
    uv_cache_dir = os.path.join(os.environ.get("HOME", "/tmp"), ".cache", "uv")
    log.info(f"Building Docker image: {BDIT_APP_IMAGE} from {project_root} using {dockerfile_path}")
    subprocess.run(
        [
            "docker", "build",
            "-f", str(dockerfile_path),
            str(project_root),
            "--build-arg", f"UV_CACHE_DIR={uv_cache_dir}",
            "-t", BDIT_APP_IMAGE
        ],
        check=True
    )

    log.info(f"Starting Lila container: {BDIT_LILA} with image {BDIT_IMAGE}")
    subprocess.run(
        ["docker", "run", "--name", BDIT_LILA, "--network", BDIT_NETWORK, "-d", BDIT_IMAGE],
        check=True
    )

    log.info(f"Running app container: {BDIT_APP} with image {BDIT_APP_IMAGE}")
    subprocess.run(
        ["docker", "run", "--rm", "--name", BDIT_APP, "--network", BDIT_NETWORK, BDIT_APP_IMAGE],
        check=True
    )

    cleanup_containers()
    log.info("✅ Done")


def main() -> None:
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    commands = {
        "integration_test": integration_test,
    }
    parser.add_argument("command", choices=commands.keys(), help=doc(commands))
    args = parser.parse_args()
    commands[args.command]()


########
# Main #
########

if __name__ == "__main__":
    print("#" * 80)
    main()
