"""Build both installable font editions, webfonts and coverage manifest."""
from pathlib import Path
import json,subprocess,sys
from fontTools.ttLib import TTFont
root=Path(__file__).resolve().parents[1]
for name,options in [('CordovaHand-Regular',[]),('CordovaHandText-Regular',['--mixed-case'])]:
 subprocess.run([sys.executable,str(root/'tools/build-font.py'),*options],check=True)
 font=TTFont(root/'fonts/ttf'/f'{name}.ttf');font.recalcTimestamp=False
 (root/'fonts/woff2').mkdir(parents=True,exist_ok=True)
 font.flavor='woff2';font.save(root/'fonts/woff2'/f'{name}.woff2')
(root/'fonts/characters.json').write_text(json.dumps({f'U+{code:04X}':chr(code) for code in sorted(font.getBestCmap())},ensure_ascii=False,indent=2)+'\n')
print('Packaged capitals and mixed-case TTF/WOFF2 editions.')
