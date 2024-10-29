#!python
# -*- coding: utf-8 -*-
"""
Title : auto_ZO_translate.py
Description : Script for translating dialogues and quest titles of the Steam game 'Z.O.N.A Origin' by AGaming+.
Author: peurKe
Creation Date: 2024-10-27
Last Modified: 2024-10-28
Version: 1.0
License: MIT
"""

# https://gist.github.com/williballenthin/8e3913358a7996eab9b96bd57fc59df2 (broken)
# https://gist.github.com/jedimasterbot/39ef35bc4324e4b4338a210298526cd0 (fixed)
# https://github.com/ssut/py-googletrans/issues/280
# https://medium.com/analytics-vidhya/removing-stop-words-with-nltk-library-in-python-f33f53556cc1

# pip install tqdm
# pip install googletrans==3.1.0a0
# pip install legacy-cgi
# pip install nltk
# pip install unidecode (? voir si besoin avec import 'unicodedata' aulieu de 'import unicodedata')
# pip install pyinstaller

# Error: Time out --> Problem with google translator API = Relaunch script
# Error: _ssl.c:1003: The handshake operation timed out --> Problem with google translator API = Relaunch script
# Error: [Errno 11001] getaddrinfo failed --> Internet connection problem = Check Internet connection and relanch script
# Error: bytes must be in range(0, 256) --> There is unicode character somewhere in element['translation'] string

import argparse
import sys
from os import path as os_path, makedirs as os_makedirs, listdir as os_listdir
import glob
import re
import time
from tqdm import tqdm
from unidecode import unidecode
import unicodedata
import json
import shutil
import binascii
from collections import namedtuple
try:
    # from nltk import download as nltk_download
    # from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from googletrans import Translator
except Exception as e:
    print(f" Error: {e}")
    input(" Press Enter to exit...")
    sys.exit(-1)

class bcolors:
    CYAN = '\033[96m'
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

DEFAULT_FILES = [
    'level0', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7',
    'level8', 'level9', 'level10', 'level11', 'level12', 'level13', 'level14', 'level15',
    'level16', 'level17', 'level18', 'level19', 'level20', 'level21', 'level22', 'level23',
    'level24', 'level25', 'level26', 'level27', 'level28', 'level29', 'resources.assets'
]

DEFAULT_ZONA_DIR_EXAMPLE = 'C:\\SteamLibrary\\steamapps\\common\\ZONAORIGIN'
DEFAULT_ZONA_DATA_DIR = './ZONAORIGIN_Data'
DEFAULT_ZONA_TRANSLATE_DIR = f"./auto_ZA_translate"
DEFAULT_ZONA_BACKUP_DIR = f"./auto_ZA_translate/BACKUP"
DEFAULT_ZONA_EXE_FILENAME = 'ZONAORIGIN.exe'

ASCII_BYTE = rb" #\/!\"'\(\)\+,\-\.0123456789:;<=>\?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

EXC_DIALOG_RE = [
    r"Z.O.N.A Project X VR,"
    r"Z.O.N.A: ORIGIN VR",
    r"UnityEngine",
    r"Primary:",
    r"root: scene",
    r"Teleport",
    r"MiniMap -",
    r"Assembly-CSharp",
    r"Unity.",
    r"HurricaneVR.Framework"
]
EXC_DIALOG_RE_ESC = [re.escape(x) for x in EXC_DIALOG_RE]

String = namedtuple("String", ["s", "offset"])

# English Stopwords
CUSTOM_EN_STOPWORDS = ['the', 'to', 'and', 'a', 'in', 'it', 'is', 'that', 'this', 'had', 'on', 'for', 'were', 'was']
# German Stopwords (But not containing English stopwords)
CUSTOM_DE_STOPWORDS = ['aber', 'abzug', 'alle', 'allem', 'allen', 'aller', 'alles', 'als', 'ander', 'andere', 'anderem', 'anderen', 'anderer', 'anderes', 'anderm', 'andern', 'anders', 'angekommen', 'auch', 'auf', 'bei', 'benutzt', 'ber', 'berfalls', 'berleben', 'berraschungen', 'bewegungen', 'bist', 'bleibt', 'damit', 'dann', 'derselbe', 'derselben', 'denselben', 'desselben', 'demselben', 'dieselbe', 'dieselben', 'dass', 'dasselbe', 'dazu', 'dein', 'deine', 'deinem', 'deinen', 'deiner', 'deines', 'den', 'denn', 'der', 'derer', 'des', 'dessen', 'dich', 'diesem', 'diesen', 'dieser', 'doch', 'dormitory', 'durch', 'ein', 'eine', 'einem', 'einen', 'einer', 'eines', 'einheit', 'einig', 'einige', 'einigem', 'einigen', 'einiger', 'einiges', 'einmal', 'erinnert', 'ihm', 'etwas', 'euer', 'eure', 'eurem', 'euren', 'eurer', 'eures', 'fur', 'gesch', 'gegen', 'gewehr', 'gewesen', 'gibt', 'habe', 'haben', 'hatte', 'hatten', 'hauptquartier', 'hilft', 'hin', 'hinter', 'ich', 'im', 'kamera', 'kugelflug', 'mich', 'mir', 'ihr', 'ihm', 'ihn', 'ihnen', 'indem', 'infizierte', 'ist', 'jede', 'jedem', 'jeden', 'jeder', 'jedes', 'jener', 'jenem', 'jenen', 'jener', 'jenes', 'jetzt', 'kalorien', 'kann', 'kannst', 'kein', 'keine', 'keinem', 'keinen', 'keiner', 'keines', 'konnen', 'konnte', 'machen', 'manchem', 'manchen', 'mancher', 'manches', 'mein', 'meine', 'meinem', 'meinen', 'meiner', 'meines', 'monolithen', 'muss', 'musste', 'nach', 'nicht', 'nichts', 'nun', 'nur', 'nutzen', 'oder', 'ohne', 'patrone', 'patronem', 'perfekt', 'perfekte', 'risches', 'sehr', 'sein', 'seine', 'seinem', 'seinen', 'seiner', 'seines', 'selbst', 'sich', 'sie', 'siehst', 'sind', 'solche', 'solchem', 'solchen', 'solcher', 'solches', 'sollte', 'sondern', 'sonst', 'sowohl', 'uber', 'und', 'uns', 'unser', 'unsere', 'unserem', 'unseren', 'unseres', 'unter', 'verbrennen', 'viel', 'vom', 'vor', 'vorbereiten', 'wahrend', 'waren', 'warst', 'weg', 'welche', 'welchem', 'welchen', 'welcher', 'welches', 'welt', 'wenn', 'werde', 'werden', 'wie', 'wieder', 'wir', 'wird', 'wirst', 'wollen', 'wollte', 'wohnheim', 'wurde', 'wurden', 'zug', 'zum', 'zur', 'zwar', 'zwischen']

