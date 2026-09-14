"""Cordova Hand: original stroke-drawn letters. Does not read reference glyphs/fonts."""
from pathlib import Path
import argparse,math,unicodedata,json
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.svgLib.path import parse_path
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'fonts/ttf/CordovaHand-Regular.ttf')
parser.add_argument('--mixed-case',action='store_true',help='Build Cordova Hand Text with the original lowercase forms.')
args=parser.parse_args()
if args.mixed_case and args.output.name=='CordovaHand-Regular.ttf':args.output=args.output.with_name('CordovaHandText-Regular.ttf')
family='Cordova Hand Text' if args.mixed_case else 'Cordova Hand'
font_name='CordovaHandText-Regular' if args.mixed_case else 'CordovaHand-Regular'
version='1.003' if args.mixed_case else '1.002'
# 76-unit strokes, up from 64: a small weight increase with unchanged centerlines,
# advance widths, kerning, and vertical metrics.
STROKE_RADIUS=38
# Width and pen paths in a 1000-unit em. Authored individually, including lowercase.
D={
'A':(540,'M40 15 L245 685 L502 5 M119 247 L409 278'),
'B':(520,'M64 4 L61 665 Q465 775 451 512 Q445 397 85 347 M88 347 Q541 423 468 127 Q429 -17 64 4'),
'C':(525,'M471 588 Q365 744 176 653 Q14 564 52 269 Q85 -31 453 67'),
'D':(550,'M65 6 L55 646 Q527 787 493 315 Q481 -6 65 6'),
'E':(475,'M437 650 L69 615 L63 27 L430 55 M70 333 L382 371'),
'F':(460,'M65 0 L72 639 L431 675 M70 343 L377 366'),
'G':(565,'M489 594 Q312 760 141 623 Q-6 469 72 211 Q184 -43 486 91 L502 340 L302 326'),
'H':(540,'M66 666 L67 10 M470 685 L476 12 M71 319 L471 364'),
'I':(220,'M110 655 L105 16'),
'J':(450,'M368 667 L362 164 Q349 -74 88 39 L52 140'),
'K':(525,'M73 672 L61 1 M470 662 L83 286 M231 422 L489 22'),
'L':(440,'M72 670 L63 34 L399 61'),
'M':(695,'M62 3 L82 672 L346 206 L606 682 L638 18'),
'N':(565,'M58 12 L69 671 L488 30 L491 681'),
'O':(565,'M279 675 Q50 673 57 355 Q54 25 296 30 Q532 54 511 370 Q495 694 279 675 Z'),
'P':(510,'M62 4 L72 649 Q448 758 458 528 Q474 299 70 339'),
'Q':(580,'M290 675 Q46 650 55 327 Q65 -1 302 27 Q543 53 511 375 Q492 697 290 675 Z M347 207 L555 -68'),
'R':(530,'M66 6 L67 648 Q463 753 458 511 Q453 329 76 328 M274 344 L496 8'),
'S':(490,'M434 601 Q201 771 81 569 Q-4 422 270 358 Q534 289 416 101 Q303 -42 55 68'),
'T':(535,'M37 646 L508 680 M272 659 L260 8'),
'U':(540,'M62 677 L60 188 Q65 -39 287 22 Q486 51 478 234 L471 675'),
'V':(535,'M45 672 L255 21 L494 681'),
'W':(730,'M43 668 L181 23 L374 462 L531 11 L689 682'),
'X':(520,'M53 668 L468 12 M457 679 L52 5'),
'Y':(520,'M41 674 L267 370 L486 682 M267 370 L255 5'),
'Z':(500,'M47 649 L461 674 L53 35 L460 58'),
'a':(455,'M361 423 Q132 568 62 294 Q5 45 181 27 Q368 27 365 461 L367 20'),
'b':(460,'M66 713 L55 25 M62 270 Q115 546 303 439 Q471 347 358 126 Q272 -31 55 25'),
'c':(408,'M352 403 Q188 552 74 363 Q-35 65 190 26 Q282 5 355 73'),
'd':(463,'M383 715 L366 18 M365 423 Q161 558 66 342 Q-14 130 119 37 Q284 -23 366 219'),
'e':(438,'M69 244 L380 277 Q379 514 179 462 Q-17 413 68 131 Q141 -20 367 77'),
'f':(332,'M108 -1 L126 529 Q120 772 314 678 M40 439 L280 464'),
'g':(461,'M365 407 Q172 555 72 354 Q-1 138 143 52 Q291 -14 370 230 M380 465 L361 -82 Q352 -316 100 -199'),
'h':(469,'M68 722 L59 10 M67 270 Q155 515 311 442 Q415 405 391 13'),
'i':(202,'M98 440 L91 9 M102 666 L104 657'),
'j':(258,'M178 447 L164 -118 Q149 -299 18 -209 M179 663 L178 654'),
'k':(434,'M66 708 L57 5 M377 451 L72 180 M208 305 L403 21'),
'l':(214,'M112 714 L91 63 Q89 12 148 25'),
'm':(684,'M55 449 L52 5 M54 278 Q131 512 263 430 Q311 385 311 17 M309 277 Q395 511 531 431 Q615 388 607 10'),
'n':(467,'M62 452 L57 8 M59 279 Q168 526 324 423 Q395 372 388 10'),
'o':(459,'M218 472 Q45 454 50 233 Q57 8 240 22 Q423 31 401 266 Q386 480 218 472 Z'),
'p':(458,'M64 452 L49 -232 M62 384 Q254 558 377 362 Q474 146 298 51 Q183 3 58 109'),
'q':(458,'M372 433 L361 -237 M373 420 Q171 545 62 351 Q-17 131 118 49 Q292 -27 369 227'),
'r':(362,'M67 450 L62 6 M65 273 Q151 543 321 426'),
's':(399,'M340 412 Q124 538 68 365 Q36 271 206 226 Q399 178 309 69 Q204 -32 48 51'),
't':(326,'M131 646 L116 136 Q106 -13 274 44 M37 437 L282 462'),
'u':(464,'M61 455 L56 159 Q58 -49 240 42 Q352 98 374 258 M384 468 L377 21'),
'v':(427,'M44 450 L196 18 L387 468'),
'w':(603,'M42 449 L140 18 L312 335 L439 14 L565 472'),
'x':(412,'M52 452 L367 20 M355 469 L48 12'),
'y':(438,'M46 455 L221 58 M389 470 L168 -84 Q107 -247 37 -217'),
'z':(414,'M49 429 L370 460 L49 23 L370 44'),
'0':(480,'M240 676 Q64 671 60 341 Q48 20 238 17 Q429 20 420 351 Q420 691 240 676 Z'),
'1':(480,'M122 520 L254 679 L241 30 M116 24 L372 37'),
'2':(480,'M67 514 Q141 763 348 640 Q521 500 227 247 L63 44 L423 48'),
'3':(480,'M72 614 Q354 779 390 554 Q413 380 205 353 M205 353 Q466 403 397 156 Q328 -31 54 72'),
'4':(480,'M344 685 L68 250 L426 259 M345 685 L328 8'),
'5':(480,'M416 671 L109 639 L92 373 Q431 494 411 212 Q386 -33 60 63'),
'6':(480,'M371 674 Q89 560 65 258 Q44 -2 253 20 Q443 47 408 236 Q365 424 83 286'),
'7':(480,'M52 646 L427 670 Q280 415 220 4'),
'8':(480,'M238 360 Q27 424 100 593 Q175 729 332 637 Q484 487 238 360 Q-24 235 104 79 Q253 -44 392 116 Q467 286 238 360 Z'),
'9':(480,'M397 365 Q132 259 80 461 Q45 662 230 682 Q426 706 409 439 Q401 133 144 9'),
'.':(180,'M88 30 L89 24'), ',':(190,'M112 51 Q120 -23 60 -81'), ':':(190,'M94 377 L95 369 M88 33 L89 25'),
';':(200,'M98 377 L99 369 M123 53 Q118 -28 61 -82'), '!':(218,'M106 667 L98 206 M97 31 L98 24'),
'?':(433,'M54 526 Q132 736 317 640 Q485 506 287 373 Q207 319 205 204 M204 30 L205 24'),
"'":(165,'M92 689 L75 526'), '"':(277,'M90 689 L72 528 M210 689 L193 526'),
'-':(364,'M59 305 L303 318'), '_':(480,'M39 -126 L442 -116'), '+':(470,'M50 303 L425 319 M240 503 L230 117'),
'=':(470,'M50 404 L423 418 M49 224 L425 237'), '/':(421,'M370 704 L47 -73'), '\\':(421,'M50 704 L368 -72'),
'(':(286,'M233 749 Q-44 314 222 -146'), ')':(286,'M58 749 Q327 314 67 -146'),
'[':(291,'M240 749 L82 730 L68 -133 L226 -125'), ']':(291,'M54 740 L211 747 L202 -127 L45 -137'),
'{':(320,'M263 750 Q103 788 149 518 Q172 338 48 311 Q179 278 133 91 Q85 -156 250 -135'),
'}':(320,'M57 750 Q217 788 171 518 Q148 338 272 311 Q141 278 187 91 Q235 -156 70 -135'),
'<':(470,'M397 559 L72 302 L395 54'), '>':(470,'M73 559 L398 302 L75 54'),
'*':(383,'M80 562 L306 334 M309 563 L76 339 M194 608 L189 281'),
'#':(535,'M194 698 L118 0 M419 703 L342 9 M63 444 L484 462 M43 226 L465 247'),
'%':(591,'M503 701 L92 -3 M141 659 Q40 658 57 548 Q80 448 180 486 Q266 531 223 623 Q195 673 141 659 Z M437 202 Q336 199 351 91 Q373 -9 474 25 Q564 80 516 166 Q484 218 437 202 Z'),
'&':(560,'M472 45 L147 455 Q-9 680 217 696 Q423 681 254 492 L106 345 Q-71 155 139 31 Q347 -58 490 325'),
'@':(721,'M469 414 Q278 532 224 326 Q171 129 300 152 Q420 160 455 392 L448 169 Q629 59 653 365 Q660 715 332 683 Q18 648 61 233 Q113 -44 538 15'),
'$':(493,'M435 592 Q193 763 84 565 Q2 419 275 356 Q527 290 412 103 Q304 -40 56 68 M284 787 L222 -112'),
'^':(423,'M62 467 L213 669 L368 476'), '`':(244,'M70 707 L169 581'), '~':(480,'M58 304 Q136 427 250 327 Q347 240 421 355'),
'|':(180,'M90 749 L88 -146'),
}
# Extra independent forms and common typography.
D.update({'ß':(480,'M74 -15 L70 529 Q64 738 265 689 Q457 633 280 410 Q482 348 408 144 Q349 22 207 89'),
'Æ':(745,'M27 5 L301 667 L349 23 M139 270 L348 294 M702 678 L352 652 L349 23 L704 47 M353 337 L638 372'),
'æ':(707,'M67 388 Q248 587 300 335 L287 19 M298 271 Q48 357 51 134 Q54 -57 290 76 M320 241 L640 272 Q635 512 432 454 Q273 415 337 132 Q410 -22 634 67'),
'Œ':(774,'M290 675 Q48 672 62 328 Q66 8 286 29 L372 55 L382 657 L290 675 Z M726 680 L382 657 L372 55 L735 75 M379 343 L684 369'),
'œ':(704,'M205 468 Q40 454 54 218 Q65 0 235 28 Q405 68 368 296 Q340 476 205 468 Z M367 249 L640 277 Q637 513 447 453 Q312 387 369 142 Q431 -18 639 62'),
'¡':(218,'M98 448 L99 441 M98 264 L108 -195'),
'¿':(433,'M214 448 L215 441 M213 257 Q215 126 130 84 Q-63 -59 113 -184 Q306 -293 379 -61'),
'£':(500,'M452 61 L62 33 M146 37 Q237 155 170 334 Q29 735 395 657 M57 296 L348 317'),
'€':(535,'M479 591 Q290 768 137 572 Q2 374 135 133 Q273 -54 475 83 M47 423 L371 441 M38 277 L365 292'),
'¢':(430,'M359 412 Q187 544 74 351 Q-15 104 183 43 Q294 13 363 81 M251 630 L191 -119'),
'¥':(530,'M44 678 L265 365 L487 687 M265 365 L258 3 M100 292 L430 309 M98 159 L426 174'),
'×':(470,'M72 492 L405 91 M397 496 L74 88'), '÷':(470,'M57 302 L415 318 M238 505 L239 498 M227 105 L228 98'),
'°':(288,'M140 694 Q36 681 49 587 Q65 492 161 510 Q265 537 237 628 Q219 709 140 694 Z'),
'•':(210,'M103 316 L105 310'), '·':(180,'M88 305 L89 299'),
'…':(565,'M87 30 L88 24 M275 30 L276 24 M463 30 L464 24'),
'–':(580,'M58 305 L524 322'), '—':(860,'M57 305 L807 324'),
'©':(716,'M361 682 Q47 677 54 335 Q55 0 368 19 Q676 42 655 371 Q637 699 361 682 Z M472 496 Q259 621 218 354 Q190 94 485 223'),
'®':(716,'M361 682 Q47 677 54 335 Q55 0 368 19 Q676 42 655 371 Q637 699 361 682 Z M243 195 L246 524 Q475 580 475 433 Q474 322 245 337 M369 344 L503 192'),
'™':(788,'M31 671 L324 684 M181 680 L173 384 M394 386 L411 685 L563 446 L711 687 L737 393'),
'←':(610,'M96 307 L551 327 M280 502 L88 306 L279 108'),
'→':(610,'M63 307 L517 327 M337 515 L529 327 L338 115'),
'↑':(530,'M261 62 L268 617 M61 406 L268 631 L477 414'),
'↓':(530,'M261 646 L268 91 M61 302 L268 76 L477 294')})
for char,base in {'‘':"'",'’':"'",'‚':',','“':'"','”':'"','„':'"','−':'-'}.items():D[char]=D[base]

