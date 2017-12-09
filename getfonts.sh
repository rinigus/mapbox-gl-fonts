#!/bin/bash

set -e

mkdir -p fonts
cd fonts

WGET="wget -nc "

$WGET https://github.com/google/fonts/raw/master/apache/opensans/OpenSans-Bold.ttf
$WGET https://github.com/google/fonts/raw/master/apache/opensans/OpenSans-Italic.ttf
$WGET https://github.com/google/fonts/raw/master/apache/opensans/OpenSans-Regular.ttf

mkdir -p noto
cd noto
$WGET https://noto-website-2.storage.googleapis.com/pkgs/Noto-hinted.zip
unzip Noto-hinted.zip

mkdir -p sans/regular
mkdir -p sans/bold
mkdir -p sans/italic

rm *Serif*
rm *UI-*
rm *Display-*
rm *Mono-*
rm *SansMono* *SansSymbols*

mv *Sans*-Regular.* sans/regular
mv *Sans*-Bold.* sans/bold
mv *Sans*-Italic.* sans/italic