CUSTOM_TARGET_STOPWORDS = {
    "en": [
        ['the', 'to', 'and', 'a', 'in', 'it', 'is', 'I', 'that', 'this', 'had', 'on', 'for', 'were', 'was']
    ],
    # # BEGIN LAST STOPWORDS FR OK
    # "fr": [
    #     ['me', 'te', 'se', 'moi', 'toi', 'lui', 'leur', 'le', 'la', 'les', 'on', 'y', 'en', 'ce', 'cela', 'ça', 'celui', 'celle', 'ceux', 'celles', 'qui', 'que', 'quoi', 'dont', 'ou'],
    #     ['a', 'alors', 'au', 'aucun', 'aussi', 'autre', 'avant', 'avec', 'avoir', 'bon', 'car', 'ces', 'ceux', 'chaque', 'comme', 'comment', 'dans', 'de', 'des', 'du', 'donc', 'elle', 'en', 'encore', 'entre', 'et', 'eux', 'faire', 'il', 'je', 'juste', 'la', 'le', 'les', 'leur', 'lui', 'mais', 'mes', 'moi', 'mon', 'ne', 'nos', 'notre', 'nous', 'par', 'pour', 'quand', 'sa', 'se', 'ses', 'son', 'sur', 'ta', 'te', 'tes', 'toi', 'ton', 'tout', 'tres', 'tu', 'un', 'une', 'vos', 'votre', 'vous'],
    #     ['afin', 'apres', 'aujourd', 'aucune', 'auquel', 'aura', 'auront', 'aussi', 'autour', 'auxquelles', 'auxquels', 'autant', 'autres', 'avant', 'avec', 'c', 'ceci', 'celle', 'celles', 'celui', 'cent', 'cependant', 'certain', 'certaine', 'certaines', 'certains', 'cet', 'cette', 'ceux', 'chacun', 'chaque', 'chez', 'ci', 'cinq', 'combien', 'comment', 'comme', 'd', 'dans', 'de', 'dedans', 'dehors', 'depuis', 'des', 'deux', 'devrait', 'doit', 'donc', 'dont', 'douze', 'du', 'elle', 'elles', 'en', 'encore', 'entre', 'environ', 'est', 'et', 'etaient', 'etaient', 'etait', 'etant'],
    #     ['etre', 'eu', 'fait', 'fais', 'faisaient', 'faites', 'fois', 'font', 'force', 'hors', 'ici', 'il', 'ils', 'je', 'jusqu', 'juste', 'l', 'la', 'laquelle', 'le', 'les', 'leur', 'leurs', 'longtemps', 'lors', 'lorsque', 'lui', 'ma', 'maint', 'mais', 'malgre', 'me', 'memes', 'moins', 'mon', 'moyen', 'ni', 'nombreuses', 'nombreux', 'notamment', 'notre', 'nous', 'nouveau', 'nul', 'on', 'ont', 'par', 'parce', 'parfois', 'parmi', 'part', 'pendant', 'personne', 'peu'],
    #     ['peut', 'peuvent', 'plus', 'plusieurs', 'plutot', 'pour', 'pourquoi', 'qu', 'quand', 'que', 'quel', 'quelle', 'quelles', 'quels', 'qui', 'quoi', 'sa', 'sans', 'se', 'selon', 'serait', 'si', 'sien', 'sienne', 'siens', 'soi', 'soit', 'son', 'sont', 'sous', 'soyez', 'suffit', 'suis', 'sujet', 'sur', 'ta', 'tandis', 'tel', 'telle', 'telles', 'tels', 'tes', 'toi', 'ton', 'tous', 'tout', 'toutes', 'tres', 'tu', 'un', 'une', 'va', 'vers', 'vif', 'vifs', 'voir'],
    #     ['vos', 'votre', 'vous', 'vu', 'y', 'a', 'afin', 'ailleurs', 'ainsi', 'ajoute', 'ajouter', 'alors', 'apres', 'aucun', 'aucune', 'aupres', 'auquel', 'aussi', 'autant', 'autour', 'aux', 'autres', 'avant', 'avec', 'avoir', 'ce', 'cela', 'celles', 'celui', 'cent', 'cependant', 'certains', 'ces', 'ceux', 'chaque', 'chez', 'comme', 'comment', 'd', 'dans', 'de', 'dedans', 'dehors', 'depuis', 'des', 'dix', 'doit', 'donc', 'dont', 'douze', 'du', 'elle', 'elles', 'en']
    # ],
    # # END LAST STOPWORDS FR OK
    "fr": [
        [ 'le', 'de', 'un', 'et', 'en', 'la', 'les', 'du', 'des', 'pour', 'dans', 'que', 'qui', 'il', 'elle', 'nous', 'vous', 'ils', 'ne',
          'au', 'avec', 'sur', 'ce', 'sa', 'ses', 'son', 'mon', 'ma', 'mes', 'ton', 'ta', 'tes', 'ou', 'par', 'se', 'cette', 'cet', 'a', 'sont',
          'moi', 'toi', 'lui', 'elle', 'eux', 'leur', 'leurs', 'y', 'on', 'te', 'me', 't', 'm', 'est', 'tous', 'toutes', 'ces', 'ceux', 'bien',
          'ainsi', 'cela', 'soit', 'comme', 'encore', 'alors', 'avant', 'depuis', 'chez', 'tres', 'peu', 'autre', 'entre', 'sans', 'apres', 'donc', 'meme', 'vers',
          'autres', 'aucun', 'aucune', 'chacun', 'chaque', 'quel', 'quelle', 'quels', 'quelles', 'quelque', 'quelques', 'souvent', 'tandis', 'toutefois', 'contre', 'hors', 'selon',
          'desormais', 'parfois', 'partout', 'pres', 'loin', 'dela', 'autant', 'certain', 'certaines', 'certains', 'dessus', 'dessous', 'ci', 'pourquoi', 'lorsque', 'comment' ]
    ],
    "cs": [
        [ 'me', 'te', 'se', 'ja', 'ty', 'on', 'jej', 'to', 'ta', 'ty', 'my', 'vy', 'oni', 'to', 'to', 'to', 'ten', 'ta', 'ti', 'kdo', 'co', 'co', 'o', 'nebo',
          'a', 'ale', 'ani', 'bude', 'by', 'byl', 'co', 'do', 'i', 'jak', 'jako', 'je', 'jeji', 'jen', 'jsem', 'jsme', 'jsou', 'jste', 'k', 'kdyz', 'mam', 'ma', 'musi', 'na', 'nad', 'nebo', 'po', 'pro', 'se', 'si', 'tak', 'ten', 'to', 'tu', 'tuto', 'ty', 'uz', 'v', 've', 'z', 'za',
          'aby', 'aj', 'anebo', 'asi', 'atd', 'avsak', 'b', 'bez', 'byla', 'byli', 'bylo', 'byt', 'coz', 'dale', 'dalsi', 'dva', 'dve', 'jejich', 'jestli', 'jeste', 'jinak', 'kazdy', 'kde', 'kdo', 'kdy', 'ke', 'ktera', 'ktere', 'ktery', 'kvuli', 'mame', 'mate', 'me', 'muj', 'mne', 'nam', 'nami', 'naproti', 'nejvice', 'nekde', 'nekdo', 'nic', 'nich', 'nim', 'ni', 'nejaky', 'nektery',
          'ani', 'aspon', 'budou', 'coz', 'cz', 'den', 'deset', 'devet', 'docela', 'dvacet', 'dvanact', 'jenom', 'jich', 'jiz', 'jini', 'jiny', 'kdyby', 'kolik', 'mezi', 'mit', 'moje', 'nejsou', 'nej', 'nekolik', 'nestaci', 'nez', 'nemu', 'nemuz', 'on', 'ona', 'oni', 'ono', 'ony', 'pod', 'podle', 'proto', 's', 'takze', 'tato', 'tenhle', 'tento', 'tohle', 'totiz', 'tvuj', 'tyhle', 'tyto', 'veskery', 'vlastne',
          'abych', 'abychom', 'abys', 'abyste', 'ak', 'aniz', 'apod', 'asi', 'behem', 'coby', 'cim', 'cimz', 'jenz', 'ktery', 'ktery', 'ktery', 'li', 'mezi', 'muze', 'nahle', 'naopak', 'obe', 'ostatne', 'par', 'podel', 'porad', 'prvni', 'rovne', 'sam', 'sam', 'shora', 'spis', 'stezi', 'sve', 'svuj', 'takhle', 'tamhle', 'takovy', 'takrka', 'tohle', 'tudiz', 'vcelku', 'vetsina', 'vubec', 'vetsinou',
          'ackoli', 'avsak', 'budes', 'budu', 'byti', 'casto', 'dle', 'docela', 'iz', 'kamz', 'kdez', 'kdyzkoliv', 'kol', 'krom', 'lec', 'leda', 'malo', 'mati', 'mozno', 'nadale', 'nac', 'nekam', 'nekterych', 'nektery', 'nekteryz', 'nekudy', 'nemu', 'odtamtud', 'onem', 'prave', 'prostrednictvim', 'pripadne', 'pricemz', 'sam', 'skrz', 'smer', 'tamtudy', 'vne', 'vzdyť', 'zkratka', 'znovu', 'zpet', 'zticha' ]
    ],
    "it": [
        [ 'di', 'a', 'da', 'in', 'che', 'e', 'il', 'la', 'un', 'una', 'per', 'con', 'su', 'io', 'tu', 'lui', 'lei', 'noi', 'voi', 'loro',
          'gli', 'le', 'lo', 'mi', 'ti', 'ci', 'vi', 'questo', 'quello', 'cui', 'ma', 'o',
          'quanto', 'quella', 'mio', 'tuo', 'suo', 'nostro', 'vostro', 'la', 'qui', 'già', 'sia', 'cosi',
          'dove', 'perche', 'ancora', 'sotto', 'sopra', 'tra', 'fra', 'se', 'quando', 'come', 'poi', 'dopo',
          'mentre', 'davanti', 'contro', 'verso', 'intanto', 'quindi', 'ora', 'poco', 'molto', 'tanto', 'altro', 'sempre', 'alcuno', 'alcuna', 'alcuni', 'alcune', 'al', 'allo', 'agli', 'dagli', 'dagli', 'agli', 'dagli' ]
    ],
    "es": [
        [ 'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'se', 'del', 'las', 'un', 'por', 'con', 'una', 'su', 'para', 'es', 'al', 'lo',
          'como', 'mas', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'si', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'tambien',
          'todo', 'nos', 'algo', 'poco', 'mismo', 'ella', 'ellos', 'uno', 'otro', 'ese', 'aquel', 'cual', 'nada', 'cada', 'estos', 'algun', 'algunos',
          'aqui', 'alli', 'alla', 'antes', 'despues', 'tal', 'donde', 'quien', 'cuyo', 'alrededor', 'cerca', 'lejos', 'durante', 'contra', 'segun', 'hasta', 'aunque',
          'ademas', 'demasiado', 'ambos', 'incluso', 'algunas', 'mucho', 'pues', 'cuales', 'cierto', 'hacia', 'ningun', 'otros', 'tanto', 'cuanto', 'tantos', 'talvez', 'quizas',
          'usted', 'vosotros', 'vuestro', 'mio', 'tuyo', 'suyo', 'nuestro', 'mientras', 'acerca', 'durante', 'via', 'respecto', 'mediante', 'pese', 'junto', 'apenas', 'siempre', 'ninguno', 'alguien', 'algunas', 'cualquiera' ]
    ],
    "ro": [
        ['si', 'in', 'pe', 'cu', 'de', 'la', 'un', 'o', 'pentru', 'este', 'sunt', 'ca', 'sa', 'mai', 'dar', 'cel', 'oare', 'ori', 'fie'],
        ['care', 'acest', 'acea', 'aceasta', 'aceste', 'acestia', 'acelasi', 'altii', 'astfel', 'cand', 'cat', 'tot', 'fi', 'doar', 'intre', 'din', 'fara', 'daca'],
        ['cum', 'unde', 'acei', 'ceva', 'acolo', 'altceva', 'cineva', 'nimic', 'fiecare', 'altul', 'parca', 'cam', 'deci', 'aceasta', 'acestea', 'asa', 'acum', 'cine'],
        ['candva', 'anumite', 'aproape', 'pana', 'inca', 'totusi', 'desi', 'incat', 'decate', 'caci', 'decand', 'destul', 'dela', 'langa', 'mereu', 'oricum', 'undeva'],
        ['toate', 'asemenea', 'din cauza', 'astazi', 'ieri', 'maine', 'impreuna', 'pentru', 'deoarece', 'sub', 'prin', 'astfel incat', 'cui', 'oricine', 'fiecare', 'unii'],
        ['cumva', 'acestora', 'acelor', 'asa cum', 'inclusiv', 'printre', 'candva', 'destule', 'atunci', 'cativa', 'oricare', 'totdeauna', 'vreo', 'aproximativ', 'exceptand', 'adesea', 'candva', 'spre', 'afara']
    ],
    "pl": [
        [ 'a', 'w', 'z', 'do', 'na', 'i', 'oraz', 'to', 'jest', 'by', 'jak', 'co', 'ze', 'czy', 'on', 'ona', 'my', 'wy', 'oni',
          'tam', 'ten', 'ta', 'nas', 'was', 'od', 'za', 'po', 'przez', 'wtedy', 'gdzie', 'kiedy', 'jako', 'bylo', 'bym', 'byc', 'w', 'dla',
          'moj', 'twoj', 'jego', 'ich', 'nasz', 'tego', 'taki', 'wszystko', 'wiele', 'dosc', 'wszystkich', 'kazdy', 'nigdy', 'nieco', 'niezle', 'czyli', 'mniej', 'raczej',
          'ale', 'lecz', 'poniewaz', 'chociaz', 'zatem', 'mimo', 'zawsze', 'teraz', 'nadal', 'jakos', 'wiecej', 'ktory', 'ktora', 'wszyscy', 'wszystkie', 'oby', 'a',
          'tylko', 'jeszcze', 'inny', 'wszelki', 'gdziekolwiek', 'ktokolwiek', 'jakikolwiek', 'ponad', 'czyz', 'wczesniej', 'na pewno',
          'z', 'o', 'przy', 'na', 'od', 'mi', 'nim', 'swoje', 'swoj', 'tak', 'trzeba', 'zbytnio', 'obok', 'ponizej', 'zgodnie', 'czym', 'zreszta' ]
    ]
}

