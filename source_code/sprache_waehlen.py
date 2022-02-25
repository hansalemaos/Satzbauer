import pandas as pd
from farbprinter.farbprinter import Farbprinter
drucker = Farbprinter()
import re

def get_sprache(textanzeigen):
    df = pd.read_pickle('SPRACHENWAEHLEN_DF.PKL')
    dfa = []
    fehlerdrucken=False
    fehlermeldung = ''
    eingabe =''
    while not any(dfa):
        try:
            drucker.p_pandas_list_dict(df)
            if fehlerdrucken is True:
                print(drucker.f.brightred.black.bold(f'\n{eingabe} konnte nicht verstanden werden!\nFehler:{fehlermeldung}\nBitte noch einmal probieren\n'))
            eingabe = input(drucker.f.black.brightyellow.bold(f"\n{textanzeigen}. \nGültige Eingaben für Deutsch sind beispielsweise: ['52', 'German', 'de', 'ger', 'deu']\n\n"))
            eingabe=eingabe.strip()
            if len(eingabe) == 2 and not eingabe.isnumeric():
                dfa = df.loc[df.iso_6391.str.contains(rf'^{eingabe}$', regex=True)].iloc[0].to_list()
                continue
            elif len(eingabe) == 3 and not eingabe.isnumeric():
                try:
                    dfa = df.loc[df.iso_6392.str.contains(rf'^{eingabe}$', regex=True)].iloc[0].to_list()
                    continue
                except:
                    dfa = df.loc[df.iso_6393.str.contains(rf'^{eingabe}$', regex=True)].iloc[0].to_list()
                    continue
            try:
                dfa = df.loc[eingabe].to_list()
                continue
            except:
                dfa = df.loc[df.language.str.contains(rf'^{eingabe}$', regex=True, flags=re.IGNORECASE)].iloc[0].to_list()
        except Exception as Fehler:
            fehlermeldung=Fehler
            fehlerdrucken=True
            continue
    print(drucker.f.brightgreen.black.bold(f'\nGewählte Sprache:\n{dfa}\n'))
    return dfa

