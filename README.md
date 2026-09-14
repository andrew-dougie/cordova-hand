# Cordova Hand

A chunky, uneven, capitals-only handwritten font for playful menus, game dialogue, scores, and small signs. Drawn by Andrew White for **Lil Miner’s Ruin** and inspired by the lively menu lettering of late-1990s console games.

![Cordova Hand specimen: uneven hand-drawn capitals, menu options, alphabet, numbers and accented letters](docs/specimen.svg)

## Download

- **[CordovaHand-Regular.ttf](fonts/ttf/CordovaHand-Regular.ttf)** — installable TrueType font for desktop apps, iOS, design tools, and game engines.
- **[CordovaHand-Regular.woff2](fonts/woff2/CordovaHand-Regular.woff2)** — compressed webfont for websites and browser games.
- **[Latest release](https://github.com/andrew-dougie/cordova-hand/releases/latest)** — packaged downloads with the license and examples.

On macOS, open the TTF in Font Book and select **Install**. On Windows, right-click the TTF and select **Install**. Choose **Cordova Hand** in your app’s font picker.

## The character

Cordova Hand has gently leaning strokes, irregular edges, open counters, and a little variation in each letter’s silhouette. Its 76-unit strokes give it enough weight to work with shadows and coarse pixel rendering.

It is a **capitals-only display face**: typing lowercase Latin letters displays the matching capitals, including supported accented letters. The text itself is unchanged, so names, copied text, localization strings, and screen-reader labels keep their original spelling. The sharp-s character (`ß`) displays as `SS`.

This is a real vector font. It stays clean at high resolution; pixelation, outlines, colors, lighting, and animation are presentation effects supplied by your app, rather than baked into the font.

| Detail | Included |
| --- | --- |
| Family | Cordova Hand |
| Style / PostScript name | Regular / `CordovaHand-Regular` |
| Release | 1.002 |
| Weight | 450 |
| Characters | 325 mapped code points |
| Numerals | Tabular 0–9 |
| Spacing | Proportional letters; 21 capital kerning pairs |
| Coverage | Printable ASCII, Latin-1, and selected Latin Extended-A letters |
| Formats | TTF and WOFF2 |

See the complete [character map](fonts/characters.json). This is not a full multilingual family: unsupported scripts need another font as a fallback.

## Use on the web

Copy the WOFF2 beside your stylesheet:

```css
@font-face {
  font-family: "Cordova Hand";
  src: url("CordovaHand-Regular.woff2") format("woff2");
  font-weight: 450;
  font-style: normal;
  font-display: swap;
}

.game-menu {
  font-family: "Cordova Hand", sans-serif;
  font-size: 2rem;
  line-height: 1.3;
}
```

No `text-transform` is required for the font’s supported lowercase Latin letters. Try the editable [browser specimen](examples/index.html) by opening it locally after downloading or cloning the repo. Serve the repository with `python3 -m http.server` if your browser restricts local font loading.

## Use on iOS

Add `CordovaHand-Regular.ttf` to your target’s resources and list the filename under `UIAppFonts` (Fonts provided by application) in Info.plist. Its PostScript name is:

```swift
let font = UIFont(name: "CordovaHand-Regular", size: 28)
label.font = font
label.text = "Return to main menu"
```

The visible lettering will be capitals while `label.text` retains its original value. Dynamic Type sizing and accessible labels remain the app’s responsibility.

## Build from source

The generator contains original hand-authored pen paths. It does not load, trace, extract, or depend on another game’s font or sprite sheet.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tools/package-font.py
python tools/render-specimen.py
python tools/verify-font.py
```

`tools/build-font.py` constructs the TrueType outlines, cmap, metrics, and kerning. `tools/package-font.py` also exports WOFF2 and the coverage manifest. Fixed font timestamps make builds reproducible with the pinned dependencies. The README specimen uses the shipped font’s actual outlines, so GitHub does not need to install or load a remote font.

Cordova Hand was initially developed under the working name **Shift Hand**. The public release uses `CordovaHand-Regular` throughout. It is an original typeface, not an extracted or reconstructed commercial game font.

## License

Copyright © 2026 Andrew White. Licensed under the **[SIL Open Font License 1.1](OFL.txt)**. You may use and embed it in personal or commercial projects, and redistribute or modify it under that license. No Reserved Font Names are declared.