RESTORE_SPECIFIC_WORDS = {
    'en':[
        { "from": " n't", "to": "n't" }
    ],
    'fr': [
        { "from": "origine vr", "to": "ORIGIN VR" },
        { "from": "harceleur", "to": "stalker" },
        { "from": "traqueur", "to": "stalker" },
        { "from": "couleur",   "to": "color" },
        { "from": "œ", "to": "oe" },
        { "from": "Tournees magazine", "to": "Balles dans chargeur" },
        { "from": "Vitesse vol balle", "to": "Vitesse des balles"}
    ],
    'cs': [
        { "from": "puvod vr", "to": "ORIGIN VR" },
        { "from": "tracker", "to": "stalker" },
        { "from": "barva",   "to": "color" }
    ],
    "it": [
        { "from": "origine vr", "to": "ORIGIN VR" },
        { "from": "tracker", "to": "stalker" },
        { "from": "colore",   "to": "color" }
    ],
    "es": [
        { "from": "origen vr", "to": "ORIGIN VR" },
        { "from": "acosador", "to": "stalker" },
        { "from": "rastreador", "to": "stalker" }
    ],
    "ro": [
        { "from": "origine vr", "to": "ORIGIN VR" },
        { "from": "urmaritor", "to": "stalker" },
        { "from": "tracker", "to": "stalker" },
        { "from": "culoare",   "to": "color" }
    ],
    "pl": [
        { "from": "pochodzenie vr", "to": "ORIGIN VR" },
        { "from": "tracker", "to": "stalker" },
        { "from": "kolor",   "to": "color" }
    ],
    'all': [
        # { "from": "< ", "to": "<" },
        # { "from": " >", "to": ">" },
        # { "from": " <", "to": "<" },
        # { "from": "> ", "to": ">" }, # </color>- | </color>:
        { "from": " # ", "to": "#" },
        { "from": " :", "to": ":" },
        { "from": " ,", "to": "," },
        { "from": " .", "to": "." },
        { "from": " !", "to": "!" },
        { "from": " ?", "to": "?" },
        { "from": " ’ ", "to": " " },
        { "from": " ' ", "to": " " },
        { "from": "’", "to": "'" },
        # # { "from": "``", "to": "\"" },  # <color>``X``</color> --> <color>\"X\"</color>
        # { "from": "`", "to": "" }  # <color>``X``</color> --> <color>X</color>
    ]
}

