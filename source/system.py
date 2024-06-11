import json # Import the JSON library used to read the data of "sites.json"
import os, sys # Import the libraries 'os', 'sys' required by the "openDownloadFolder" function

class System:

    def __init__(self) -> None:
        self.url = None
        self.data_path = "sites.json"
        self.createJSON() # Try to create the JSON file
        self.data = self.readJSON()

    def createJSON(self) -> None:

        # Create the JSON file used to store the GitHub repositories. If the JSON file already exist, the creation will be skipped
        try:

            # Create the JSON file "sites.json"
            with open(self.data_path, "x") as file:
                pass

            # Write the JSON data, inside "sites.json", that will be used to store the repositories
            with open(self.data_path, "w") as file:
                file.write("{\n    \"repositories\": {} \n}")  

        except FileExistsError:
            pass
    
    def readJSON(self) -> None:

        try:
            with open(self.data_path, "r") as file:
                self.data = json.load(file) # Read the data of "sites.json"

        except FileNotFoundError: # Check if the file exists, if not return an error to the user and close the tool:
                                # In this case is required since readData() returns a value required by other functions and it would generate other errors

            print("- Error: The file 'sites.json' is required to use this tool but it hasn't been found in the same directory where is the tool.")
            print("- The tool will now create a new one.")
            self.createJSON() # Regenerate the json file
            self.readJSON() # Recall the function, this time it will read the file

    def updateJSON(self) -> None:

        # Open the JSON file and update it
        try:
            with open(self.data_path, "w") as file: 
                json.dump(self.data, file) # Write the new data of the file


        except FileNotFoundError: # Check if the file exists, if not return an error to the user
            print("- Error: The file 'sites.json' is required to use this tool but it hasn't been found in the same directory where is the tool.")
            print("- The tool will now create a new one.")
            self.createJSON() # Regenerate the json file

        self.readJSON() # 'data' needs to be updated too for all the functions

    def formatUrlToAPI(self) -> str|None:
        
        # Remove all the slash from the url
        url_splitted = self.url.split("/")
        print(url_splitted)

        # Verify that the url is a GitHub url
        if url_splitted[2] != "github.com":
            print(f"The url given in input is: {url_splitted[2]} which is not github.com")
            return

        # Verify that the url of the repository is the one required in the README.md file
        if len(url_splitted) != 5:
            print("The url of the repository is not the in the format required by the script: \"https://github.com/username/repository_name \"")
            return

        # Strings used to modify the url given in input by the user
        api = "https://api.github.com/repos/"
        releases = "/releases"

        # url_splitted[3] is the username of the repository owner, url_splitted[4] is the name of the repository
        url_formatted = api + url_splitted[3] + "/" + url_splitted[4] + releases

        return url_formatted # The url formatted is returned and not assigned because only a few functions requires it

    def openDownloadFolder(self) -> None:

        operatingSystem = sys.platform # Get the current Operating System, required to choose which command is required to open the download folder

        current_directory = os.getcwd() # Get the directory where is executed the tool, since the repositories are downloaded in the same folder

        # Check which Operating system is being used
        if operatingSystem == 'win32':
            os.system(f'explorer "{current_directory}"') # Execute the command to open the folder

        else:
            os.system(f'open "{current_directory}"') # Execute the command to open the folder