#!python
# -*- coding: utf-8 -*-
"""
Title : auto_ZO_translate.py
Description : Script for translating dialogues and quest titles of the Steam game 'Z.O.N.A Origin' by AGaming+.
Author: peurKe
Creation Date: 2024-10-27
Last Modified: 2024-10-31
Version: 1.1
License: MIT
"""

# https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe
# https://www.python.org/ftp/python/3.13.0/python-3.13.0.exe
# https://gist.github.com/williballenthin/8e3913358a7996eab9b96bd57fc59df2 (broken)
# https://gist.github.com/jedimasterbot/39ef35bc4324e4b4338a210298526cd0 (fixed)
# https://github.com/ssut/py-googletrans/issues/280
# https://medium.com/analytics-vidhya/removing-stop-words-with-nltk-library-in-python-f33f53556cc1

# pip install --upgrade pip
# pip install tqdm googletrans==3.1.0a0 legacy-cgi nltk unidecode pywin32 pyinstaller
# pip install tqdm
# pip install googletrans==3.1.0a0
# pip install legacy-cgi
# pip install nltk
# pip install unidecode
# pip install pywin32
# pip install pyinstaller

# Error: Time out --> Problem with google translator API = Relaunch script
# Error: _ssl.c:1003: The handshake operation timed out --> Problem with google translator API = Relaunch script
# Error: [Errno 11001] getaddrinfo failed --> Internet connection problem = Check Internet connection and relanch script
# Error: bytes must be in range(0, 256) --> There is unicode character somewhere in element['translation'] string

import argparse
import sys
from os import path as os_path, makedirs as os_makedirs, listdir as os_listdir, remove as os_remove, getcwd as os_getcwd
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
    # from nltk.corpus import stopwords
    from nltk import download as nltk_download
    from nltk.tokenize import word_tokenize
    from googletrans import Translator
    import win32com.client
except Exception as e:
    print(f" Error: {e}")
    input(f" Press Enter to exit...")
    sys.exit(-1)

class bcolors:
    OK = '\033[92m'
    INFO = '\033[93m'
    FAIL = '\033[91m'
    ASK = '\033[96m'
    ENDC = '\033[0m'
    NOTIF = '\033[42m'

DEFAULT_FILES = [
    'level0', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7',
    'level8', 'level9', 'level10', 'level11', 'level12', 'level13', 'level14', 'level15',
    'level16', 'level17', 'level18', 'level19', 'level20', 'level21', 'level22', 'level23',
    'level24', 'level25', 'level26', 'level27', 'level28', 'level29', 'resources.assets'
]

