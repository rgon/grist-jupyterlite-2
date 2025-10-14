#!/usr/bin/env bash


if [[ $1 == "clean" ]]; then
  echo "Cleaning previous builds..."
  rm -rf .jupyterlite.doit.db || true
  rm -rf _output || true
  rm -rf files/package.tar.gz || true
  exit 0
fi
set -eux

PACKAGE_MANAGER_PREFIX="uv run"

# echo "Cleaning previous builds..."
# eval $ jlpm run clean

# echo "Installing dependencies in extension..."
cd extension
eval $PACKAGE_MANAGER_PREFIX jlpm install
echo "Building extension..."
eval $PACKAGE_MANAGER_PREFIX jlpm build
cd ..

# echo "Developing extension..."
eval $PACKAGE_MANAGER_PREFIX jupyter labextension develop ./extension --overwrite

echo "Packaging grist python source code..."
./package.sh

eval $PACKAGE_MANAGER_PREFIX jupyter lite build

eval $PACKAGE_MANAGER_PREFIX jupyter lite serve