D.update({
'«':(550,'M273 451 L74 278 L268 110 M483 459 L284 287 L478 119'),
'»':(550,'M72 451 L271 278 L77 110 M282 459 L481 287 L287 119'),
'¯':(480,'M67 748 L418 760'),
'±':(480,'M57 376 L425 393 M239 590 L231 191 M57 45 L425 58'),
'µ':(472,'M62 451 L53 -222 M65 260 Q55 -20 239 42 Q354 93 378 271 M390 467 L382 30 L438 22')})
# Sample each hand-drawn centerline, expand it into a smooth, slightly irregular
# pen ribbon. Positive contours overlap harmlessly; counters are true holes.
def centerlines(svg):
 rec=RecordingPen();parse_path(svg,rec);parts=[];points=[];at=(0,0)
 for op,args in rec.value:
  if op=='moveTo':
   if points:parts.append((points,False))
   at=args[0];points=[at]
  elif op=='lineTo':
   end=args[0];n=max(2,math.ceil(math.dist(at,end)/24));start=at
   points.extend(tuple(start[j]+(end[j]-start[j])*i/n for j in (0,1)) for i in range(1,n+1));at=end
  elif op=='qCurveTo':
   control,end=args;start=at;n=max(8,math.ceil((math.dist(start,control)+math.dist(control,end))/20))
   points.extend(tuple((1-i/n)**2*start[j]+2*(1-i/n)*(i/n)*control[j]+(i/n)**2*end[j] for j in (0,1)) for i in range(1,n+1));at=end
  elif op=='closePath':
   if math.dist(points[0],points[-1])>1:points.append(points[0])
   parts.append((points,True));points=[]
  elif op=='endPath':
   if points:parts.append((points,False));points=[]
 if points:parts.append((points,False))
 return parts

