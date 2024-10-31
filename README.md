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


## Usage from binary release

• Download the latest binary release:

  https://github.com/peurKe/auto_ZO_translate/releases  

• Move the 'auto_ZO_translate.exe' and 'auto_ZO_translate (restore).exe' files in the same directory as the 'ZONAORIGIN.exe' executable file (usually in the 'C:\Program Files (x86)\Steam\steamapps\common\ZONAORIGIN\' directory).

• Go to the 'C:\Program Files (x86)\Steam\steamapps\common\ZONAORIGIN\'

• Execute 'auto_ZO_translate.exe'

  Press Enter if prerequisites displayed on the screen are correct ('Z.O.N.A Origin' game is up to date + Script can connect to the Internet from your PC for Google Translator API requests).

  Select the language you want to translate English to (Possible choices are: fr, it, es, cd, pl, ro)
  
• To restore original translation, execute the 'auto_ZO_translate (restore).exe' shortchut :

  Then confirm you want to restore original translation (y/n)


## Usage from sources

• Download the latest Python package:
    
  "64-bit" for Windows (https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe).
        
  "32-bit" for Windows (https://www.python.org/ftp/python/3.13.0/python-3.13.0.exe).
        
• Run the installer and follow the prompts to install Python.

• Open python installed console and install all following additional packages:

    pip install tqdm googletrans==3.1.0a0 legacy-cgi nltk unidecode

• Move the 'auto_ZO_translate.py' script in the same directory as the 'ZONAORIGIN.exe' executable file (usually in the 'C:\Program Files (x86)\Steam\steamapps\common\ZONAORIGIN\' directory).

• Go to the 'C:\Program Files (x86)\Steam\steamapps\common\ZONAORIGIN\'

• Double clic on 'auto_ZO_translate.py' to execute script

  Press Enter if prerequisites displayed on the screen are correct ('Z.O.N.A Origin' game is up to date + Script can connect to the Internet from your PC for Google Translator API requests).

  Select the language you want to translate English to (Possible choices are: fr, it, es, cd, pl, ro)
  
• To restore original translation, execute the script with following argument:
  
    ./auto_ZO_translate.py -r

  Then confirm you want to restore original translation (y/n)
  
