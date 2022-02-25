from maximize_console import *
from farbprinter.farbprinter import Farbprinter
drucker = Farbprinter()
from add_color_print import add_color_print_to_regedit, updates_quero_estudar_alemao
def einfuehrung(name):
    print(1000 * "\n")
    maximize_console(lines=30000)
    add_color_print_to_regedit()
    colorfunctionslogo = [drucker.f.black.red.normal, drucker.f.black.brightyellow.normal]
    drucker.p_ascii_front_on_flag_with_border(
        text=name,
        colorfunctions=colorfunctionslogo,
        bordercolorfunction=drucker.f.brightgreen.black.italic,
        font="slant",
        width=1000,
        offset_from_left_side=5,
        offset_from_text=15,
    )
    colorfunctionspage = [
        drucker.f.black.brightwhite.normal,
        drucker.f.black.brightgreen.normal,
    ]
    drucker.p_ascii_front_on_flag_with_border(
        text="www . queroestudaralemao . com . br",
        colorfunctions=colorfunctionspage,
        bordercolorfunction=drucker.f.brightgreen.black.negative,
        font="slant",
        width=1000,
        offset_from_left_side=1,
        offset_from_text=1,
    )
    updates_quero_estudar_alemao()