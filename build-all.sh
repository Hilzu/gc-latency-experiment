#!/usr/bin/env bash

set -e

cd src/java/
javac Main.java

cd ../scala
scalac Main.scala

cd ../node
npm install

cd ../haskell
stack ghc -- -O2 -optc-O3 Main.hs
