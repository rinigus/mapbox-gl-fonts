# Conversion scripts for fonts into Mapbox GL-supported glyphs

The fonts are imported into SQLite database and are developed targeting support for
[OSM Scout Server](https://github.com/rinigus/osmscout-server). The fonts are imported as a group of fonts that is merged
into a single font. The resulting merged font gets the glyphs from the provided list of fonts by picking the glyph from the first font that
has it.  


## Requirements

As a requirement, font import requires
[node-fontnik](https://github.com/mapbox/node-fontnik/). Install it
with

```
npm install -g fontnik
```


## Prepare PBF reader

The fonts are imported using `fontimport.py` script. The script requires Protocol Buffers Python representation of the PBFs used by Mapbox GL to
define font stacks. To generate Python code, run

```
(cd proto && protoc --python_out=. glyphs.proto)
```

## Getting fonts and import

At present, scripts are written for fetching Open Sans and Noto fonts. To fetch and unpack fonts, run `getfonts.sh`.
To import these fonts into SQLite, run `import.sh`.
