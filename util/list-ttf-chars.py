import sys

from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

chars = {}
for f in sys.argv[1:]:
    for table in TTFont(f, fontNumber=0)['cmap'].tables:
        chars.update(table.cmap)

print('\n'.join(['U+%08x' % c
                 for c, desc in sorted(chars.items())]))
