from system import formatLinktoAPI, addLink, createJSON, removeRepository, viewRepository
from versionManager import checkNewVersions, changeVersion

createJSON()

print(
f"""
****** GitHub Checker ******

  ***  Version: 1.0.3  ***

  *** Source Code: https://github.com/Forzooo/GitHub-Checker ***

  ***  Made by: Forzo  ***
****************************"""
)

while True:
    option = input("\nFunctions available: \n(0) Exit from the tool \n(1) Add a repository \n(2) Verify new releases \n(3) Remove a repository \n(4) Change the version you are using of a repository \n(5) View all the repository\n\nOption: ")

    if option == "0":
        break

    elif option == "1":
        url = input("Enter a GitHub repository link: ")

        url_formatted = formatLinktoAPI(url=url)

        addLink(url_formatted)

    elif option == "2":
        checkNewVersions()

    elif option == "3":

        url = input("Url of the repository: ")
        removeRepository(url=url)

    elif option== "4":
        url = input("Url of the repository: ")
        version = input("Version you are using: ")

        changeVersion(url=url, version=version)

    elif option == "5":
        viewRepository()
