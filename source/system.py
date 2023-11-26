def formatLinktoAPI(url: str) -> str|None:
    
    import requests # Import the library required to verify if the repository exist

    try:

        response = requests.get(url)

    except requests.exceptions.MissingSchema:
        print(f"You have entered an invalid url: {url}")
        return

    if response.status_code != 200:
        print("The repository does not exist.")
        return

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

def addLink(url: str) -> None:

    from versionManager import getLatestVersion

    data = readData()

    version = getLatestVersion(url=url) # Since it's a new url, the JSON needs to get the latest version of the repository

    data["repositories"][url] = version # Add to the dictionary the url and the latest version of the repository 

    updateJSON(data=data) # Update the JSON file with the changes made

    print(f"Added the repository: {url}")

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

    with open("sites.json", "r") as file:
        data = json.load(file) # Read the data of "sites.json"

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
    with open("sites.json", "w") as file: 
        json.dump(data, file) # Write the new data of the file

    return

def viewRepository():

    import time # Import the time library to allow the user to see the repository before the loop starts again asking for another option

    data = readData() # Obtain the data of the JSON file

    print("The repository you have saved are: \n")

    # Write all the repositories saved with the version the user is using
    for repository in data["repositories"]:
        print(f"* {formatLinkFromAPI(repository)} - {data["repositories"][repository]}")

    time.sleep(5) # Wait 5 seconds before the loop starts again

    return