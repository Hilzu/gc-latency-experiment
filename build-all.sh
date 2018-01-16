#!/usr/bin/env bash

set -euo pipefail

cd src/java/
javac -version
javac Main.java

cd ../scala
scalac -version
scalac Main.scala

cd ../node
echo -n "Node "
node --version
yarn install -s

cd ../haskell
stack ghc -- --version
stack ghc -- -O2 -optc-O3 Main.hs

cd ../swift
swiftc --version
swiftc -O -Xcc -O3 Main.swift

cd ../go
go version
go build
