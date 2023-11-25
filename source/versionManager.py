from system import readData, updateJSON, formatLinkFromAPI, formatLinktoAPI

def obtainTagNames(url: str) -> list:

    import requests # Import the library required to get data from webpages
    
    repository_data = (requests.get(url)).json() # Obtain the data from the api of the repository given in input

    tag_names = [release["tag_name"] for release in repository_data] # Obtain all the tag names of the releases

    return tag_names

def getLatestVersion(url: str) -> str:

    tagVersions = obtainTagNames(url=url) # Obtain all the tag versions of the releases of the repository

    version = tagVersions[0] # Obtain the latest release of the repository

    return version


def checkNewVersions():

    import time # Import the time library to allow the user to see the repositories before the loop starts again asking for another option

    data = readData() # Read the data from "sites.json"
    repositories = data["repositories"] # Obtain the data of the repositories

    # Iterate through all the urls saved in the JSON file
    for url in repositories:

        localVersion = repositories[url] # Obtain the local version (the one used by the user) of the repository
        onlineVersion = getLatestVersion(url=url) # Obtain the latest version of the repository

        userFriendlyUrl = formatLinkFromAPI(url) # Convert the API link to the normal GitHub link

        # Verify if the local version of the user is the latest one available
        if localVersion == onlineVersion:
            print(f"* You have already the latest version: {localVersion} of {userFriendlyUrl}")

        else:
            print(f"* A new release, version: {onlineVersion} for {userFriendlyUrl} is now available. You are using version: {localVersion}")

    time.sleep(5)
    return

def changeVersion(url: str, version: str):

    data = readData() # Obtain the data of the JSON file

    url_formatted = formatLinktoAPI(url=url) # Format the url of the repository

    try:

        old_version = data["repositories"][url_formatted] # Obtain the previous version the user was using of the repository

    except KeyError:
        return # The error is already written in the formatLinkToApi function

    data["repositories"][url_formatted] = version # Change the version of the repository to the new one

    updateJSON(data=data) # Update the JSON file with the changes made

    print(f"Changed the version of {url} from {old_version} to {version}")