#!/usr/bin/env bash

set -euo pipefail

# Locate workspace root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$WS_ROOT"

echo "========================================"
echo " Formatting ROS 2 Racecar Workspace"
echo "========================================"

# ----------------------------------------
# Python: Ruff
# ----------------------------------------

echo ""
echo "[1/3] Formatting Python..."

ruff check \
    --fix \
    --config "$SCRIPT_DIR/ruff.toml" \
    src/

ruff format \
    --config "$SCRIPT_DIR/ruff.toml" \
    src/

# ----------------------------------------
# C++: clang-format
# ----------------------------------------

echo ""
echo "[2/3] Formatting C++..."

find src -type f \
    \( -name "*.cpp" -o -name "*.cc" -o -name "*.cxx" \
       -o -name "*.hpp" -o -name "*.hh" -o -name "*.h" \) \
    -print0 |
    while IFS= read -r -d '' file; do
        clang-format-18 \
            --style="file:$SCRIPT_DIR/.clang-format" \
            -i "$file"
    done

# ----------------------------------------
# YAML: Prettier
# ----------------------------------------

echo ""
echo "[3/3] Formatting YAML..."

prettier \
    --write \
    --config "$SCRIPT_DIR/.prettierrc.json" \
    --ignore-path "$SCRIPT_DIR/.prettierignore" \
    --ignore-path .gitignore \
    --ignore-path .prettierignore \
    "src/**/*.{yaml,yml}" \
    "!src/racecar_localisation/config/ekf.yaml"

echo ""
echo "========================================"
echo " Formatting Complete!"
echo "========================================"
