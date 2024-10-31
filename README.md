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

```
1. Press Enter if prerequisites displayed on the screen are correct:
      - Your 'Z.O.N.A Origin' game must be up to date
      - Your PC has an Internet connection for Google Translator API requests).

2. Select the language you want to translate English to (Possible choices are: fr, it, es, cd, pl, ro)
```

• To restore original translation, execute the shortcut 'auto_ZO_translate (restore)' created by the executable

```
Then confirm you want to restore original translation (y/n)
```


## Usage from sources

• Download the **3.12.7** version of Python for windows:

   # /!\ Do not download the latest version because of numba python package requirement (only versions >=3.9,<3.13 are supported):
   
   # Python for Windows "64-bit" 3.12.7   https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe
   
   # Python for Windows "32-bit" 3.12.7   https://www.python.org/ftp/python/3.12.7/python-3.12.7.exe
        
• Run the installer and follow the prompts to install Python.

• Open python installed console, upgrade pip package and install all following additional packages:

    pip install --upgrade pip
    pip install numba tqdm googletrans==3.1.0a0 legacy-cgi nltk unidecode pywin32 pyinstaller

• Move the 'auto_ZO_translate.py' script in the same directory as the 'ZONAORIGIN.exe' executable file (usually in the 'C:\Program Files (x86)\Steam\steamapps\common\ZONAORIGIN\' directory).

• Go to the 'C:\Program Files (x86)\Steam\steamapps\common\ZONAORIGIN\'

• Double clic on 'auto_ZO_translate.py' to execute script

```
1. Press Enter if prerequisites displayed on the screen are correct:
      - Your 'Z.O.N.A Origin' game must be up to date
      - Your PC has an Internet connection for Google Translator API requests).

2. Select the language you want to translate English to (Possible choices are: fr, it, es, cd, pl, ro)
```
  
• To restore original translation, execute the shortcut 'auto_ZO_translate (restore)' created by the script execution

```
Then confirm you want to restore original translation (y/n)
```  
