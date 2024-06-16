# Import the classes from the library 'rich' used to improve the graphics of the terminal
from rich.markdown import Markdown
from rich.console import Console
from rich.progress import Progress
from system import System
import requests # Import the library required to verify if the repository exist
import os # Import the library used to create the directory of the release
import time # Import the libreary required to calculate the download speed

class VersionManager:

    def __init__(self) -> None:
        self.system = System()
        self.system.readJSON() # Python requires that for some reason 'data' needs to be read from this class otherwise the interpreter would
                               # set it to None, even if it has been read inside System
        self.url = None

    # It's recommended to use setUrl instead of assigning with 'self.url = ...' since in that case the url in System isn't updated with the changes
    def setUrl(self, url: str) -> None:
        self.system.url = url
        self.url = url
        
    def verifyRepositoryExist(self) -> bool:

        try:
            response = requests.get(self.url)

        except requests.exceptions.MissingSchema: # Check if the url does not have http or https
            return False

        if response.status_code != 200: # If the status code is not 200 then it means the repository does not exist
            return False

        return True

    # 'version' is not defined for the entire class because only 'addRepository' and 'changeVersion' requires it
    def addRepository(self, version: str) -> None:

        if not self.verifyRepositoryExist(): # Check if the repository given in input exist
            print(f"- The repository {self.url} does not exist.")
            return

        # Check if the user has written in the version input 'latest' to set the version of the repository to the last one available
        if version.lower() == "latest":
            version = self.getLatestVersion()[0] # Get the latest version available on GitHub

        self.system.data["repositories"][self.url] = version # Add to the dictionary the url and the version of the repository 

        self.system.updateJSON() # Update the JSON file with the changes made

        print(f"- Added the repository: {self.url}")

    def changeVersion(self, version: str):

        try:
            old_version = self.system.data["repositories"][self.url] # Obtain the previous version the user was using of the repository

        except KeyError:
            print("- You have entered an url which is not in the JSON file.")
            return 

        # If the user is using the latest relase than update it to the last one available (This is used if the user has already updated with the new release, of a repository, 
        # without using this tool)
        if version.lower() == "latest":
            version = self.getLatestVersion()[0] # Get the latest version available on GitHub

        self.system.data["repositories"][self.url] = version # Change the version of the repository to the new one
        self.system.updateJSON() # Update the JSON file with the changes made

        print(f"- Changed the version of {self.url} from {old_version} to {version}")

    def removeRepository(self):

        try:
            del self.system.data["repositories"][self.url] # Delete the url from the data

        except KeyError:
            print("- You have entered an url which is not in the JSON file.")
            return

        self.system.updateJSON() # Update the JSON file with the changes made

        print(f"- Removed the repository: {self.url}") # Print to the user that the repository has been removed

    def viewRepositories(self) -> None:

        console = Console()

        print("- The repositories you have saved, with the version you are using: ")

        # Write all the repositories saved with the version the user is using
        for repository in self.system.data["repositories"]:
            version = self.system.data["repositories"][repository] # Obtain the version of the repository

            repository_elements = repository.split("/")
            text = f"* [{repository_elements[-2]} - {repository_elements[-1]}]({repository}): {version}"

            console.print(Markdown(text)) # Convert the text to the Markdown styled one and print it
        
    def checkRepositories(self) -> bool:

        flag = True # The flag is set to be True and it won't be changed unless one or more repositories don't exist anymore
        repositories = self.system.data["repositories"] # Obtain the data of the repositories

        repositories_dead = [] # To avoid RuntimeError if more than one repository does not exist anymore keep in a list all the repositories
                               # and delete them after for loop

        # Look for repository that don't exist anymore and save them in the list
        for repository in repositories: # Iterate over the repositories link
            self.setUrl(repository) # It's required to set the url because otherwise the function 'verifyRepositoryExist'
                                    # would likely use another url all the time
            if not self.verifyRepositoryExist(): # If the repositories does not exist then remove it from "sites.json"
                repositories_dead.append(repository) # Add the dead repository to the list
                flag = False # One or more repositories don't exist anymore thus the flag is set to be false

        # Remove the repositories that don't exist anymore
        for repository in repositories_dead:
            self.setUrl(repository)

            print(f"- The repository {repository} does not exist anymore:")
            self.removeRepository()
        
            print("") # Improve the readability of the console 

        return flag

    def obtainVersions(self) -> tuple | None:
        
        repository_data = (requests.get(self.system.formatUrlToAPI())).json() # Obtain the data from the API of the repository given in input

        try:
            tag_names = [release["tag_name"] for release in repository_data] # Obtain all the tag names of the releases
        
        except TypeError as e:
            
            # If a repository if found to not be existing anymore check if there are other that don't exist too
            if repository_data['status'] == '404':
                self.checkRepositories()
                return None # None is used to tell checkNewVersions to end its execution. Otherwise RuntimeError would occur


        pre_release = [release["prerelease"] for release in repository_data] # Obtain all the boolean of the prereleases
        description = [release["body"] for release in repository_data] # Retrive all the "body" tags from all the releases in the json. Where "body" is the description of the release

        return (tag_names, pre_release, description) # Return every release, if it's a prerelease and its description

    def getLatestVersion(self) -> tuple | None:

        tagVersions = self.obtainVersions() # Obtain all the tag versions of the releases of the repository

        # This happens only if the repository don't exist anymore and it's required to return None to stop the execution of checkNewVersions
        if tagVersions == None:
            return None

        version = tagVersions[0][0] # Obtain the latest release of the repository
        prelease_flag = tagVersions[1][0] # Obtain the flag whether the latest release of the repository is a prerelease
        description = tagVersions[2][0] # Obtain the description of the latest release of the repository

        return (version, prelease_flag, description)

    def checkNewVersions(self):

        console = Console() # Initialize the Console class

        repositories = self.system.data["repositories"] # Obtain the data of the repositories

        releasesUpToDate = 0 # Define a counter of the latest releases that the user already has

        # Iterate through all the urls saved in the JSON file
        for url in repositories:

            self.setUrl(url) # It's required to set the URL in this way otherwise the functions will probably use all the time the URL of another repository

            localVersion = repositories[url] # Obtain the local version (the one used by the user) of the repository
            
            onlineVersion = self.getLatestVersion() # Obtain the latest version and the flag whether it's a prelease, of the repository

            if onlineVersion == None: # The function stops if one or more repositories are found to be dead, to avoid RuntimeError
                print("- Since you had some repositories that don't exist anymore, you need to recall the function.")
                return

            # Verify if the local version of the user is not the latest one available (index 0 of onlineVerision)
            if localVersion != onlineVersion[0]:
                
                # Check whether the latest release is a prerelease (index 1 of onlineVersion)
                if (onlineVersion[1]):
                    console.print(Markdown(f"* A new release, version: {onlineVersion[0]} (prerelease) for {url} is now available. You are using version: {localVersion}"))

                else:
                    console.print(Markdown((f"* A new release, version: {onlineVersion[0]} for {url} is now available. You are using version: {localVersion}")))


                option = input("- Do you want to see the description of the release? (y/N) ") # Ask the user whether he wants to see the description of the release

                if option.lower() == "y":

                    description = onlineVersion[2] # Obtain the description of the latest release of a repository (index 2 of getLatestVersion function)
                    descriptionMarkdown = Markdown(description) # Convert the description from the MD (Markdown) of GitHub to the one used by the library 'rich'
                    Console.print(Console(), descriptionMarkdown) # Write in the terminal the description of the release with the MD syntax

                option = input("- Do you want to download it? (y/N) ") # Ask the user whether he wants to download the latest release available

                if option.lower() == "y":
                    downloadResponse = self.downloadRelease() # Call the download release function with the url of the repository, and save the respose: it is needed to check whether
                                                            # an error occurred while trying to download the assets, or otherwise to tell the user where the files are
                    if downloadResponse in [ValueError, IndexError, None]: # If the user aborted the download or created an error then there is no reason 
                                                                           # to execute the following lines
                        return

                    print(f"- You can find the files you have downloaded in {downloadResponse} folder, which has been created inside the folder of the tool.")

                    self.changeVersion(version=onlineVersion[0]) # Call the change version function to update the user version of the repository to the latest one

                print("\n") # Add a new line to improve the readability between the releases of the repositories

            else:
                releasesUpToDate += 1 # Update the counter of the latest relases the user already has by 1

        if releasesUpToDate == len(repositories): # If the user has all the latest releases, then write out the following output
            print("- You have the latest release of all the repositories.")

        return

    def downloadRelease(self) -> type[ValueError] | type[IndexError] | str | None:

        repository_data = (requests.get(self.system.formatUrlToAPI())).json() # Obtain the data from the api of the repository given in input

        version_release = [release["tag_name"] for release in repository_data][0] # Obtain the version of the latest release

        assetsJSON = repository_data[0]["assets"] # Obtain only the assets of the latest release from the JSON file of the releases of the repository

        assetsUrl = [release["browser_download_url"] for release in assetsJSON] # Obtain the url of all the assets in the latest release
        assetsName = [assetsUrl[i].split("/")[-1] for i in range(len(assetsUrl))] # Retrive the file name from the url of each asset

        # Write the name of all the assets available to download
        print("- Assets available to download: ")
        for i, assetName in enumerate(assetsName):

            print(f"  {i+1}. {assetName}")

        option = input("- Write the number of the assets you want to download (ex. 1 3) (Write 'all' without quotes to download them all): ") # Get in input which asset the user wants to download | He will write it in numbers
        
        # Verify if the user wants to download all the assets
        if option.lower() != "all":
        
            retriveOptions = option.split(" ") # Remove a space from each choice
            retriveOptions = list(filter(lambda x: x != '', retriveOptions)) # If more spaces have been written in the input delete all of them

            # Verify whether the user does not want to download an asset
            if (len(retriveOptions) == 0):
                return None

            assetsToDownload = [] # Declare the list which will contain all the url of the assets that will be downloaded

            # Assing at each option, of the user, the correspondent asset
            for option in retriveOptions:
                try:
                    assetsToDownload.append(assetsUrl[int(option)-1]) # Since in the output, of the assets available to downlaod, every index was incremented by 1 (so the option will be),
                                                                    # now to be used from the list (which goes from 0 to len(list) - 1) it needs to be decremented by 1.
                                                                    # Moreover the option needs to be converted to an integer since the input type is string

                except ValueError: # If the option entered is not a number the following error message will be written and the download will be stopped
                    print(f"You have entered: {option} which is not a number. \nAborting the operation.")
                    return ValueError # ValueError will be returned to prevent the code from changing the version, the user is using, of the repository

                except IndexError: #  If the option is not in the list of the assets available the following error message will be written and the download will be stopped
                    print(f"You have entered: {option} which is not in the list of the assets available to download. \nAborting the operation.")
                    return IndexError # IndexError will be returned to prevent the code from changing the version, the user is using, of the repository


        else: # Since the user wants to download every asset, assign to the assetsToDownload list all the url of the assets

            assetsToDownload = assetsUrl

        url_splitted = self.url.split("/") # Split the url removing all the slashes

        nameOfTheDirectory = f"{url_splitted[3]}-{url_splitted[4]}-{version_release}" # Create the name of the directory by url_splitted[3] the name of the owner of the repository
                                                                    # and url_splitted[4] the name of the repository. Moreover include the verion of the release

        try:
            os.mkdir(nameOfTheDirectory) # Create a directory for the content downloaded of the repository
        
        except FileExistsError: # If the directory already exist skip the creation of it
            pass

        # Iterate through all the assets that the user has chosen to download
        for url in assetsToDownload:
            response = requests.get(url=url, stream=True)  # Make a GET request to the URL and enable streaming

            file_name = url.split("/")[-1]  # Retrieve the file name from the URL
            total_size = int(response.headers.get('content-length', 0))  # Get the total size of the file

            # Create a progress bar using the 'rich' library
            with Progress() as progress:
                task = progress.add_task("[cyan]Downloading...", total=total_size)
                start_time = time.time()
                downloaded = 0
                with open(f"{nameOfTheDirectory}/{file_name}", "wb") as file:  # Create the file, that will be downloaded, and open it in write binary mode
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk) # Write the chunk downloaded to the file
                            downloaded += len(chunk) # Added the chunk to the downloaded size
                            elapsed_time = time.time() - start_time # Calculate the time it took to download the chunk

                            # Verify that the time elapsed is greater than 0, otherwise it would result in a divsion by 0
                            if elapsed_time > 0:    
                                download_speed = downloaded / elapsed_time # Calculate the current download speed

                            else:
                                download_speed = 0 # Set the download speed to 0

                            progress.update(task, advance=len(chunk), description=f"[yellow]{file_name}[/yellow] [{downloaded / 1024 / 1024:.2f}MB/{total_size / 1024 / 1024:.2f}MB] Speed: {download_speed / 1024 / 1024:.2f}MB/s ")
                            # Update the progress bar with the current data

        return nameOfTheDirectory # Return the name of the directory for the print statement in 'checkNewVersions'