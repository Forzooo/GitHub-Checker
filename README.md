# GitHub-Checker
**About the tool.** This tool aims to automate the process of checking and downloading new versions available of one or more repositories on GitHub.
It is written in Python 3.12 (which is required), and is Open Source under the GPL-3.0 license.

**About new releases.** The development phase of this tool has ended with `v1.0.11`. From now if new releases will be published, they will only contain bug fixes or minor improvements.

**How to compile the tool.**
1. Download the source code of the repository (You can either download it from the last release or from the repository itself)
2. Open a terminal
3. Go in the GitHub-Checker root directory using `cd` 
4. Write `pyinstaller ./source/main.py --onefile` in the terminal (You have to install `pyinstaller` with `pip install pyinstaller` if you don't already have it.)
5. Now check the `dist` folder: you will find the .exe in it.

**External Libraries Required.**
You can find the all the libraries required to compile the tool, with which version I used, in `requirements.txt`
