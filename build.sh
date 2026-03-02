#!/usr/bin/env bash

python -m pip install pipx
cd catsign_um
pipx run build
cd ..
cd catsign_json
pipx run build