DEFAULT_ZONA_DIR_EXAMPLE = 'C:\\SteamLibrary\\steamapps\\common\\ZONAORIGIN'
DEFAULT_ZONA_DATA_DIR = './ZONAORIGIN_Data'
DEFAULT_ZONA_TRANSLATE_DIR = './auto_ZO_translate'
DEFAULT_ZONA_TRANSLATE_SUCCEED_FILE = 'done.txt'
DEFAULT_ZONA_BACKUP_DIR = './auto_ZO_translate/BACKUP'
DEFAULT_ZONA_EXE_FILENAME = 'ZONAORIGIN.exe'
DEFAULT_ZONA_GLOBAL_GM = 'globalgamemanagers'
DEFAULT_ZONA_TRANSLATE_RESTORE_SHORTCUT = 'auto_ZO_translate (restore).lnk'

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
CUSTOM_DE_STOPWORDS = ['aber', 'abzug', 'alle', 'allem', 'allen', 'aller', 'alles', 'als', 'ander', 'andere', 'anderem', 'anderen', 'anderer', 'anderes', 'anderm', 'andern', 'anders', 'angekommen', 'auch', 'auf', 'bei', 'benutzt', 'ber', 'berfalls', 'berleben', 'berraschungen', 'bewegungen', 'bist', 'bleibt', 'damit', 'dann', 'derselbe', 'derselben', 'denselben', 'desselben', 'demselben', 'dieselbe', 'dieselben', 'dass', 'dasselbe', 'dazu', 'dein', 'deine', 'deinem', 'deinen', 'deiner', 'deines', 'den', 'denn', 'der', 'derer', 'des', 'dessen', 'dich', 'diesem', 'diesen', 'dieser', 'doch', 'dormitory', 'durch', 'ein', 'eine', 'einem', 'einen', 'einer', 'eines', 'einheit', 'einig', 'einige', 'einigem', 'einigen', 'einiger', 'einiges', 'einmal', 'erinnert', 'ihm', 'etwas', 'euer', 'eure', 'eurem', 'euren', 'eurer', 'eures', 'fur', 'gesch', 'gegen', 'gewehr', 'gewesen', 'gibt', 'habe', 'haben', 'hallo', 'hatte', 'hatten', 'hauptquartier', 'hilft', 'hin', 'hinter', 'ich', 'im', 'kamera', 'kugelflug', 'mich', 'mir', 'ihr', 'ihm', 'ihn', 'ihnen', 'indem', 'infizierte', 'ist', 'jede', 'jedem', 'jeden', 'jeder', 'jedes', 'jener', 'jenem', 'jenen', 'jener', 'jenes', 'jetzt', 'kalorien', 'kann', 'kannst', 'kein', 'keine', 'keinem', 'keinen', 'keiner', 'keines', 'konnen', 'konnte', 'machen', 'manchem', 'manchen', 'mancher', 'manches', 'mein', 'meine', 'meinem', 'meinen', 'meiner', 'meines', 'monolithen', 'muss', 'musste', 'nach', 'nicht', 'nichts', 'nun', 'nur', 'nutzen', 'oder', 'ohne', 'patrone', 'patronem', 'perfekt', 'perfekte', 'risches', 'sehr', 'sein', 'seine', 'seinem', 'seinen', 'seiner', 'seines', 'selbst', 'sich', 'sie', 'siehst', 'sind', 'solche', 'solchem', 'solchen', 'solcher', 'solches', 'sollte', 'sondern', 'sonst', 'sowohl', 'uber', 'und', 'uns', 'unser', 'unsere', 'unserem', 'unseren', 'unseres', 'unter', 'verbrennen', 'viel', 'vom', 'vor', 'vorbereiten', 'wahrend', 'waren', 'warst', 'weg', 'welche', 'welchem', 'welchen', 'welcher', 'welches', 'welt', 'wenn', 'werde', 'werden', 'wie', 'wieder', 'wir', 'wird', 'wirst', 'wollen', 'wollte', 'wohnheim', 'wurde', 'wurden', 'zug', 'zum', 'zur', 'zwar', 'zwischen']

CUSTOM_TARGET_STOPWORDS = {
    "en": [
        ['the', 'to', 'and', 'a', 'in', 'it', 'is', 'I', 'that', 'this', 'had', 'on', 'for', 'were', 'was']
    ],
    "fr": [
        # Manually added: 'une', 'contre', 'mode'
        # Manually removed: 'pas'
        ['a', 'abord', 'alors', 'aucun', 'aucune', 'avec', 'avoir', 'car', 'ce', 'cela', 'ces', 'cette', 'contre', 'dans', 'de', 'des', 'du', 'en', 'et', 'il', 'ils', 'je', 'la', 'le', 'les', 'mais', 'me', 'mon', 'ne', 'ni', 'nous', 'on', 'ou', 'par', 'pour', 'que', 'qui', 'quoi', 'sa', 'si', 'son', 'sur', 'ta', 'te', 'toi', 'ton', 'un', 'une', 'vous', 'y', 'dans', 'pouvez', 'peut', 'serait', 'aura', 'doit', 'etre']
    ],
    "cs": [
        # Manually added: 'a', 'proti', 'rezim'
        # Manually removed: 'ne'
        ['a', 'ale', 'aniz', 'az', 'bude', 'by', 'byl', 'byla', 'bylo', 'byly', 'co', 'do', 'jak', 'jako', 'je', 'jedna', 'jeste', 'jeho', 'jejich', 'jsem', 'jsi', 'k', 'kdyz', 'ktera', 'ktere', 'ktery', 'ma', 'mam', 'mit', 'muze', 'my', 'na', 'nebo', 'nekdo', 'neni', 'o', 'od', 'ona', 'oni', 'po', 'pod', 'pokud', 'pro', 'proti', 'rezim', 'se', 'si', 'svuj', 'svoje', 'ta', 'tak', 'ten', 'to', 'tu', 'uz', 'vam', 'vas', 'vy', 'z', 'za', 'ze', 'musite', 'musi', 'bude']
    ],
    "it": [
        # Manually added: 'a', 'contro', 'modalita'
        # Manually removed: 'non'
        ['a', 'ad', 'al', 'alla', 'alle', 'altro', 'ancora', 'anche', 'aspetta', 'avere', 'che', 'come', 'con', 'contro', 'cosa', 'da', 'dai', 'dal', 'de', 'di', 'dove', 'e', 'fai', 'fara', 'gia', 'ha', 'hanno', 'il', 'in', 'io', 'la', 'le', 'lo', 'loro', 'ma', 'me', 'mi', 'mio', 'modalita', 'ne', 'noi', 'nostro', 'o', 'per', 'piu', 'quale', 'quando', 'che', 'chi', 'sono', 'su', 'tra', 'tu', 'un', 'una', 'voi', 'sarebbe', 'deve', 'puo']
    ],
    "es": [
        # Manually added: 'a', 'contra', 'modo'
        # Manually removed: 'no'
        ['a', 'al', 'ante', 'bajo', 'como', 'con', 'contra', 'cuanto', 'de', 'del', 'desde', 'donde', 'durante', 'el', 'ella', 'ellos', 'en', 'entre', 'es', 'esta', 'estoy', 'ha', 'hace', 'hay', 'lo', 'los', 'me', 'mi', 'mismo', 'modo', 'muy', 'nada', 'nos', 'nuestro', 'o', 'para', 'pero', 'por', 'que', 'quien', 'si', 'sin', 'sobre', 'su', 'sus', 'te', 'tu', 'un', 'una', 'y']
    ],
    "ro": [
        # Manually added: 'a', 'impotriva', 'tryb'
        # Manually removed: 'nu'
        ['a', 'acesta', 'aceste', 'adica', 'altceva', 'altul', 'am', 'an', 'as', 'atunci', 'ba', 'bai', 'bi', 'de', 'decat', 'din', 'dintre', 'este', 'eu', 'fara', 'fie', 'fiecare', 'fiecare', 'in', 'impotriva', 'la', 'ma', 'me', 'mi', 'mii', 'mod', 'o', 'pe', 'poate', 'propria', 'propriile', 'sau', 'se', 'si', 'sunt', 'tine', 'tu', 'un', 'una', 'vor', 'va']
    ],
    "pl": [
        # Manually added: 'a', 'impotriva', 'mod'
        # Manually removed: 'nu'
        ['a', 'ale', 'by', 'c', 'co', 'd', 'da', 'dla', 'do', 'i', 'jak', 'je', 'jeden', 'jedna', 'kiedy', 'ktory', 'moze', 'na', 'ni', 'o', 'od', 'ona', 'oni', 'po', 'pomiedzy', 'przeciwko', 'przed', 'przy', 'sa', 'si', 'tak', 'to', 'tryb', 'tu', 'w', 'wszystko', 'z', 'za']
    ]
}

