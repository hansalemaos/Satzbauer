import re
import menu3
from farbprinter.farbprinter import Farbprinter
drucker =Farbprinter()
m = menu3.Menu(True)
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
colorcodeweg = lambda result : ansi_escape.sub('', result)

def dict_reverser(d):
    seen = set()
    return {v: k for k, v in d.items() if v not in seen or seen.add(v)}

def mit_leerzeichen_auffuellen(farbigesmenu, offsetlinks=3, offsetrechts=3):
    farbigesmenu = [(len(x), x) for x in farbigesmenu].copy()
    farbigesmenu.sort(reverse=True)
    farbigesmenu = {offsetlinks * ' ' + x[1] + (farbigesmenu[0][0] + 1 - x[0]) * ' ' +offsetrechts * ' ' :x[1]   for x in farbigesmenu}
    return farbigesmenu.copy()

def create_color_menu(farbigesmenu, menuinfo="Welche Antwort ist richtig?", aufforderung="Deine Antwort oder 'q', um das Programm zu beenden: ", gewaehlteantwort='Deine Wahl: '):
    farbigesmenufertig = []
    funktionsauswahl = [drucker.f.black.brightred.normal, drucker.f.black.brightwhite.normal, drucker.f.black.brightmagenta.normal, drucker.f.black.brightgreen.normal, drucker.f.black.magenta.normal, drucker.f.black.brightcyan.normal, drucker.f.black.brightyellow.normal, drucker.f.black.brightblue.normal]
    farbigesmenudict = mit_leerzeichen_auffuellen(farbigesmenu)
    farbigesmenu = [x for x in farbigesmenudict.keys()]
    if len(farbigesmenu) > len(funktionsauswahl):
        funktionsauswahl = funktionsauswahl * len(farbigesmenu)
    for menuitem, farbe in zip(farbigesmenu, funktionsauswahl):
        farbigesmenufertig.append(farbe(menuitem))
    c = m.menu(menuinfo, farbigesmenufertig, aufforderung)
    antwort = colorcodeweg(farbigesmenu[c - 1])
    antwort = farbigesmenudict[antwort]
    m.success(gewaehlteantwort + antwort)
    return antwort





