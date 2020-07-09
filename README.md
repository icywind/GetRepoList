# GetRepoList

## 1. About:

-   This repo provide scripts obtains a list of all public repositories associated with a chosen username. Utilizes Github's REST API v3.
-   A python script and a bash script are provided.  Either one can provide the same output.  Choose which one to use based on environment.

## 2. Required Packages:
Python Dependency
-   *requests*, "pip install requests"

Bash Dependency
- *curl*
- *jq*

## 3. How to use:

### Python

There are two output file type supported.  
**Synopsis**:
  ./**list_repos.py** -u <user> [-o <csvfile> | -j <jsonfile>]

For example:

 - ***./list_repos.py -u helloworld*** => will pull repo list from username helloworld and save the content into helloworld.csv.  
- ***./list_repos.py -u helloworld -j output.json*** => will pull repo list from username helloworld and save the raw json string into output.json.

### Bash
**Synopsis**:
**./list_repos.bash** \<user>

For example:

- ***./list_repos.bash helloworld*** => will pull repo list from username helloworld and save the content into helloworld.csv.  
## 4. CSV file:
See the line that defines properties in the python script.  Only these properties of the repo object will be written to the CSV file.

