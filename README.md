# auto_ZO_translate

Script for translating dialogues and quest titles of the Steam game 'Z.O.N.A Origin' by AGaming+.

## Prerequisites

  • Your 'Z.O.N.A Origin' game must be up to date.
  
  • You must authorise this script in your firewall (API requests toward Online Google translator are required).

## Currently supported languages

  • **fr** = French
  
  • **it** = Italian (Not tested as I don't speak this language)
  
  • **es** = Spanish (Not tested as I don't speak this language)
  
  • **cs** = Czech (Not tested as I don't speak this language)
  
  • **pl** = Polish (Not tested as I don't speak this language)
  
  • **ro** = Romanian (Not tested as I don't speak this language)

## Installation from sources

On Windows 10/11:

  • Install python:
  
    Download the latest Python package:
    
        “64-bit” for Windows (https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe).
        
        “32-bit” for Windows (https://www.python.org/ftp/python/3.13.0/python-3.13.0.exe).
        
    Run the installer and follow the prompts to install Python.
    
  • Open python installed console and install all following additional packages:
  
        pip install tqdm googletrans==3.1.0a0 legacy-cgi nltk unidecode

  • Move the 'auto_ZO_translate.py' script in the same directory as the 'ZONAORIGIN.exe' executable file (usually in the 'C:\Program Files (x86)\Steam\steamapps\common\ZONAORIGIN\' directory).

  • Go to the 'C:\Program Files (x86)\Steam\steamapps\common\ZONAORIGIN\'

  • Double-Clic on 'auto_ZO_translate.py'

  • Press enter if prerequisites are OK

  • Select the language you want to translate English to (Possible choices are: fr, it, es, cd, pl, ro)
  
  • To restore original translation, execute the script with following argument:
  
        ./auto_ZO_translate.py -r
