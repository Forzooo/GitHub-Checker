from system import readData, updateJSON, formatLinkFromAPI, formatLinktoAPI

def obtainVersions(url: str) -> tuple:

    import requests # Import the library required to get data from webpages
    
    repository_data = (requests.get(url)).json() # Obtain the data from the api of the repository given in input

    tag_names = [release["tag_name"] for release in repository_data] # Obtain all the tag names of the releases
    pre_release = [release["prerelease"] for release in repository_data] # Obtain all the boolean of the prereleases

    return (tag_names, pre_release) # Return every release and if it's a prerelease

def getLatestVersion(url: str) -> tuple:

    tagVersions = obtainVersions(url=url) # Obtain all the tag versions of the releases of the repository

    version = tagVersions[0][0] # Obtain the latest release of the repository
    prelease = tagVersions[1][0] # Obtain the flag whether the latest release of the repository is a prerelease


    return (version, prelease)


def checkNewVersions():

    import time # Import the time library to allow the user to see the repositories before the loop starts again asking for another option

    data = readData() # Read the data from "sites.json"
    repositories = data["repositories"] # Obtain the data of the repositories

    releasesUpToDate = 0 # Define a counter of the latest releases that the user already has

    # Iterate through all the urls saved in the JSON file
    for url in repositories:

        localVersion = repositories[url] # Obtain the local version (the one used by the user) of the repository
        onlineVersion = getLatestVersion(url=url) # Obtain the latest version and the flag whether it's a prelease, of the repository

        userFriendlyUrl = formatLinkFromAPI(url) # Convert the API link to the normal GitHub link

        # Verify if the local version of the user is not the latest one available (index 0 of onlineVerision)
        if localVersion != onlineVersion[0]:
            
            if (onlineVersion[1]):
                print(f"* A new release, version: {onlineVersion[0]} (prerelease) for {userFriendlyUrl} is now available. You are using version: {localVersion}")

            else:
                print(f"* A new release, version: {onlineVersion[0]} for {userFriendlyUrl} is now available. You are using version: {localVersion}")


            option = input("- Do you want to see the description of the release? (y/N) ") # Ask the user whether he wants to see the description of the release

            if option.lower() == "y":

                description = getDescriptionRelease(url=url)[0] # Call the get description release function to get the description of the latest release of a repository (index 0)

                print(f"Description of the release: \n{description}")

            option = input("- Do you want to download it? (y/N) ") # Ask the user whether he wants to download the latest release available

            if option.lower() == "y":
                downloadRelease(url=url) # Call the download release function with the url of the repository

                changeVersion(url=userFriendlyUrl, version=onlineVersion) # Call the change version function to update the user version of the repository to the latest one

            print("\n") # Add a new line to improve the readability between the releases of repositories


        else:
            releasesUpToDate += 1 # Update the counter of the latest relases the user already has by 1

    if releasesUpToDate == len(repositories): # If the user has all the latest releases, then write out the following output
        print("- You have the latest release of all the repositories.")

    time.sleep(2)
    return

def changeVersion(url: str, version: str):

    data = readData() # Obtain the data of the JSON file

    url_formatted = formatLinktoAPI(url=url) # Format the url of the repository

    try:

        old_version = data["repositories"][url_formatted] # Obtain the previous version the user was using of the repository

    except KeyError:
        return # The error is already written in the formatLinkToApi function

    # If the user is using the latest relase than update it to the last one available (This is used if the user has already updated with the new release, of a repository, 
    # without using this tool)
    if version.lower() == "latest":
        version = getLatestVersion(url=url_formatted)[0] # Get the latest version available on GitHub

    data["repositories"][url_formatted] = version # Change the version of the repository to the new one
    updateJSON(data=data) # Update the JSON file with the changes made

    print(f"Changed the version of {url} from {old_version} to {version}")

def downloadRelease(url: str):

    import requests # Import the library required to get data from webpages
    import os # Import the library used to create the directory of the release
    from tqdm import tqdm # Import the library used to create the progress bar of the download

    repository_data = (requests.get(url)).json() # Obtain the data from the api of the repository given in input

    assetsJSON = repository_data[0]["assets"] # Obtain only the assets of the latest release from the JSON file of the releases of the repository

    releasesUrls = [release["browser_download_url"] for release in assetsJSON] # Obtain all the urls of the file in the latest release

    urlFromAPI = formatLinkFromAPI(url) # Convert the url from the APi GitHub url
    url_splitted = urlFromAPI.split("/") # Split the url removing all the slash

    nameOfTheDirectory = f"{url_splitted[3]}-{url_splitted[4]}" # Create the name of the directory by url_splitted[3] the name of the owner of the repository
                                                                # and url_splitted[4] the name of the repository


    try:
        os.mkdir(nameOfTheDirectory) # Create a directory for the content downloaded of the repository
    
    except FileExistsError: # If the directory already exist skip the creation of it
        pass

    # Iterate through all the file that can be downloaded from the latest release
    for url in releasesUrls:
        response = requests.get(url=url, stream=True)  # Make a GET request to the URL and enable streaming

        file_name = url.split("/")[-1]  # Retrieve the file name from the URL
        total_size = int(response.headers.get('content-length', 0))  # Get the total size of the file

        # Create a progress bar
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name, ascii=True) as pbar:
            with open(f"{nameOfTheDirectory}/{file_name}", "wb") as file:  # Open a file in write binary mode
                for chunk in response.iter_content(chunk_size=1024):  # Iterate over the streamed content in chunks
                    if chunk:
                        file.write(chunk)  # Write the chunk to the file
                        pbar.update(len(chunk))  # Update the progress bar with the chunk size

    return


def getDescriptionRelease(url: str):


    import requests # Import the library required to get data from webpages
    
    repository_data = (requests.get(url)).json() # Obtain the data from the api of the repository given in input

    description = [release["body"] for release in repository_data] # Retrive all the "body" tags from all the releases in the json. Where "body" is the description of the release

    return description