def contour(pen,pts):
 pen.moveTo(tuple(round(x) for x in pts[0]));
 for p in pts[1:]:pen.lineTo(tuple(round(x) for x in p))
 pen.closePath()

def outlines(svg,seed=0,scale=1,dx=0,dy=0):
 result=[]
 for path,closed in centerlines(svg):
  if closed:path=path[:-1]
  left=[];right=[]
  for i,(x,y) in enumerate(path):
   a=path[(i-1)%len(path)] if closed or i else path[0]
   b=path[(i+1)%len(path)] if closed or i+1<len(path) else path[-1]
   vx,vy=b[0]-a[0],b[1]-a[1];d=max(.001,math.hypot(vx,vy));nx,ny=-vy/d,vx/d
   r=STROKE_RADIUS*(1+.085*math.sin(x*.017+y*.011+seed)+.035*math.cos(y*.029-seed))
   left.append((x+nx*r,y+ny*r));right.append((x-nx*r,y-ny*r))
  if closed:paths=[left,list(reversed(right))]
  else:
   def cap(center,start,end):
    a=math.atan2(start[1]-center[1],start[0]-center[0]);r=math.dist(center,start)
    return [(center[0]+r*math.cos(a-math.pi*i/8),center[1]+r*math.sin(a-math.pi*i/8)) for i in range(1,8)]
   paths=[left+cap(path[-1],left[-1],right[-1])+list(reversed(right))+cap(path[0],right[0],left[0])]
  # A mild forward lean and optical overshoot are baked into vectors, not CSS.
  for pts in paths:result.append([((x+y*.045)*scale+dx,y*scale+dy) for x,y in pts])
 return result

