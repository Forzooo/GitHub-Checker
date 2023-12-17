from system import addLink, createJSON, removeRepository, viewRepository, openDownloadFolder
from versionManager import checkNewVersions, changeVersion

createJSON()

print(
"""
╭──────────────────────────── GitHub Checker ────────────────────────────╮
│                                                                        │
│   ***  Version: 1.0.7  ***                                             │
│                                                                        │
│   *** Source Code: https://github.com/Forzooo/GitHub-Checker ***       │
│                                                                        │
│   ***  Made by: Forzo  ***                                             │
╰────────────────────────────────────────────────────────────────────────╯
"""
)

options = [
    "Exit from the tool",
    "Add a repository",
    "Remove a repository",
    "View all the repositories",
    "Verify new releases",
    "Change the version you are using of a repository",
    "Open the download folder",
]
while True:

    print("\nFunctions available: ")

    for i in range(len(options)):
        print(f"({i}) {options[i]}")

    option = input("\n\nOption: ")


    if option == "0":
        break

    elif option == "1":
        url = input("Enter a GitHub repository link: ")
        version = input("Version you are using (type 'latest' (without quotes) to set to the last one available): ")

        addLink(url=url, version=version)

    elif option == "2":

        url = input("Url of the repository: ")
        removeRepository(url=url)

    elif option == "3":
        viewRepository()

    elif option == "4":
        checkNewVersions()

    elif option == "5":
        url = input("Url of the repository: ")
        version = input("Version you are using (type 'latest' (without quotes) to set to the last one available): ")

        changeVersion(url=url, version=version)

    elif option == "6":
        openDownloadFolder()

