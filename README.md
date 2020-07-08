# GetRepoList

## 1. About:

-   This Python script obtains a list of all public repositories associated with a chosen username. Utilizes Github's REST API v3.

## 2. Required Packages:

-   requests, "pip install requests"

## 3. How to use:

There are two output file type supported.  
**Synopsis**:
  ./**list_repos.py** -u <user> [-o <csvfile> | -j <jsonfile>]

For example:

 - ***list_repos.py -u helloworld*** => will pull repo list from username helloworld and save the content into helloworld.csv.  
- ***list_repos.py -u helloworld -j output.json*** => will pull repo list from username helloworld and save the raw json string into output.json.

## 4. CSV file:
See the line that defines properties in the python script.  Only these properties of the repo object will be written to the CSV file.

