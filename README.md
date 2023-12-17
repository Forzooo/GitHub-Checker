# GitHub-Checker
**About the tool**
This tool aims to automate the process of checking and installing new versions available in one or more repositories on GitHub.

It is written in Python, and is Open Source under the GPL-3.0 license.

**Compile the tool:**
1. Download the source code of the repository
2. Open a terminal
3. Go in the GitHub-Checker root directory
4. Write `pyinstaller ./source/main.py --onefile` (You have to install it with `pip install pyinstaller` if you don't already have it.)
5. Now check the `dist` folder. You will find the .exe in it.

**External Library Required:**
* `tqdm` used for the download progress bar
* `pyinstaller` used only if you want to compile the tool
