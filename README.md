# GitHub-Checker
**About the tool.** This tool aims to automate the process of checking and downloading new versions available of one or more repositories on GitHub.
It is written in Python 3.12 (which is required), and is Open Source under the GPL-3.0 license.

**About new releases.** The development phase of this tool has ended with version `1.0.11`. From now if new releases will be published, they will only contain bug fixes or minor improvements.

**How to compile the tool.**
1. Download the source code of the repository (You can either download it from the last release or from the repository itself)
2. Open a terminal
3. Go into GitHub-Checker root directory using `cd`
4. Install the libraries, required by the tool, using: `pip install -r requirements.txt`
5. If you don't already have pyinstaller install it with `pip install pyinstaller`
6. Compile the tool by using `pyinstaller ./source/main.py --onefile`
7. Now check the dist folder: you will find the executable in it.

**External Libraries Required.**
You can find the all the libraries required to compile the tool, with which version I used, in `requirements.txt`