ACC={
'\u0300':'M170 820 L287 730','\u0301':'M227 735 L345 839',
'\u0302':'M130 742 L249 830 L366 739','\u0303':'M106 757 Q165 842 248 772 Q314 713 384 806',
'\u0308':'M163 787 L164 784 M328 787 L329 784',
'\u030A':'M244 894 Q151 874 182 785 Q211 724 282 763 Q353 823 291 876 Q266 896 244 894 Z',
'\u0304':'M121 782 L377 790','\u0306':'M118 815 Q239 668 376 813',
'\u0307':'M249 790 L250 785','\u030B':'M164 735 L244 838 M290 735 L370 838',
'\u030C':'M133 823 L250 732 L370 827',
'\u0327':'M255 -18 L216 -96 Q363 -100 253 -213 L170 -213',
'\u0328':'M352 12 Q159 -173 324 -174 L364 -147',
}
glyphs={};metrics={};cmap={};geometry={}
def make(char,paths,width):
 name='.notdef' if char is None else f'uni{ord(char):04X}';pen=TTGlyphPen(None)
 for pts in paths:contour(pen,pts)
 g=pen.glyph()
 # Overlap flag makes intersection intent explicit to native and browser rasterizers.
 if hasattr(g,'flags') and len(g.flags):g.flags[0]|=0x40
 glyphs[name]=g
 minx=min((x for pts in paths for x,y in pts),default=0)
 metrics[name]=(int(width+75),round(minx));geometry[char]=(paths,width)
 if char is not None:cmap[ord(char)]=name
