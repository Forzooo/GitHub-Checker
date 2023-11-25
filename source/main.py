from system import formatLinktoAPI, addLink, createJSON, removeRepository
from versionManager import checkNewVersions, changeVersion

createJSON()

print(
f"""
****** GitHub Checker ******

  ***  Version: 1.0.0  ***

  *** Source Code: https://github.com/Forzooo/GitHub-Checker ***

  ***  Made by: Forzo  ***
****************************
"""
)

option = input("Functions available: \n(1) Add link \n(2) Verify new releases \n(3) Remove a repository \n(4) Change the version you are using of a repository\n\nOption: ")

if option == "1":
    url = input("Insert a GitHub repository link: ")

    url_formatted = formatLinktoAPI(url=url)

    addLink(url_formatted)

elif option == "2":
    checkNewVersions()

elif option == "3":

    url = input("Url of the repository: ")
    removeRepository(url=url)

elif option=="4":
    url = input("Url of the repository: ")
    version = input("Version you are using: ")

    changeVersion(url=url, version=version)

input("Press enter to exit from the tool...")