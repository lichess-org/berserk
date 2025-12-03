#!/usr/bin/env python3

from __future__ import annotations

import yaml
import re
import sys
import pathlib

# tablebase endpoints, defined dynamically with "/{variant}" in the code
FALSE_POSITIVES = ["/standard", "/atomic", "/antichess"]

if len(sys.argv) != 2 or not pathlib.Path(sys.argv[1]).is_file():
    path = "../api/doc/specs/lichess-api.yaml"
    if not pathlib.Path(path).is_file():
        print(
            "Usage: check-endpoints.py",
            "<path to lichess-api.yaml from lichess-org/api repo>",
        )
        exit(1)
else:
    path = sys.argv[1]


with open(path) as f:
    spec = yaml.load(f, Loader=yaml.SafeLoader)

clients_content = "\n".join(
    p.read_text() for p in pathlib.Path("berserk/clients/").glob("*.py")
)

missing_endpoints: list[str] = []

for endpoint, data in spec["paths"].items():
    # Remove leading slash
    endpoint_without_slash = endpoint[1:]

    # Replace parameter placeholders with regular expression
    # Encode/decode methods allow to treat it as raw string: https://stackoverflow.com/questions/2428117/casting-raw-strings-python/2428132#2428132
    endpoint_regex = (
        f"/{re.sub(r'{[^/]+?}', r'[^/]+?', endpoint_without_slash)}".encode(
            "unicode_escape"
        ).decode()
    )

    # Check if endpoint or a variation of it is present in file
    if not re.search(endpoint_regex, clients_content):
        if servers := data.get("servers"):
            if host := servers[0].get("url"):
                endpoint = host + endpoint
        missing_endpoints.append(endpoint)

if missing_endpoints:
    print("\nMissing endpoints:\n")
    for endp in sorted(missing_endpoints):
        if endp not in FALSE_POSITIVES:
            print(endp)
else:
    print("No missing endpoints")
