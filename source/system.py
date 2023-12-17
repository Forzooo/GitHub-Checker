def verifyRepositoryExist(url: str) -> bool:
    import requests # Import the library required to verify if the repository exist

    try:

        response = requests.get(url)

    except requests.exceptions.MissingSchema:
        print(f"You have entered an invalid url: {url}")
        return False

    if response.status_code != 200:
        print("The repository does not exist.")
        return False

    return True

def formatLinktoAPI(url: str) -> str|None:
    
    # Remove all the slash from the url
    url_splitted = url.split("/")

    # Verify that the url is a GitHub url
    if url_splitted[2] != "github.com":
        print(f"The url given in input is: {url_splitted[2]} which is not github.com")
        return

    # Verify that the url of the repository is the one required in the README.md file
    if len(url_splitted) != 5:
        print("The url of the repository is not the in the format required by the script. \nRead the README.md for details.")
        return

    # Strings used to modify the url given in input by the user
    api = "https://api.github.com/repos/"
    releases = "/releases"

    # url_splitted[3] is the username of the repository owner, url_splitted[4] is the name of the repository
    url_formatted = api + url_splitted[3] + "/" + url_splitted[4] + releases

    return url_formatted

def formatLinkFromAPI(url: str) -> str:

    # Remove all the slash from the url
    url_splitted = url.split("/")


    # String used to modify the url given in input by the user
    github_link = "https://github.com/"

    # url_splitted[4] is the username of the repository owner, url_splitted[5] is the name of the repository
    url_formatted = github_link + url_splitted[4] + "/" + url_splitted[5]

    return url_formatted

def addLink(url: str, version: str) -> None:

    from versionManager import getLatestVersion

    if not verifyRepositoryExist(url):
        return

    url_formatted = formatLinktoAPI(url=url) # Convert the url to the one used from the tool: "https://api.github.com. ..."

    # Check if the user has written in the version input 'latest' to set the version of the repository to the last one available
    if version.lower() == "latest":
        version = getLatestVersion(url=url_formatted)[0] # Get the latest version available on GitHub

    data = readData()

    data["repositories"][url_formatted] = version # Add to the dictionary the url and the version of the repository 

    updateJSON(data=data) # Update the JSON file with the changes made

    print(f"Added the repository: {url_formatted}")

    return


def createJSON() -> None:

    # Create the JSON file used to store the GitHub repositories. If the JSON file already exist, the creation will be skipped
    try:

        # Create the JSON file "sites.json"
        with open("sites.json", "x") as file:
            pass

        # Write the JSON data, inside "sites.json", that will be used to store the repositories
        with open("sites.json", "w") as file:
            file.write("{\n    \"repositories\": {} \n}")  

    except FileExistsError:
        pass

    return

def readData():

    import json # Import the JSON library used to read the data of "sites.json"


    try:
        with open("sites.json", "r") as file:
            data = json.load(file) # Read the data of "sites.json"

    except FileNotFoundError: # Check if the file exists, if not return an error to the user and close the tool:
                              # In this case is required since readData() returns a value required by other functions and it would generate other errors

        print("- Error: The file 'sites.json' is required to use this tool but it hasn't been found in the same directory where is the tool.")
        print("- The tool will now create a new one.")
        createJSON() # Regenerate the json file
        input("- Press enter to exit from the tool...")
        quit() # Close the tool


    return data

def removeRepository(url: str):

    url_formatted = formatLinktoAPI(url=url) # Format the link given in input of a repository 

    data = readData() # Obtain the data of the JSON file

    try:

        del data["repositories"][url_formatted] # Delete the url from the data

    except KeyError:
        print("You have entered an url which is not in the JSON file.")
        return

    updateJSON(data=data) # Update the JSON file with the changes made


def updateJSON(data):

    import json # Import the JSON library to write the new data of the file

    # Open the JSON file and update it
    try:
        with open("sites.json", "w") as file: 
            json.dump(data, file) # Write the new data of the file


    except FileNotFoundError: # Check if the file exists, if not return an error to the user
        print("- Error: The file 'sites.json' is required to use this tool but it hasn't been found in the same directory where is the tool.")
        print("- The tool will now create a new one.")
        createJSON()

    return

def viewRepository():

    import time # Import the time library to allow the user to see the repository before the loop starts again asking for another option

    data = readData() # Obtain the data of the JSON file

    print("The repository you have saved are: \n")

    # Write all the repositories saved with the version the user is using
    for repository in data["repositories"]:
        print(f"* {formatLinkFromAPI(repository)} - {data["repositories"][repository]}")

    time.sleep(5) # Wait 5 seconds before the loop of the menu starts again

    return


def openDownloadFolder():

    import os, sys # Import the libraries 'os', 'sys'

    operatingSystem = sys.platform # Get the current Operating System, required to choose which command is required to open the download folder

    current_directory = os.getcwd() # Get the directory where is executed the tool, since the repositories are downloaded in the same folder

    # Check which Operating system is being used
    if operatingSystem == 'win32':
        os.system(f'explorer "{current_directory}"') # Execute the command to open the folder

    else:
        os.system(f'open "{current_directory}"') # Execute the command to open the folder

    return