make(None,outlines('M70 0 L70 680 L440 680 L440 0 Z M135 125 L369 556 M143 562 L373 120'),510)
for c,(w,svg) in D.items():make(c,outlines(svg,ord(c)*.41),w)
for c in [' ','\u00A0']:make(c,[],260)
for code in range(0x00C0,0x0180):
 c=chr(code)
 if c in geometry:continue
 decomp=unicodedata.normalize('NFD',c)
 if len(decomp)==2 and decomp[0] in D and decomp[1] in ACC:
  base,mark=decomp;paths,w=geometry[base];accent=outlines(ACC[mark],code*.41,dx=(w-500)/2,dy=-205 if base.islower() and mark not in ['\u0327','\u0328'] else 0)
  if base=='i':paths=outlines('M98 440 L91 9',ord(base)*.41)
  make(c,paths+accent,w)
for c,base in [('Ø','O'),('ø','o'),('Ł','L'),('ł','l'),('Đ','D'),('đ','d'),('Ŧ','T'),('ŧ','t')]:
 paths,w=geometry[base]
 svg=('M45 -25 L'+str(w-30)+' '+('700' if base.isupper() else '490')) if c in 'Øø' else 'M30 310 L'+str(w-20)+' 402'
 make(c,paths+outlines(svg,0),w)
make('ı',outlines('M98 440 L91 9'),202)
for c,base in [('Ð','D'),('ð','d'),('Þ','P'),('þ','p')]:
 paths,w=geometry[base];make(c,paths+outlines('M22 332 L248 352'),w)
# Ellipsis/quotation/ASCII, Latin-1 and common European accents are real cmap entries.
# Supplement the remaining Latin-1 symbols without mapping unknown scripts to Latin.
for c,base in [('ª','a'),('º','o'),('²','2'),('³','3'),('¹','1')]:
 w,svg=D[base];make(c,outlines(svg,1,scale=.58,dy=390),w*.58)
for c,num,den in [('¼','1','4'),('½','1','2'),('¾','3','4')]:
 make(c,outlines(D[num][1],1,scale=.52,dy=340)+outlines('M110 -10 L570 710')+outlines(D[den][1],2,scale=.52,dx=415),720)
