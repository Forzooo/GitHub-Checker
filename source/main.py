from system import addLink, createJSON, removeRepository, viewRepository, openDownloadFolder
from versionManager import checkNewVersions, changeVersion

createJSON()

# Import the classes from 'rich' library
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console() # Create the console

text = """
*  Version: 1.0.13

* Source Code: [https://github.com/Forzooo/GitHub-Checker](https://github.com/Forzooo/GitHub-Checker)

*  Made by: Forzo
"""

text = Markdown(text) # Convert the text to print it with the Markdown style

# Create a styled panel
panel = Panel(text, title="GitHub Checker", border_style="blue", )

# Print the styled panel
console.print(panel)



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

    console.print("\n[b]Functions available:[/b]\n")

    for i, option in enumerate(options):
        console.print(f"[cyan]({i})[/cyan] {option}")

    option = console.input("\n[b]Option:[/b] ")


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

