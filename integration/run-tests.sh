#!/bin/bash -e

python3 -m pip install -e . --no-cache-dir

attempts=0
while [ $attempts -lt 30 ]; do
    if curl -s http://bdit_lila:9663 >/dev/null; then
        break
    fi
    echo "⌛ Waiting for lila to start..."
    sleep 1
    attempts=$((attempts + 1))
done

pytest integration
