# GitHub-Checker
**About the tool:** This tool aims to automate the process of checking and installing new versions available in one or more repositories on GitHub.
It is written in Python 3.12 (which is required), and is Open Source under the GPL-3.0 license.

**About new releases:** The development phase of this tool has ended with `v1.0.11`. From now if new releases will be published they will only contain bug fixes or minor improvements.

**Compile the tool:**
1. Download the source code of the repository
2. Open a terminal
3. Go in the GitHub-Checker root directory
4. Write `pyinstaller ./source/main.py --onefile` (You have to install it with `pip install pyinstaller` if you don't already have it.)
5. Now check the `dist` folder. You will find the .exe in it.

**External Library Required:**
* `rich` used to improve the graphics of the terminal
* `pyinstaller` used only if you want to compile the tool (optional)

(Note. From version `1.0.13` `tqdm` is no longer required)

You can find the libraries required, with which version I used, in `requirements.txt`