def is_dialog_string(dialog):
    # Exclude string containing only whitespace
    if dialog.isspace():
        return False
    # Exclude string not containing at least one whitespace
    if not re.search(r' ', dialog):
        return False
    # Exclude string terminate with ':', '-', ': ', '- ' (or with only several whitespaces at the end)
    if re.search(r'[-:]{1}\s*$', dialog):
        return False
    # # Exclude color format string not containing ': ' or '- '
    # if re.search(r'(<color=|</color>)', dialog):
    #     if not re.search(r'(- |: )', dialog):
    #         return False
       
    # Exclude and include with regex stringd
    exc_dialog_re = re.compile('|'.join(EXC_DIALOG_RE_ESC), re.IGNORECASE)
    if exc_dialog_re.search(dialog):
        return False
    return True

def ascii_strings(buf, n=4, start_from=0):
    reg = rb"([%s]{%d,})" % (ASCII_BYTE, n)
    ascii_re = re.compile(reg)
    for match in ascii_re.finditer(buf):
        ascii_string = match.group().decode("ascii")
        # print("0x{:x}:{:s}".format(start_from + match.start(), ascii_string))
        if not is_dialog_string(ascii_string):
            continue
        ascii_address = start_from + match.start()
        yield String(ascii_string, ascii_address)

