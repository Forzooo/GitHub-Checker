from system import addLink, createJSON, removeRepository, viewRepository, openDownloadFolder
from versionManager import checkNewVersions, changeVersion, checkRepositories

createJSON() # Create "sites.json" (it happens only if it does not exist already)

# Import the classes from 'rich' library
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console() # Create the console

text = """
*  Version: 1.0.14

* Source Code: [https://github.com/Forzooo/GitHub-Checker](https://github.com/Forzooo/GitHub-Checker)

*  Made by: Forzo
"""

text = Markdown(text) # Convert the text to print it with the Markdown style

# Create a styled panel
panel = Panel(text, title="GitHub Checker", border_style="blue", )

# Print the styled panel
console.print(panel)


# Define all the options available to the user
options = [
    "Exit from the tool",
    "Add a repository",
    "Remove a repository",
    "View all the repositories",
    "Check the status of the repositories",
    "Verify new releases",
    "Change the version you are using of a repository",
    "Open the download folder",
]
while True:

    # Print all the options
    console.print("\n[b]Functions available:[/b]\n")

    for i, option in enumerate(options):
        console.print(f"[cyan]({i})[/cyan] {option}")

    option = console.input("\n[b]Option:[/b] ")


    # Check which option the user has chosen
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
        checkRepositories()

    elif option == "5":
        checkNewVersions()

    elif option == "6":
        url = input("Url of the repository: ")
        version = input("Version you are using (type 'latest' (without quotes) to set to the last one available): ")

        changeVersion(url=url, version=version)

    elif option == "7":
        openDownloadFolder()

