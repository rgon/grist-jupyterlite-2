#!/usr/bin/env bash

set -eux

rm .jupyterlite.doit.db || true

# echo "Cleaning previous builds..."
# eval $PACKAGE_MANAGER_PREFIX jlpm run clean

# echo "Installing dependencies in extension..."
# cd extension
# eval $PACKAGE_MANAGER_PREFIX jlpm install
# echo "Building extension..."
# eval $PACKAGE_MANAGER_PREFIX jlpm build
# cd ..

# echo "Developing extension..."
# eval $PACKAGE_MANAGER_PREFIX jupyter labextension develop ./extension --overwrite

uv run jupyter lite serve