def dialog_exclude_lang(dialog, lang='de', skip=False):
    if skip:
        return False
    # Replace all special characters by whitespaces
    re.sub(r'[^a-zA-Z0-9\s]', ' ', dialog)
    # Set tokens
    tokens = word_tokenize(dialog)
    # Set stopwords for lang
    if lang == 'de':
        requested_exclude_lang = CUSTOM_DE_STOPWORDS
    else:
        requested_exclude_lang = CUSTOM_DE_STOPWORDS

    # Exclude lang
    if any(item.lower() in requested_exclude_lang for item in tokens):
        return True
    return False

def remove_specials(text):
    # return text.replace('"', '')
    return re.sub(r'[^a-zA-Z0-9\s\.,!?:]', '', text)

def remove_accents(text):
    # text = unicodedata.normalize('NFKD', text)
    # return "".join([c for c in text if not unicodedata.combining(c)])
    return unidecode(text)

def restore_translated_words(text, lang='en'):
    for restore_word in RESTORE_SPECIFIC_WORDS[lang]:
        text = text.replace(restore_word['from'], restore_word['to'])
    return text

def dialog_filter(dialog, lang='en', remove_accent=True, target_length=0):
    if '</color>' in dialog:
        sep = '</color>'
        dialog_list = dialog.split(sep)
    # elif '</color>-' in dialog:
    #     sep = '</color>'
    #     dialog_list = dialog.split(sep)
    else:
        sep = ''
        dialog_list = ['', dialog]

    color = dialog_list[0]
    dialog = dialog_list[1]

    # Remove all accentuation characters
    dialog = remove_accents(dialog)
    # Split text to a list of words
    tokens = word_tokenize(dialog)
    # Remove stop words
    for requested_stopwords in CUSTOM_TARGET_STOPWORDS[lang]:
        dialog_filtered_list = [t for t in tokens if t.lower() not in requested_stopwords]
        dialog = ' '.join(dialog_filtered_list)
        # Current stopwords set is not enough, go to next stopwords set
        if len(dialog) > target_length:
            tokens = word_tokenize(dialog)
            continue
    # Restore specific words in translated lang
    dialog = restore_translated_words(dialog, lang=lang)
    # Restore specific words for all langs
    dialog = restore_translated_words(dialog, lang='all')
    return f"{color}{sep}{dialog}"

