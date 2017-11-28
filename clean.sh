#!/usr/bin/env bash

set -euo pipefail

rm -rf src/haskell/Main src/haskell/*.hi src/haskell/*.o \
  src/java/*.class \
  src/node/node_modules \
  src/python/*.pyc \
  src/scala/*.class \
  src/swift/Main
