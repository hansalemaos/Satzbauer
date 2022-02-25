import os
import subprocess
import sys
from time import sleep

import requests
import bs4
import spacy

from einfuehrung import einfuehrung
from menudownload import *
import de_dep_news_trf
satzanalyse_werkzeug = de_dep_news_trf.load()
import regex
import pickle
from satzmetzger.satzmetzger import Satzmetzger
import numpy as np
linebreaknach = 70
prompt = drucker.f.black.magenta.normal('''Wahrscheinlich sind einige der Wörter falsch! \nDu musst diese Wörter korrigeren!\nGib die Nummer, die vor dem Wort steht ein, um das Wort zu korrgieren!\nGib q ein, um das Programm zu beenden!\n''')
return_choice =  drucker.f.black.brightcyan.italic(" <-- Gib diese Nummer ein, wenn du alles korrigiert hast!\n")
kurzbeschreibung_aufgabe = drucker.f.black.brightyellow.italic("\nKorrigiere die Fehler! Gib die letzte Zahl in der Liste ein, sobald du fertig bist! Dein Ziel ist, auf 100% Übereinstimmung zu kommen!\n")
tagsmitbesipiele = 'beispieletigertags.pkl'


def read_pkl(filename):
    with open(filename, "rb") as f:
        data_pickle = pickle.load(f)
    return data_pickle


def transpose_list_of_lists(listexxx):
    try:
        return [list(xaaa) for xaaa in zip(*listexxx)]
    except Exception as Fehler:
        print(Fehler)
        try:
            return np.array(listexxx).T.tolist()
        except Exception as Fehler:
            print(Fehler)
            return listexxx


def delete_duplicates_from_nested_list(nestedlist):
    tempstringlist = {}
    for ergi in nestedlist:
        tempstringlist[str(ergi)] = ergi
    endliste = [tempstringlist[key] for key in tempstringlist.keys()]
    return endliste.copy()


def flattenlist_neu_ohne_tuple(iterable):
    def iter_flatten(iterable):
        it = iter(iterable)
        for e in it:
            if isinstance(e, list):
                for f in iter_flatten(e):
                    yield f
            else:
                yield e

    a = [i for i in iter_flatten(iterable)]
    return a


def htmleinlesen(seitenlink):
    htmlcode = requests.get(seitenlink)
    suppe = bs4.BeautifulSoup(htmlcode.text, "html.parser")
    ganzertext = "\n".join([t.text for t in suppe.findAll("p")])
    return ganzertext


def txtdateien_lesen(text):
    try:
        dateiohnehtml = (
                b"""<!DOCTYPE html><html><body><p>""" + text + b"""</p></body></html>"""
        )
        soup = bs4.BeautifulSoup(dateiohnehtml, "html.parser")
        soup = soup.text
        return soup.strip()
    except Exception as Fehler:
        print(Fehler)


def get_file_path(datei):
    pfad = sys.path
    pfad = [x.replace('/', '\\') + '\\' + datei for x in pfad]
    exists = []
    for p in pfad:
        if os.path.exists(p):
            exists.append(p)
    return list(dict.fromkeys(exists))


def get_text():
    p = subprocess.run(get_file_path(r"Everything2TXT.exe")[0], capture_output=True)
    ganzertext = txtdateien_lesen(p.stdout)
    return ganzertext

einfuehrung('Satzbauer')
alletagsmitbeispiele = read_pkl(tagsmitbesipiele)
satzmetzgerle = Satzmetzger()
ganzertext = get_text()
einzelnesaetze = satzmetzgerle.zerhack_den_text(ganzertext)
allesaetzefertigfueraufgabe = []
allemoeglichenpunkte = 0
punktevomuser = 0
for satzindex, einzelnersatz in enumerate(einzelnesaetze):
    cfg = {}
    richtigersatz=''
    falschersatz=''
    print('\n')
    analysierter_text = satzanalyse_werkzeug(einzelnersatz)
    dokument_als_json = analysierter_text.doc.to_json()
    alleverbenimsatz = []
    schongedruckt = False
    komplettersatzanzeigen = drucker.f.brightred.black.italic('\n'+'Kompletter Satz: ') +  drucker.f.black.brightred.italic(dokument_als_json["text"] +'\n')
    for wordindex, token in enumerate(dokument_als_json["tokens"]):
        allemoeglichenpunkte = allemoeglichenpunkte+1
        farbigesmenufertig = []

        anfangwort = token["start"]
        endewort = token["end"]
        aktuelleswort = dokument_als_json["text"][anfangwort:endewort]
        leerzeichenplatz = len(dokument_als_json["text"][anfangwort:endewort]) * "_"
        platzhalter = (
                dokument_als_json["text"][:anfangwort]
                + leerzeichenplatz
                + dokument_als_json["text"][endewort:]
        )
        satzschongemacht = dokument_als_json["text"][:anfangwort]
        satzdrucken = drucker.f.black.white.italic('\nWir sind hier:   ') + drucker.f.white.black.normal(satzschongemacht) + drucker.f.brightyellow.black.italic(aktuelleswort) +  drucker.f.black.white.italic('\n')
        richtigpost = token['tag']


        for indi, tag in enumerate(alletagsmitbeispiele):

            antwort=''
            indexnummer='0'
            if indi + 1 < 10:
                indexnummer = drucker.f.magenta.black.normal(f'  {indi + 1}   ')
            elif indi + 1 >= 10:
                indexnummer = drucker.f.magenta.black.normal(f'  {indi + 1}  ')
            posart = drucker.f.black.cyan.normal(tag[-3].ljust(45))
            tags = drucker.f.black.brightgreen.normal(f' {tag[1]}'.ljust(9))
            beispiel = tag[-1]
            if indi + 1 < 10:
                farbigesmenufertig.append(f'    {indexnummer}{tags}{posart}{beispiel}')
            elif indi + 1 >= 10:
                farbigesmenufertig.append(f'{indexnummer}{tags}{posart}{beispiel}')
        menuinfo = "Welche Antwort ist richtig?"
        print(komplettersatzanzeigen)
        print(satzdrucken)
        aufforderung = drucker.f.black.brightyellow.normal("\n\tDeine Antwort oder 'q', um das Programm zu beenden: \n")
        aufforderungganz = komplettersatzanzeigen + satzdrucken  + aufforderung
        c = m.menu(menuinfo, farbigesmenufertig, aufforderungganz)
        try:
            antwort = regex.findall(r'^\s*\d+\s*([^\s]+)', colorcodeweg(farbigesmenufertig[c - 1]))[0]
        except:
            continue
        sleep(1)
        print(drucker.f.blue.brightwhite.normal(f'\n\n\tDeine Antwort ist: {antwort}\n\tDie richtige Antwort ist: {richtigpost}\n\n'))
        if antwort.strip() == richtigpost.strip():
            punktevomuser = punktevomuser +1
        print(drucker.f.cyan.brightwhite.italic(
            f'\n\n     Erreichte Punkte: {punktevomuser} von {allemoeglichenpunkte}            \n\n'))
        print(10 * '\n')




