# Scripts for importing fonts into SQLite database with Mapbox GL-supported glyphs

In this project, the scripts are developed for importing fonts (TTF and OTF) into SQLite database in Mapbox GL-supported format.
The scripts are developed targeting support for [OSM Scout Server](https://github.com/rinigus/osmscout-server). The fonts are imported
as a group of fonts that is merged into a single font stack. The resulting merged font stack gets the glyphs from the provided list
of fonts by picking the glyph from the first font that has it. As a result, the fonts that are distributed as a set of fonts can be merged
and easily used in Mapbox GL styles.


## Requirements

As a requirement, font import requires
[build_pbf_glyphs](https://github.com/stadiamaps/build_pbf_glyphs). Install it
with

```
cargo install build_pbf_glyphs
```


## Prepare PBF reader

The fonts are imported using `fontimport.py` script. The script requires Protocol Buffers Python representation of the PBFs used by Mapbox GL to
define the font stacks. To generate Python code, run

```
(cd proto && protoc --python_out=. glyphs.proto)
```

## Getting fonts and import

At present, scripts are written for fetching Open Sans and Noto fonts. To fetch and unpack fonts, run `getfonts.sh`.
To import these fonts into SQLite, run `import.sh`.
