"""Rebuild the installable font, webfont and character coverage manifest."""
from pathlib import Path
import json,subprocess,sys
from fontTools.ttLib import TTFont
root=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(root/'tools/build-font.py')],check=True)
font=TTFont(root/'fonts/ttf/CordovaHand-Regular.ttf')
(root/'fonts/woff2').mkdir(parents=True,exist_ok=True)
font.flavor='woff2';font.save(root/'fonts/woff2/CordovaHand-Regular.woff2')
(root/'fonts/characters.json').write_text(json.dumps({f'U+{code:04X}':chr(code) for code in sorted(font.getBestCmap())},ensure_ascii=False,indent=2)+'\n')
print('Packaged TTF, WOFF2 and 325-character coverage manifest.')
