"""Check the published binaries agree and retain their advertised font metadata."""
from pathlib import Path
from fontTools.ttLib import TTFont
root=Path(__file__).resolve().parents[1]
fonts=[TTFont(root/p) for p in ['fonts/ttf/CordovaHand-Regular.ttf','fonts/woff2/CordovaHand-Regular.woff2']]
for font in fonts:
 cmap=font.getBestCmap()
 assert len(cmap)==325
 assert font['name'].getDebugName(1)=='Cordova Hand'
 assert font['name'].getDebugName(6)=='CordovaHand-Regular'
 assert 'Open Font License' in font['name'].getDebugName(13)
 assert all(code in cmap for code in range(32,127))
 assert all(code in cmap for code in range(160,256))
 for lower in 'abcdefghijklmnopqrstuvwxyzáàâäéèêëíïóöúüñçæœøł':
  assert cmap[ord(lower)]==cmap[ord(lower.upper())],lower
 assert len({font['hmtx'][cmap[ord(n)]][0] for n in '0123456789'})==1
 assert font['hhea'].ascent==980 and font['hhea'].descent==-320
 assert font['hmtx'][cmap[ord('ß')]][0]>font['hmtx'][cmap[ord('S')]][0]
assert fonts[0].getBestCmap()==fonts[1].getBestCmap()
assert fonts[0]['hmtx'].metrics==fonts[1]['hmtx'].metrics
print('TTF and WOFF2: metadata, capitals, accents, spacing and 325-character coverage passed.')

textFonts=[TTFont(root/p) for p in ['fonts/ttf/CordovaHandText-Regular.ttf','fonts/woff2/CordovaHandText-Regular.woff2']]
for f in textFonts:
 assert f['name'].getDebugName(1)=='Cordova Hand Text'
 assert f['name'].getDebugName(6)=='CordovaHandText-Regular'
 assert len(f.getBestCmap())==325
 for lower in 'abcdefghijklmnopqrstuvwxyz':assert f.getBestCmap()[ord(lower)]!=f.getBestCmap()[ord(lower.upper())]
 assert f['OS/2'].sxHeight==470
assert textFonts[0].getBestCmap()==textFonts[1].getBestCmap()
assert textFonts[0]['hmtx'].metrics==textFonts[1]['hmtx'].metrics
print('Mixed-case TTF and WOFF2: original lowercase, metadata, metrics and coverage passed.')
