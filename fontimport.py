#!/usr/bin/env python2.7

import re, argparse, os, glob, sqlite3, tempfile, shutil, collections, sys
import proto.glyphs_pb2 as glyphs

parser = argparse.ArgumentParser(description='Import fonts and  merge them into one collection of PBF glyphs in SQLite database')
parser.add_argument('fonts', type=str, nargs="*",
                    help='List of fonts in the order of preference (from the first to the last)')
parser.add_argument('--database', type=str, help='SQLite database where the fonts are inserted')
parser.add_argument('--directory', type=str, help='Output directory where font is written')
parser.add_argument('--fontname', type=str, help='Font name for the merged fonts. When not specified, the name of the first font is used')

#####################################################################
## Helper functions

def font(filename):
    # from https://stackoverflow.com/a/199126
    f = os.path.basename(re.sub(r"([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))", r"\1 ", filename.replace('-','')[:-4]))
    return f

def get_glyph(glyph_id, gls):
    for s in gls.stacks:
        for g in s.glyphs:
            if g.id == glyph_id:
                return g
    return None

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

############
### main ###

args = parser.parse_args()
if len(args.fonts) < 1:
    print "No fonts specified for import"
    sys.exit(-1)

if args.database is None and args.directory is None:
    print "Please provide output directory or database"
    sys.exit(-1)
    
if args.database is not None and args.directory is not None:
    print "Please provide either output directory or database, not both"
    sys.exit(-1)
    
if args.fontname is None:
    args.fontname = font(args.fonts[0])

# check font list for doubles
flist = []
for f in args.fonts:
    if f not in flist:
        flist.append(f)
args.fonts = flist

# convert all to pbfs
fontdir = {}
ranges = set()
for f in args.fonts:
    fontname = font(f)
    print f, fontname
    d = tempfile.mkdtemp()
    os.system("build-glyphs '%s' '%s'" % (f, d))
    fontdir[f] = d
    for pbfname in glob.glob(d + "/*pbf"):
        ranges.add(os.path.basename(pbfname))

print "Fonts loaded"

# open the database
if args.database is not None:
    conn = sqlite3.connect(args.database)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS fonts(stack TEXT NOT NULL, range TEXT NOT NULL, pbf BLOB, unique(stack,range))")
    database_output = True
else:
    mkdir_p(os.path.join(args.directory, args.fontname))
    database_output = False
    

# iterate through ranges and merge fonts
ranges = list(ranges)
ranges.sort()
stats = collections.defaultdict(int)
for R in ranges:
    fonts = {}
    # load all fonts
    for f in args.fonts:
        fname = os.path.join(fontdir[f], R)
        if os.path.exists(fname):
            with open(fname, 'rb') as fin:
                g = glyphs.glyphs()
                g.ParseFromString(fin.read())
                fonts[f] = g

    # find available ids
    ids = set()
    for f in args.fonts:
        for s in fonts[f].stacks:
            for g in s.glyphs:
                ids.add(g.id)
    ids = list(ids)
    ids.sort()

    # merge fonts
    merged = glyphs.glyphs()
    stack = merged.stacks.add()
    stack.name = args.fontname
    stack.range = R[:-4]

    # write only if there is at least one glyph in the range
    if len(ids) > 0:
        for glyph_id in ids:
            g = None
            i = 0
            while g is None:
                cf = args.fonts[i]
                g = get_glyph(glyph_id, fonts[cf])
                i += 1
            ng = stack.glyphs.add()
            ng.ParseFromString(g.SerializeToString())
            stats[cf] += 1

        # write merged font to db
        if database_output:
            c.execute("INSERT OR REPLACE INTO fonts(stack,range,pbf) VALUES(?,?,?)",
                      (args.fontname, R[:-4], buffer(merged.SerializeToString())))
        else:
            fname = os.path.join(args.directory, args.fontname, R)
            with open(fname, 'wb') as f:
                f.write(buffer(merged.SerializeToString()))

    print "Range: %s ; Glyphs written: %d" % (R[:-4], len(ids))

# index database and close it
if database_output:
    c.execute("CREATE INDEX IF NOT EXISTS idx_fonts ON fonts(stack,range)")
    conn.commit()
    conn.close()

# cleanup
for f,d in fontdir.iteritems():
    shutil.rmtree(d)

# stats
print "\nUsed glyphs:"
for f in args.fonts:
    print f, '\t', stats[f]
print
