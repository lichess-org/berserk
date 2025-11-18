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

from argparse import RawTextHelpFormatter
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional, List, Union, Tuple


#############
# Constants #
#############


SCRIPT_DIR = Path(__file__).resolve(strict=True).parent
LOG_PATH = f"{__file__}.log"
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


def main() -> None:
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    # commands = {
    # "cmd": cmd_function,
    # }
    # parser.add_argument("command", choices=commands.keys(), help=doc(commands))
    # args = parser.parse_args()
    # commands[args.command]()


########
# Main #
########

if __name__ == "__main__":
    print("#" * 80)
    main()
