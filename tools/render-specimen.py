"""Render the README specimen from the released font's real vector outlines."""
from pathlib import Path
import argparse
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--mixed-case',action='store_true');args=parser.parse_args()
name='CordovaHandText-Regular' if args.mixed_case else 'CordovaHand-Regular'
font=TTFont(root/'fonts/ttf'/f'{name}.ttf');cmap=font.getBestCmap();glyphs=font.getGlyphSet()
paths=['<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="780" viewBox="0 0 1280 780" role="img" aria-label="Cordova Hand font specimen"><rect width="1280" height="780" rx="20" fill="#17131e"/><path d="M64 228H1216 M64 492H1216" stroke="#67543c" stroke-width="2"/>']
def line(text,x,y,size,color):
 cursor=0;scale=size/1000
 for c in text:
  name=cmap.get(ord(c),'.notdef');pen=SVGPathPen(glyphs);glyphs[name].draw(pen)
  paths.append(f'<path fill="{color}" d="{pen.getCommands()}" transform="translate({x+cursor*scale:.3f} {y}) scale({scale} {-scale})"/>')
  cursor+=font['hmtx'][name][0]
line('Cordova Hand Text' if args.mixed_case else 'Cordova Hand',64,166,96 if args.mixed_case else 122,'#ffdd8d')
line('Play    Resume    Try again',70,305,55,'#fff1d2')
line('Return to main menu',70,383,57,'#8de2a1')
line('New high score!    12,345',70,455,49,'#89caff')
line('abcdefghijklmnopqrstuvwxyz' if args.mixed_case else 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',70,567,43,'#fff1d2')
line('0123456789   + - ! ? & @ # %',70,632,46,'#fff1d2')
line('Café • Niño • Über • Æther • Œuvre',70,693,36,'#d1bcd7')
line('325 characters • TTF + WOFF2 • OFL 1.1',70,747,25,'#ae99b4')
paths.append('</svg>');(root/'docs').mkdir(exist_ok=True);(root/'docs'/('specimen-text.svg' if args.mixed_case else 'specimen.svg')).write_text('\n'.join(paths))
print('Rendered README specimen using actual released glyphs.')
