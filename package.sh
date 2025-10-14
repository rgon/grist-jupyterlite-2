#!/usr/bin/env bash

clean=$1

set -eux


if [[ $clean == "clean" ]]; then
  echo "Cleaning previous builds..."
  rm -rf dist || true
  rm -rf jupyter_grist_api/grist.egg-info || true
fi
cd jupyter_grist_api

uv build
cd ..
cp dist/grist-*.whl files/grist-0.0.0-py3-none-any.whl

# cp grist/dist/grist-*.tar.gz files/package.tar.gz