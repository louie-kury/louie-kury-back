#!/bin/sh
# Project-local CLI, same output/config root even when called from a subfolder.
set -eu
project_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
cd "$project_root"
exec "$project_root/tools/ai/node_modules/.bin/playwright-cli" "$@"