def dialog_translate(src, dialog, to='fr'):
    if '</color>' in dialog:
        sep = '</color>'
        dialog_list = dialog.split(sep)
    # elif '</color>' in dialog:
    #     sep = '</color>'
    #     dialog_list = dialog.split(sep)
    else:
        sep = ''
        dialog_list = ['', dialog]

    color = dialog_list[0]
    dialog = dialog_list[1]

    # Remove all special characters
    dialog = remove_specials(dialog)

    # Translate dialog string
    dialog =  src.translate(dialog, dest=to).text
    return f"{color}{sep}{dialog}"

def dialog_quest_only(dialog):
    to_include = [
        'Find ', 'Inform ', 'Reach ', 'Clear ', 'Return ', 'Wait ', 'Inverstigate ',
        'Disable ', 'specifically at',  # Truncated one
        'Explore ', 'find the Obelisk',  # Truncated one
    ]
    # /!\ Fix ASCII character as binary character in dialog
    # 'Return to the base and tell Strizh that he was deceived.j'
    to_exclude = [ 'Return to the base and tell Strizh that he was deceived' ]
        
    pattern_inc = '|'.join(map(re.escape, to_include))
    pattern_exc = '|'.join(map(re.escape, to_exclude))
    if re.match('^' + pattern_inc + '.', dialog):
        if re.match('^' + pattern_exc + '.', dialog):
            return False
        return True
    return False

def get_address_from_binary(file_desc, file, search_hex, search_txt):
    file_desc.seek(0)
    offset_int = file_desc.read().find(bytes.fromhex(search_hex))
    return offset_int

def backup_files():
    print(f" • [Create backup in '{DEFAULT_ZONA_BACKUP_DIR}/' directory] ...")
    os_makedirs(DEFAULT_ZONA_BACKUP_DIR)
    # All 'levelNN' original files
    files_to_copy = [os_path.join(DEFAULT_ZONA_DATA_DIR, f) for f in os_listdir(DEFAULT_ZONA_DATA_DIR) if f.startswith('level') and not f.endswith('.resS')]
    # Unique 'resources.assets' original file
    files_to_copy.append(f"{DEFAULT_ZONA_DATA_DIR}/resources.assets")
    # Copy all original files in backup directory
    for file in files_to_copy:
        backup_file = os_path.join(DEFAULT_ZONA_BACKUP_DIR, os_path.basename(file))
        shutil.copy2(file, backup_file)
    print(f" • {bcolors.OK}[Create backup in '{DEFAULT_ZONA_BACKUP_DIR}/' directory] OK{bcolors.ENDC}\n")

def restore_files(src=DEFAULT_ZONA_BACKUP_DIR):
    print(f" • [Restore files from '{src}/' directory to '{DEFAULT_ZONA_DATA_DIR}/'] ...")
    if not os_path.exists(src):
        print(f" • {bcolors.FAIL}[Restore files from '{src}/' directory impossible because directory does not exist] Failed{bcolors.ENDC}\n")
        if src == DEFAULT_ZONA_BACKUP_DIR:
            print(f" {bcolors.WARN}Tip: Use the Steam 'Check integrity of game files' button located in 'Installed files' tab in the Z.O.N.A Origin's game properties.{bcolors.ENDC}\n")
        input(" Press Enter to exit...\n")
        sys.exit(-1)

    # All backup files
    files_to_copy = [os_path.join(src, f) for f in os_listdir(src)]
    # Copy all backup files in data directory
    for file in files_to_copy:
        data_file = os_path.join(DEFAULT_ZONA_DATA_DIR, os_path.basename(file))
        shutil.copy2(file, data_file)
    print(f" • {bcolors.OK}[Restore files from '{src}/' directory to '{DEFAULT_ZONA_DATA_DIR}/'] OK{bcolors.ENDC}\n")


