from system import System
from versionManager import VersionManager

# Import the classes from 'rich' library
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

import time # Required to let the menu be more readable

initial_prompt = """
*  Version: 1.1.3

* Source Code: [https://github.com/Forzooo/GitHub-Checker](https://github.com/Forzooo/GitHub-Checker)

*  Made by: Forzo
"""

text = Markdown(initial_prompt) # Convert the text to print it with the Markdown style

# Create a styled panel
panel = Panel(text, title="GitHub Checker", border_style="blue", )

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

if __name__ == "__main__":    

    versionManager = VersionManager()

    console = Console() # Create the console
    # Print the initial prompt panel
    console.print(panel)

    while True:

        console.print("\n[b]Functions available:[/b]\n")

        # Print all the options available
        for i, option in enumerate(options):
            console.print(f"[cyan]({i})[/cyan] {option}")

        option = console.input("\n[b]Option:[/b] ")

        # Check which option the user has chosen
        match option:

            case "0":
                break

            case "1":
                url = input("Enter a GitHub repository link: ")
                version = input("Version you are using (type 'latest' (without quotes) to set to the last one available): ")

                versionManager.setUrl(url)
                versionManager.addRepository(version=version)

            case "2":

                url = input("Url of the repository: ")
                versionManager.setUrl(url)
                versionManager.removeRepository()

            case "3":
                versionManager.viewRepositories()

            case "4":
                check_repository_flag = versionManager.checkRepositories()

                if check_repository_flag:
                    print("- All the repositories you have saved exists.")

            case "5":
                versionManager.checkNewVersions()

            case "6":
                url = input("Url of the repository: ")
                version = input("Version you are using (type 'latest', without quotes, to set it to the last one available): ")
                versionManager.setUrl(url)

                versionManager.changeVersion(version=version)

            case "7":
                System.openDownloadFolder(System)

            case _:
                pass

        time.sleep(2) # Wait 2 seconds before the loop of the menu starts again
