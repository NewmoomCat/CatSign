#!/usr/bin/env bash
#
# 简易的构建脚本
#
cd ume && pip install pipx && pipx run build
cd ..
cd jsone && pipx run build

exit