def main():
    try:
        if not os_path.exists(DEFAULT_ZONA_EXE_FILENAME):
            print(f" {bcolors.FAIL}")
            print(f" Error: Move this script in the same directory as the 'ZONAORIGIN.exe' executable file (usually in the '{DEFAULT_ZONA_DIR_EXAMPLE}' directory).\n")
            print(f" Then run this moved script again.")
            print(f" {bcolors.ENDC}\n")
            sys.exit(-1)

        argparser = argparse.ArgumentParser()
        argparser.add_argument("-l", "--lang", type=str, default='empty', choices=['empty', 'fr', 'cs', 'it', 'es', 'ro', 'pl'], help="language to translate to")
        argparser.add_argument("-f", "--files", type=str, default='empty', help="comma separated str. Default is with all 'levelNN' and 'resources.assets' files")
        argparser.add_argument("-s", "--min-size", type=int, default=15, help="minimum size for string to translate is set to 15")
        argparser.add_argument("-r", "--restore", action='store_true', help="restore backup files (reset)")

        args = argparser.parse_args()
    
        i_lang = args.lang
        i_files = args.files.split(',')
        i_min_size = args.min_size
        i_restore = args.restore

        # RESTORE: Create backup file in backup directory if not already existing
        if i_restore:
            if os_path.exists(DEFAULT_ZONA_BACKUP_DIR):
                restore = ''
                while restore not in ['y', 'n']:
                    restore = str(input(f"{bcolors.CYAN}Confirm you want to restore backup files (y/n): {bcolors.ENDC}")).lower().strip()
                if restore == 'y':
                    restore_files()
            else:
                print(f" • {bcolors.FAIL}[Restore files from '{DEFAULT_ZONA_BACKUP_DIR}/' directory impossible because directory does not exist] Failed{bcolors.ENDC}\n")
                print(f" {bcolors.WARN}Tip: Use the Steam 'Check integrity of game files' button located in 'Installed files' tab in the Z.O.N.A Origin's game properties.{bcolors.ENDC}\n")
                input(" Press Enter to exit...\n")
                sys.exit(1)

        # TRANSLATE
        else:
            print(f" {bcolors.WARN}")
            print(f" // PREREQUISITES:")
            print("    • Your 'Z.O.N.A Origin' game must be up to date.")
            print("    • You must authorise this script in your firewall (API requests from the Online Google translator are required).\n")
            print("    Press Ctrl+C to exit if you need to update 'Z.O.N.A Origin' game before translate...")
            input("    Press Enter to translate 'Z.O.N.A Origin' game...")
            print(f" {bcolors.ENDC}")

            # BEGIN GUI execution
            if not i_restore:
                restore = ''
                while restore not in ['y', 'n']:
                    restore = str(input(f" {bcolors.CYAN}Do you want to restore backup files before translate ? (y/n): {bcolors.ENDC}")).lower().strip()
                if restore == 'y':
                    restore_files()

            if i_lang == 'empty':
                i_lang = ''
                while i_lang not in ['fr', 'cs', 'it', 'es', 'ro', 'pl']:
                    i_lang = str(input(f" {bcolors.CYAN}Language to translate to (fr|cs|it|es|ro|pl): {bcolors.ENDC}")).lower().strip()
            # END GUI execution
        
            # Save 'i_min_size' for 'resources.assets'
            i_min_size_saved = i_min_size

            # Default 'i_files'
            if i_files == ['empty']:
                i_files = DEFAULT_FILES

            print(f" {bcolors.WARN}")
            print(f" // PARAMETERS:")
            print(f"    • translate from .................... : 'en'")
            print(f"    • translate to ...................... : '{i_lang}'")
            print(f"    • minimum size string to translate .. : {i_min_size}")
            print(f"    • files to translate ................ : {i_files}\n")
            print(f" {bcolors.ENDC}")

            # Download nltk 'stopwords' and 'punkt_tab'
            # nltk_download('stopwords')
            # nltk_download('punkt_tab')
            # stops = set(stopwords.words('german'))
            # stops = set(stopwords.words('french'))
            # stops = set(stopwords.words('czech'))
            # print(stops)
            # input(" Press Enter to continue...")
            # sys.exit(0)
            
            # Initialize Google Translator
            translator = Translator()

            # Create backup file in backup directory if not already existing
            if os_path.exists(DEFAULT_ZONA_BACKUP_DIR):
                print(f" • {bcolors.OK}[Backup in '{DEFAULT_ZONA_BACKUP_DIR}/' directory already exists] OK{bcolors.ENDC}\n")
            else:
                backup_files()

            print(f" • [Translate from 'en' to '{i_lang}'] ...\n")
            
            # BEGIN Translate to i_lang
            
            # Create relative translate dir for lang file destination
            TRANSLATE_DIR_PATH = f"{DEFAULT_ZONA_TRANSLATE_DIR}/{i_lang}"
            if not os_path.exists(TRANSLATE_DIR_PATH):
                os_makedirs(TRANSLATE_DIR_PATH)

            # print
            # print(f" • [Translate from 'en' to '{i_lang}'] ...")

            # for i_file in i_files:
            for i_file in tqdm(i_files):

                i_file_translated = f"{TRANSLATE_DIR_PATH}/{i_file}"
                i_file = f"{DEFAULT_ZONA_DATA_DIR}/{i_file}"
            
                # print(f" • [Translate from 'en' to '{i_lang}'] {i_file} ...")

                with open(i_file, 'rb') as f:
                    if i_file == 'resources.assets':
                        # 'i_min_size' for 'resources.assets' cannot be too big. Some quests (as 'Explore ' one ) are truncated with non-ascii characters.
                        if i_min_size > 6:
                            i_min_size = 6
                        # Only 'resources.assets' file
                        start_from_hex_0 = "41 46 55 20 5F 4F 54 53 54 55 50 4E 49 4B"  # AFU _OTSTUPNIK
                        start_from_int_0 = get_address_from_binary(f, i_file, start_from_hex_0, 'AFU _OTSTUPNIK')
                        # end_from_hex_0 = "53 68 6F 6F 74 69 6E 67 20 73 66 78"  # Shooting sfx
                        # end_from_int_0 = get_address_from_binary(f, i_file, end_from_hex_0, 'Shooting sfx')
                        allowed_ranges = [
                            {
                                "begin_int": start_from_int_0,  # 131796768/0x07db0f20
                                # "end_int": end_from_int_0  # 131811120/0x07db4730   # Not used anymore
                                "end_int": -1
                            },
                            # {
                            #     "begin_int":  start_from_int_1,  # 131424672/0x07d561a0
                            #     "end_int": end_from_int_1  # 132384996/0x07e408e4
                            # }
                        ]
                    else:
                        i_min_size = i_min_size_saved
                        # All 'levelNN' files
                        start_from_hex_0 = "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 80 3F 00 00 80 3F 00 00 80 3F"  # ....Ç?..Ç?..Ç?..Ç?
                        start_from_int_0 = get_address_from_binary(f, i_file, start_from_hex_0, '....Ç?..Ç?..Ç?..Ç?')
                        allowed_ranges = [
                            {
                                "begin_int": start_from_int_0,  # 0
                                "end_int": -1  # To the EOF
                            }
                        ]

                    # # BEGIN Not used anymore
                    # with open(i_file, 'rb') as f:
                    #     data_offset = f.read().find(bytes.fromhex(start_from_hex_0))
                    #     if data_offset < 0:
                    #         continue
                    # data_offset_hex = "0x{:x}".format(data_offset)
                    # data_offset_int = int(data_offset_hex, 16)
                    # # data_offset_int = 0

                    # # print(f"data_offset_hex={data_offset_hex}")
                    # # print(f"data_offset_int={data_offset_int}")
                    # # input(" Press Enter to continue...")
                    # # sys.exit(0)
                    # # END Not used anymore
                
                # If start address for searching in file is a valid address (not negative one)
                if start_from_int_0 >= 0:

                    with open(i_file, 'rb') as f:
                        f.seek(start_from_int_0)
                        b = f.read()
                        json_write_to = []
                        
                        for s in ascii_strings(b, n=i_min_size, start_from=start_from_int_0):
                            
                            break_requested = False
                            # Check if we are in allowed range
                            for range in allowed_ranges:
                                if range['begin_int'] < 0:
                                    break_requested = True
                                # Break if string address not in allowed range
                                if range['begin_int'] >= 0 and s.offset < range['begin_int']:
                                    break_requested = True
                                if range['end_int'] >= 0 and s.offset > range['end_int']:
                                    break_requested = True
                            if break_requested:
                                break

                            if 'resources.assets' in i_file:
                                if not dialog_quest_only(s.s):
                                    continue

                            if not dialog_exclude_lang(s.s, lang='de'):
                                max_length = len(s.s)
                                dialog_tr = dialog_translate(src=translator, dialog=s.s, to=i_lang)
                                dialog_str = dialog_filter(dialog=dialog_tr, lang=i_lang, target_length=max_length)
                                if dialog_str:
                                    translated_size = len(dialog_str)
                                    oversize = 'False'
                                    if translated_size > max_length:
                                        oversize = 'True'
                                    # dialog maximum length is source length
                                    dialog_str = dialog_str[:max_length]
                                    # Fill dialog with whitespaces to match source length
                                    dialog_str = dialog_str.ljust(max_length)
                                    # Remove any unicode character
                                    dialog_str = dialog_str.encode('ascii', 'ignore').decode()
                                    # Calculate new size
                                    new_size = len(dialog_str)
                                    # Print result CSV
                                    sep = ';'
                                    # print(" {:s}{:1s}ASCII{:1s}0x{:x}{:1s}True{:1s}{:d}{:1s}{:d}{:1s}{:d}{:1s}{:s}{:1s}{:s}".format(i_file, sep, sep, s.offset, sep, sep, max_length, sep, translated_size, sep, new_size, sep, oversize, sep, dialog_str))
                                    # print(" {:s}{:1s}ASCII{:1s}0x{:x}{:1s}{:s}".format(i_file, sep, sep, s.offset, sep, s.s))
                                    # Set 'json_write_to' dict
                                    address_hex = "0x{:x}".format(s.offset)
                                    address_int = int(address_hex, 16)
                                    json_write_to.append(
                                        dict(
                                            address_int=address_int,
                                            address_hex=address_hex,
                                            text=s.s,
                                            text_size=max_length,
                                            translation=dialog_str,
                                            translation_size=new_size                                     
                                        )
                                    )    
                    
                    # Print results
                    # print(' ### BEGIN JSON ###')
                    # print(json.dumps(json_write_to, indent=4))
                    # print(' ### END JSON ###')

                    # Error: bytes must be in range(0, 256) --> unicode somewhere in element['translation']
                    # Backup i_file

                    # Copy original file in relative translate dir
                    shutil.copyfile(i_file, i_file_translated)

                    # Translate file in relative translate dir
                    with open(i_file_translated, 'rb+') as f:
                        for element in json_write_to:
                            # Convert ASCII string to binary representation
                            binary_string = b''
                            for ascii_char in element['translation']:
                                binary_string += bytes([ord(ascii_char)])
                            f.seek(element['address_int'])
                            f.write(binary_string)

                    # print(f" • {bcolors.OK}[Translate from 'en' to '{i_lang}'] {i_file} OK{bcolors.ENDC}")

            # print
            # print(f" • {bcolors.OK}[Translate from 'en' to '{i_lang}'] OK{bcolors.ENDC}")

            # END Translate to i_lang

            # All is OK!
            print(f" • {bcolors.OK}[Translate from 'en' to '{i_lang}'] OK{bcolors.ENDC}\n")

            # Copy translated files to default data dir
            print(f" • {bcolors.WARN}[Copy translated files from '{TRANSLATE_DIR_PATH}' to '{DEFAULT_ZONA_DATA_DIR}'] ...{bcolors.ENDC}\n")
            restore_files(src=TRANSLATE_DIR_PATH)
            print(f" • {bcolors.OK}[Copy translated files from '{TRANSLATE_DIR_PATH}' to '{DEFAULT_ZONA_DATA_DIR}'] OK{bcolors.ENDC}\n")

            print(f"{bcolors.OK}")
            print(f" To activate translation:")
            print(f"    1. Launch 'Z.O.N.A Origin' game from Steam as usual.")
            print(f"    2. Be sure to select 'English' language in 'Z.O.N.A Origin' game's settings.\n")
            print(f"{bcolors.ENDC}")

    except Exception as e:
        print(f" {bcolors.FAIL}Error: {e}{bcolors.ENDC}")

    finally:
        input(" Press Enter to exit...")

if __name__ == '__main__':
    main()
