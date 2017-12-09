#!/bin/bash

set -e

IMPORT="./fontimport.py --database=glyphs.sqlite"

$IMPORT fonts/OpenSans-Bold.ttf
$IMPORT fonts/OpenSans-Italic.ttf
$IMPORT fonts/OpenSans-Regular.ttf

$IMPORT fonts/noto/sans/regular/NotoSans-Regular.ttf fonts/noto/sans/regular/*
$IMPORT fonts/noto/sans/bold/NotoSans-Bold.ttf fonts/noto/sans/bold/*
$IMPORT fonts/noto/sans/italic/NotoSans-Italic.ttf fonts/noto/sans/italic/*