for c,svg in [('¬','M47 348 L391 367 L385 199'),('¦','M90 750 L87 385 M89 220 L88 -146'),('¶','M384 -125 L397 699 L238 695 Q21 697 63 452 Q95 338 258 361 M258 683 L244 -125'),('§','M369 639 Q182 771 113 618 Q82 532 259 446 Q462 342 309 192 Q214 98 94 218 Q-13 379 213 445 M94 218 Q275 139 334 35 Q344 -137 85 -38'),('¤','M136 468 Q316 566 406 379 Q496 163 270 126 Q44 145 97 349 Q105 423 136 468 Z M51 534 L135 454 M387 453 L470 538 M56 61 L140 153 M377 149 L472 54')]:make(c,outlines(svg,5),520 if c not in '¦' else 180)
make('\u00AD',[],0)
for c,svg in [('¨','M163 787 L164 784 M328 787 L329 784'),('´','M130 650 L248 754'),('¸','M155 2 L115 -78 Q272 -84 158 -192 L74 -193')]:make(c,outlines(svg),390)
# Cordova Hand is a capitals-only display face. Map lowercase code points to the
# matching authored capitals so UIKit labels, web canvases and 3D text agree while
# stored/localized/accessibility strings keep their original spelling.
capital_mappings={}
for code in ([] if args.mixed_case else list(cmap)):
 char=chr(code);upper=char.upper()
 if char==upper:continue
 if len(upper)==1 and ord(upper) in cmap:
  cmap[code]=cmap[ord(upper)];capital_mappings[char]=upper
 elif len(upper)>1 and all(letter in geometry for letter in upper):
  paths=[];cursor=0
  for letter in upper:
   shape,width=geometry[letter]
   paths.extend([[(x+cursor,y) for x,y in contour] for contour in shape]);cursor+=width+75
  make(char,paths,cursor-75);capital_mappings[char]=upper
order=list(glyphs);fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(order);fb.setupCharacterMap(cmap);fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=980,descent=-320,lineGap=0)
fb.setupNameTable({'familyName':family,'styleName':'Regular','uniqueFontIdentifier':font_name+'-'+version,'fullName':family+' Regular','psName':font_name,'version':'Version '+version,'copyright':'Copyright 2026 Andrew White. Original lettering.','description':'Handwritten UI lettering with original lowercase forms.' if args.mixed_case else 'Original handwritten game UI lettering. Medium-weight capitals-only UI edition.','licenseDescription':'This Font Software is licensed under the SIL Open Font License, Version 1.1.','licenseInfoURL':'https://openfontlicense.org/'})
fb.setupOS2(version=4,sTypoAscender=980,sTypoDescender=-320,sTypoLineGap=0,usWinAscent=980,usWinDescent=320,sxHeight=470 if args.mixed_case else 700,sCapHeight=700,usWeightClass=450,fsType=0,fsSelection=0xC0)
fb.setupPost();fb.setupMaxp();font=fb.font
pairs={'AV':-48,'AW':-40,'AY':-40,'AT':-34,'FA':-26,'LT':-38,'LV':-40,'LY':-43,'PA':-30,'TA':-35,'To':-50,'Ta':-45,'Te':-42,'Ty':-25,'VA':-45,'Vo':-28,'WA':-35,'Wo':-22,'YA':-44,'Yo':-50,'Ye':-40,'Ya':-46,'rt':-10}
# Lowercase cmap aliases must share capital kerning; prefer authored capital pairs.
capital_pairs={}
for pair,value in pairs.items():capital_pairs.setdefault(pair.upper(),value)
pairs=pairs if args.mixed_case else capital_pairs
fea='languagesystem DFLT dflt; languagesystem latn dflt; feature kern {\n'+''.join(f'pos uni{ord(a):04X} uni{ord(b):04X} {n};\n' for (a,b),n in pairs.items())+'} kern;'
addOpenTypeFeaturesFromString(font,fea)
# Fixed timestamps make repeated authoring byte-for-byte reproducible.
font['head'].created=font['head'].modified=3872102400;font.recalcTimestamp=False
args.output.parent.mkdir(parents=True,exist_ok=True)
font.save(args.output)
report={'family':family,'glyphs':len(glyphs),'characters':len(cmap),'kerningPairs':len(pairs),'missingASCII':[chr(i) for i in range(32,127) if i not in cmap],'missingLatin1':[chr(i) for i in range(160,256) if i not in cmap],'scripts':'Latin; system fallback for other scripts','strokeWidth':STROKE_RADIUS*2, 'version':version, 'capitalMappings':len(capital_mappings)}
print(json.dumps(report))