RESTORE_SPECIFIC_WORDS = {
    'en':[
        { "from": " n't", "to": "n't" }
    ],
    'fr': [
        { "from": "origine vr", "to": "ORIGIN VR" },
        { "from": "harceleur", "to": "Stalker" },
        { "from": "traqueur", "to": "Stalker" },
        { "from": "couleur",   "to": "color" },
        { "from": "œ", "to": "oe" },
        { "from": "Tournees magazine", "to": "Balles dans chargeur" },
        { "from": "Vitesse vol balle", "to": "Vitesse des balles"}
    ],
    'cs': [
        { "from": "puvod vr", "to": "ORIGIN VR" },
        { "from": "tracker", "to": "Stalker" },
        { "from": "psi", "to": "psych" },
        { "from": "barva",   "to": "color" }
    ],
    "it": [
        { "from": "origine vr", "to": "ORIGIN VR" },
        { "from": "tracker", "to": "Stalker" },
        { "from": "colore",   "to": "color" }
    ],
    "es": [
        { "from": "origen vr", "to": "ORIGIN VR" },
        { "from": "acosador", "to": "Stalker" },
        { "from": "rastreador", "to": "stalker" }
    ],
    "ro": [
        { "from": "origine vr", "to": "ORIGIN VR" },
        { "from": "urmaritor", "to": "Stalker" },
        { "from": "tracker", "to": "Stalker" },
        { "from": "culoare",   "to": "color" }
    ],
    "pl": [
        { "from": "pochodzenie vr", "to": "ORIGIN VR" },
        { "from": "tracker", "to": "Stalker" },
        { "from": "kolor",   "to": "color" }
    ],
    'all': [
        # { "from": "< ", "to": "<" },
        # { "from": " >", "to": ">" },
        # { "from": " <", "to": "<" },
        # { "from": "> ", "to": ">" }, # </color>- | </color>:
        { "from": "  ", "to": " " },
        { "from": " # ", "to": "#" },
        { "from": " :", "to": ":" },
        { "from": " ,", "to": "," },
        { "from": " .", "to": "." },
        { "from": " !", "to": "!" },
        { "from": " ?", "to": "?" },
        { "from": " ’’ ", "to": " " },
        { "from": "’’", "to": "'" },
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


def ascii_strings_version(buf):
    # Search for version '0.0NN' pattern
    reg = rb"(0\.0[0-9][0-9])"
    ascii_re = re.compile(reg)
    for match in ascii_re.finditer(buf):
        ascii_string = match.group().decode("ascii")
        ascii_address = match.start()
        yield String(ascii_string, ascii_address)
        # Only the first one
        break


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
    # Replace special characters with one whitepace (can generate double whitespace)
    text = re.sub(r'[^a-zA-Z0-9\s\.,!?:]', ' ', text)
    # Remove double whitespaces
    text = text.replace('  ', ' ')
    return text


def replace_accents(text):
    # text = unicodedata.normalize('NFKD', text)
    # return "".join([c for c in text if not unicodedata.combining(c)])
    return unidecode(text)


def restore_translated_words(text, lang='en'):
    for restore_word in RESTORE_SPECIFIC_WORDS[lang]:
        # # Replace case sensitive
        # text = text.replace(restore_word['from'], restore_word['to'])
        # Replace case insensitive
        pattern = re.compile(re.escape(restore_word['from']), re.IGNORECASE)
        text = pattern.sub(restore_word['to'], text)
    return text


def dialog_filter(dialog, lang='en', target_length=0):
    # Preserve <color=#hhhhhh></color> tags
    if '<color' in dialog:
        if '</color>' in dialog:
            sep = '</color>'
            dialog_list = dialog.split(sep)
        else:
            # No </color> tag associated to existing <color=#hhhhhh> tag, so no translate is needed
            return dialog
    # No <color=#hhhhhh> and </color> tags found
    else:
        sep = ''
        dialog_list = ['', dialog]

    color = dialog_list[0]
    dialog = dialog_list[1]

    # Replace all accentuation characters
    dialog = replace_accents(dialog)

    # Remove all special characters
    dialog = remove_specials(dialog)

    #  This list will grow with successives stopwords list
    all_requested_stopwords = []

    # Remove stop words
    index_stopword = 0
    for requested_stopwords in CUSTOM_TARGET_STOPWORDS[lang]:
        # Split text to a list of words
        tokens = word_tokenize(dialog)
        # Get stopwords
        all_requested_stopwords.extend(requested_stopwords)
        # Filter stopwords
        dialog_filtered_list = [t for t in tokens if t.lower() not in all_requested_stopwords]
        # Recreate dialog
        dialog = ' '.join(dialog_filtered_list)
        # # DEBUG
        # print(f"[{index_stopword}][{len(dialog)}] {dialog}")
        index_stopword += 1
        # Current stopwords set is not enough, go to next stopwords set
        if len(dialog) <= target_length:
            break
    # Restore specific words in translated lang
    dialog = restore_translated_words(dialog, lang=lang)
    # Restore specific words for all langs
    dialog = restore_translated_words(dialog, lang='all')
    return f"{color}{sep}{dialog}"


def dialog_translate(src, dialog, to='fr'):
    # Preserve <color=#hhhhhh></color> tags
    if '<color' in dialog:
        if '</color>' in dialog:
            sep = '</color>'
            dialog_list = dialog.split(sep)
        else:
            # No </color> tag associated to existing <color=#hhhhhh> tag, so no translate is needed
            return dialog
    # No <color=#hhhhhh> and </color> tags found
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


def get_address_from_binary(file_desc, file, search_hex, label):
    file_desc.seek(0)
    try:
        offset_int = file_desc.read().find(bytes.fromhex(search_hex))
    except:
        printc(f" Error: {e} during search for '{label}' in '{file}' binary file\n", bcolors.FAIL)
        sys.exit(-1)
    return offset_int


def backup_files(version):
    backup_dir = f"{DEFAULT_ZONA_BACKUP_DIR}_{version}"
    printc(f" • [Create backup in '{backup_dir}/' directory] ...\n", bcolors.INFO)
    os_makedirs(backup_dir)
    # All 'levelNN' original files
    files_to_copy = [os_path.join(DEFAULT_ZONA_DATA_DIR, f) for f in os_listdir(DEFAULT_ZONA_DATA_DIR) if f.startswith('level') and not f.endswith('.resS')]
    # Unique 'resources.assets' original file
    files_to_copy.append(f"{DEFAULT_ZONA_DATA_DIR}/resources.assets")
    # Copy all original files in backup directory
    for file in files_to_copy:
        backup_file = os_path.join(backup_dir, os_path.basename(file))
        shutil.copy2(file, backup_file)
    printc(f" • [Create backup in '{backup_dir}/' directory] OK\n", bcolors.OK)


def restore_files(version=None, src=DEFAULT_ZONA_BACKUP_DIR):
    if version:
        src = f"{DEFAULT_ZONA_BACKUP_DIR}_{version}"

    printc(f" • [Restore files from '{src}/' directory to '{DEFAULT_ZONA_DATA_DIR}/'] ...\n", bcolors.INFO)
    if not os_path.exists(src):
        printc(f" • [Restore files from '{src}/' directory impossible because directory does not exist] Failed\n", bcolors.FAIL)
        if src == DEFAULT_ZONA_BACKUP_DIR:
            printc(f" Tip: Use the Steam 'Check integrity of game files' button located in 'Installed files' tab in the Z.O.N.A Origin's game properties.\n", bcolors.INFO)
        inputc(f" Press Enter to exit...\n", bcolors.ASK)
        sys.exit(-1)

    # All backup files
    files_to_copy = [os_path.join(src, f) for f in os_listdir(src)]
    files_count = len(files_to_copy)
    if not files_count:
        printc(f" Error: There is {files_count} file to restore from '{src}/' directory.\n", bcolors.FAIL)
        inputc(f" Press Enter to exit...\n", bcolors.ENDC)
        sys.exit(-1)
    # Copy all backup files in data directory
    for file in files_to_copy:
        data_file = os_path.join(DEFAULT_ZONA_DATA_DIR, os_path.basename(file))
        shutil.copy2(file, data_file)
    printc(f" • [Restore {files_count} files from '{src}/' directory to '{DEFAULT_ZONA_DATA_DIR}/'] OK\n", bcolors.OK)


def check_all_in_langs(text):
    if 'all' in text:
        text = ['fr', 'cs', 'it', 'es', 'ro', 'pl']
    return text


def translate_ended_message():
    print(f" To play with this translation:")
    print(f"    1. Just launch 'Z.O.N.A Origin' game from Steam as usual.")
    print(f"    2. Be sure to select 'English' language in 'Z.O.N.A Origin' game's settings.\n")
    printc(f"                                                                                                         ", bcolors.NOTIF)
    printc(f"    /!\\ Over the next few days:                                                                          ", bcolors.NOTIF)
    printc(f"        If 'Z.O.N.A Origin' no longer launches correctly or if a new update has been made by AGaming+    ", bcolors.NOTIF)
    printc(f"        You will need to run this script again to update the translation.                                ", bcolors.NOTIF)
    printc(f"                                                                                                         ", bcolors.NOTIF)
    print()


def create_restore_shortcut():
    # Get current script name
    script_name = os_path.basename(__file__)
    # Get current working directory
    current_dir = os_getcwd()
    # Define the executable path and shortcut properties
    exe_path = f"{current_dir}\\{script_name}"
    exe_args = '-r'
    shortcut_name = "auto_ZO_translate (restore).lnk"
    shortcut_target = exe_path
    # Create a WScript.Shell object
    shell = win32com.client.Dispatch('WScript.Shell')
    # Create a shortcut object
    shortcut = shell.CreateShortCut(shortcut_name)
    # Set the shortcut properties
    shortcut.TargetPath = shortcut_target
    shortcut.WorkingDirectory = os_path.dirname(shortcut_target)
    shortcut.Arguments = exe_args
    # Save the shortcut
    shortcut.save()
    return shortcut_name


def printc(msg, c=None):
    if not c:
        print(msg)
    else:
        print(f"{c}{msg}{bcolors.ENDC}")


def inputc(prompt, c=None):
    if not c:
        res = input(prompt)
    else:
        res = input(f"{c}{prompt}{bcolors.ENDC}")
    return res


def main():

    try:
        # Check current working directory is valid
        if not os_path.exists(DEFAULT_ZONA_EXE_FILENAME):
            printc(f" Error: Move this script in the same directory as the 'ZONAORIGIN.exe' executable file (usually in the '{DEFAULT_ZONA_DIR_EXAMPLE}' directory).\n", bcolors.FAIL)
            printc(f" Then run this moved script again.", bcolors.FAIL)
            sys.exit(-1)

        # Create a restore shortcut in the current directory if not existing
        if not os_path.exists(DEFAULT_ZONA_TRANSLATE_RESTORE_SHORTCUT):
            printc(f" • [Create a restore shortcut in the current directory] ...\n", bcolors.INFO)
            shortcut = create_restore_shortcut()
            printc(f" • [Create '{shortcut}' restore shortcut in the current directory] OK\n", bcolors.OK)

        # Get script arguments
        argparser = argparse.ArgumentParser()
        argparser.add_argument("-l", "--langs", type=str, default='empty', choices=['empty', 'all', 'fr', 'cs', 'it', 'es', 'ro', 'pl'], help="Languages to translate to. if more than one language then '--langs' parameter must be comma separated (eg. 'fr,cs')")
        argparser.add_argument("-f", "--files", type=str, default='empty', help="Comma separated str. Default is with all 'levelNN' and 'resources.assets' files. if '--file' is specified then '--files' parameter must be comma separated (eg. 'level7,level11')")
        argparser.add_argument("-s", "--min-size", type=int, default=18, help="Minimum size for string to translate is set to 18 (to avoid <color></color> tags)")
        argparser.add_argument("-r", "--restore", action='store_true', help="Restore backup files (reset)")
        argparser.add_argument("-rv", "--restore-version", type=str, default=None, help="Specify the '0.0NN' patch version to restore. Default will be the current version. (reset)")
        argparser.add_argument("--force", action='store_true', help=f"Force translate even if translated files are already existing in '{DEFAULT_ZONA_TRANSLATE_DIR}/' directory")
        
        args = argparser.parse_args()

        i_langs = args.langs.split(',')
        i_langs = check_all_in_langs(i_langs)
        i_force = args.force
        i_files = args.files.split(',')
        i_min_size = args.min_size
        i_restore = args.restore
        i_restore_version = args.restore_version

        i_file_ggm = f"{DEFAULT_ZONA_DATA_DIR}/{DEFAULT_ZONA_GLOBAL_GM}"
        current_version_patch = None
        with open(i_file_ggm, 'rb') as f:
            f.seek(0)
            b = f.read()
            # Search for first '0.0NN' version pattern
            for version in ascii_strings_version(b):
                current_version_patch = version.s

        if current_version_patch is None:
            printc(f" No '0.0NN' version patch found in '{i_file_ggm}' binary file.\n", bcolors.FAIL)
            inputc(f" Press Enter to exit...\n", bcolors.ASK)
            sys.exit(1)

        # RESTORE: Create backup file in backup directory if not already existing
        if i_restore:
            print(f" /// RESTORATION:\n")
            if i_restore_version:
                restore_version = i_restore_version
            else:
                restore_version = current_version_patch
            restore_dir = f"{DEFAULT_ZONA_BACKUP_DIR}_{restore_version}"
            if os_path.exists(restore_dir):
                restore = ''
                while restore not in ['y', 'n']:
                    restore = str(inputc(f" Confirm you want to restore all '{restore_version}' backup binary files (y/n):", bcolors.ASK)).lower().strip()
                if restore == 'y':
                    restore_files(current_version_patch)
            else:
                printc(f" • [Restore all binary files impossible because there is no backup for '{restore_version}' version] Failed\n", bcolors.FAIL)
                printc(f" Tip: Use the Steam 'Check integrity of game files' button located in 'Installed files' tab in the Z.O.N.A Origin's game properties to restore original binary files.\n", bcolors.INFO)
                inputc(f" Press Enter to exit...\n", bcolors.ASK)
                sys.exit(1)

        # TRANSLATE
        else:
            print(" /// PREREQUISITES:\n")
            printc("    • Your 'Z.O.N.A Origin' game must be up to date.", bcolors.INFO)
            printc("    • Your PC has an Internet connection for Google Translator API requests.\n", bcolors.INFO)
            printc(" Press Ctrl+C to exit if you need to update 'Z.O.N.A Origin' game before translate...", bcolors.ASK)
            inputc(" Press Enter to translate 'Z.O.N.A Origin' game...", bcolors.ASK)

            # BEGIN GUI execution
            if i_langs == ['empty']:
                i_langs = ''
                print()
                while i_langs not in ['fr', 'cs', 'it', 'es', 'ro', 'pl']:
                    i_langs = str(inputc(f" Language to translate to (fr|cs|it|es|ro|pl): ", bcolors.ASK)).lower().strip()
                i_langs = i_langs.split(',')
                i_langs = check_all_in_langs(i_langs)
            # END GUI execution
        
            # Save 'i_min_size' for 'resources.assets'
            i_min_size_saved = i_min_size

            # Default 'i_files'
            if i_files == ['empty']:
                i_files = DEFAULT_FILES

            print()
            print(f" /// PARAMETERS:\n")
            printc(f"    • Translate from .................... : 'en'", bcolors.INFO)
            printc(f"    • Translate to ...................... : '{i_langs}'", bcolors.INFO)
            printc(f"    • Minimum size string to translate .. : {i_min_size}", bcolors.INFO)
            printc(f"    • Binary files to translate ......... : {i_files}\n", bcolors.INFO)

            # Download nltk 'stopwords' and 'punkt_tab'
            # nltk_download('stopwords')
            # Download nltk 'punkt' and 'punkt_tab'
            # nltk_download('punkt')
            # nltk_download('punkt_tab')
            # stops = set(stopwords.words('german'))
            # stops = set(stopwords.words('french'))
            # stops = set(stopwords.words('czech'))
            # print(stops)
            # inputc(f" Press Enter to continue...", bcolors.ASK)
            # sys.exit(0)
            
            print(f" /// TRANSLATION:\n")
            # Initialize Google Translator
            translator = Translator()

            # Create backup file in backup directory if not already existing
            # Initialize flag for backup files so that they are not restored when the backup has just been performed
            backup_files_done = False
            backup_dir = f"{DEFAULT_ZONA_BACKUP_DIR}_{current_version_patch}"
            if os_path.exists(backup_dir):
                printc(f" • [Backup in '{backup_dir}/' directory already exists] OK\n", bcolors.OK)
            else:
                backup_files(current_version_patch)
                # Set flag for backup files
                backup_files_done = True
            
            # Initialiaze variable for lang for progression
            i_langs_count = len(i_langs)
            i_langs_index = 0
            
            # for i_file in i_files:
            for i_lang in i_langs:

                # Check already existing and create relative translate dir for lang file destination
                TRANSLATE_DIR_PATH = f"{DEFAULT_ZONA_TRANSLATE_DIR}/{i_lang}_{current_version_patch}"
                # Initialiaze success file flag path
                TRANSLATE_SUCCEED_FILE = f"{TRANSLATE_DIR_PATH}/{DEFAULT_ZONA_TRANSLATE_SUCCEED_FILE}"
                # Does translate dir for lang file destination does not exists?
                if not os_path.exists(TRANSLATE_DIR_PATH):
                    os_makedirs(TRANSLATE_DIR_PATH)
                else:
                    printc(f" • [Translated files for '{i_lang}' and '{current_version_patch}' version already exists in '{TRANSLATE_DIR_PATH}/' directory] OK\n", bcolors.OK)
                    # Check success file flag exists in translate lang directory
                    if os_path.exists(TRANSLATE_SUCCEED_FILE):
                        printc(f" • [Translated directory contains a valid '{TRANSLATE_SUCCEED_FILE}' succeed flag file] OK\n", bcolors.OK)
                        # Translate dir for lang file destination does exists ('--force' parameter is not requested)
                        if not i_force:
                            printc(f" • [Force translate IS NOT requested]\n", bcolors.ASK)
                            # Copy existing translate dir for lang file
                            printc(f" • [Copy translated files from '{TRANSLATE_DIR_PATH}/' to '{DEFAULT_ZONA_DATA_DIR}/'] ...\n", bcolors.INFO)
                            restore_files(src=TRANSLATE_DIR_PATH)
                            printc(f" • [Copy translated files from '{TRANSLATE_DIR_PATH}/' to '{DEFAULT_ZONA_DATA_DIR}/'] OK\n", bcolors.OK)
                            translate_ended_message()
                            inputc(f" Press Enter to exit...\n", bcolors.ASK)
                            sys.exit(0)
                        # Translate dir for lang file destination does exists ('--force' parameter is requested)
                        else:
                            printc(f" • [Translated files for '{i_lang}' and '{current_version_patch}' version already exists in '{TRANSLATE_DIR_PATH}/' directory] OK\n", bcolors.OK)
                            printc(f" • [Translated directory does contain a valid '{TRANSLATE_SUCCEED_FILE}' succeed flag file] OK\n", bcolors.OK)
                            printc(f" • [But force translate IS requested] OK\n", bcolors.OK)
                            printc(f" • [Remove valid '{TRANSLATE_SUCCEED_FILE}' succeed flag file] ...\n", bcolors.INFO)
                            os_remove(TRANSLATE_SUCCEED_FILE)
                            printc(f" • [Remove valid '{TRANSLATE_SUCCEED_FILE}' succeed flag file] OK\n", bcolors.OK)
                    else:
                        printc(f" • [Translated directory does not contain a valid '{TRANSLATE_SUCCEED_FILE}' succeed flag file] OK\n", bcolors.OK)
                        printc(f" • [Force translate will be performed]\n", bcolors.ASK)

                # Increment lang index for progression
                i_langs_index = i_langs_index + 1

                # Do not restore when the backup has just been performed
                if not backup_files_done:
                    # Restore original backup files in data dir before translate
                    printc(f" • [Restore original backup files from '{DEFAULT_ZONA_BACKUP_DIR}/' to '{DEFAULT_ZONA_DATA_DIR}/'] ...\n", bcolors.INFO)
                    restore_files(current_version_patch)
                    printc(f" • [Restore original backup files from '{DEFAULT_ZONA_BACKUP_DIR}/' to '{DEFAULT_ZONA_DATA_DIR}/'] OK\n", bcolors.OK)

                # BEGIN Translate to i_lang
                printc(f" • [Translate from 'en' to '{i_lang}' ({i_langs_index}/{i_langs_count})] ...\n", bcolors.INFO)
                
                # print
                # print(f" • [Translate from 'en' to '{i_lang}'] ...\n")

                # for i_file in i_files:
                for i_file in tqdm(i_files):

                    i_file_translated = f"{TRANSLATE_DIR_PATH}/{i_file}"
                    i_file = f"{DEFAULT_ZONA_DATA_DIR}/{i_file}"
                
                    # print(f" • [Translate from 'en' to '{i_lang}'] {i_file} ...\n")

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
                                        # # BEGIN To be uncommented if DEBUG PRINT #1 is needed
                                        # translated_size = len(dialog_str)
                                        # oversize = 'False'
                                        # if translated_size > max_length:
                                        #     oversize = 'True'
                                        # # END To be uncommented if DEBUG PRINT #1 is needed
                                        # dialog maximum length is source length
                                        # if len(dialog_str) > max_length:
                                        #     dialog_str = dialog_str[:max_length]
                                        #     dialog_str = dialog_str[:-3] + '###'
                                        dialog_str = dialog_str[:max_length]
                                        # Fill dialog with whitespaces to match source length
                                        dialog_str = dialog_str.ljust(max_length)
                                        # Remove any unicode character
                                        dialog_str = dialog_str.encode('ascii', 'ignore').decode()
                                        # Calculate new size
                                        new_size = len(dialog_str)
                                        # # BEGIN DEBUG PRINTS
                                        sep = ';'
                                        # # DEBUG PRINT #1
                                        # print(" {:s}{:1s}ASCII{:1s}0x{:x}{:1s}True{:1s}{:d}{:1s}{:d}{:1s}{:d}{:1s}{:s}{:1s}{:s}".format(i_file, sep, sep, s.offset, sep, sep, max_length, sep, translated_size, sep, new_size, sep, oversize, sep, dialog_str))
                                        # # DEBUG PRINT #2
                                        # print(" {:s}{:1s}ASCII{:1s}0x{:x}{:1s}{:s}".format(i_file, sep, sep, s.offset, sep, s.s))
                                        # # DEBUG PRINT #3
                                        # print(" {:s}{:1s}ASCII{:1s}0x{:x}{:1s}{:s}".format(i_file, sep, sep, s.offset, sep, dialog_str))
                                        # # DEBUG PRINT #4
                                        # print(" <{:d}> {:s}".format(max_length, dialog_str))
                                        # BEGIN DEBUG PRINTS
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

                        # # printc(f" • [Translate from 'en' to '{i_lang}'] {i_file} OK\n", bcolors.OK)

                # Create success file flag in translate lang directory
                with open(TRANSLATE_SUCCEED_FILE, "w") as f:
                    pass

                # print
                # printc(f" • [Translate from 'en' to '{i_lang}'] OK\n", bcolors.OK)

                # END Translate to i_lang

                # All is OK!
                printc(f" • [Translate from 'en' to '{i_lang}' ({i_langs_index}/{i_langs_count})] OK\n", bcolors.OK)

                # Copy translated files to default data dir
                printc(f" • [Copy translated files from '{TRANSLATE_DIR_PATH}/' to '{DEFAULT_ZONA_DATA_DIR}/'] ...\n", bcolors.INFO)
                restore_files(src=TRANSLATE_DIR_PATH)
                printc(f" • [Copy translated files from '{TRANSLATE_DIR_PATH}/' to '{DEFAULT_ZONA_DATA_DIR}/'] OK\n", bcolors.OK)

            translate_ended_message()

    except Exception as e:
        printc(f" Error: {e}\n", bcolors.FAIL)

    finally:
        inputc(f" Press Enter to exit...", bcolors.ASK)

if __name__ == '__main__':
    main()
