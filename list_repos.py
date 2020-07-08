#!/usr/bin/python

# Script to generate csv file for repos

import json
import requests
import math
import sys, getopt

# *** CHANGE THIS FOR DIFFERENT USERNAME ***
# ******************************************
PROPERTIES = [ "name", "language", "description", "html_url", "contributors_url", "created_at", "updated_at", "forks", "open_issues_count", "watchers"]


def get_repo_count(username):
    response = requests.get("https://api.github.com/users/" + username)
    data = response.json()
    return data["public_repos"]

def get_contributor(repo):
    url = repo['contributors_url']
    response = requests.get(url)
    # the json is a list sorted by contribution count, so grab the first one
    contributors = response.json()
    owner = contributors[0]
    url =  "https://api.github.com/users/" + owner['login']
    response = requests.get(url)
    person = response.json()
    return person["name"]

# Note that Github API only returns 100 repos result max
def get_repo_json(username):
    c = get_repo_count(username)
    # print "total:", c
    pages = math.ceil(c/100.0)
    repos = []
    for page in range(int(pages)):
	url = "https://api.github.com/orgs/" + username + "/repos?per_page=100&page="+str(page+1)
	response = requests.get(url)
	repos += response.json()
    return repos

def set_owner(repos):
    for repo in repos:
	print "repo:", repo["name"],
	name = get_contributor(repo)
	print " owner:", name

def load_json(filename):
    print (",".join(s for s in PROPERTIES))
    with open(filename) as json_file:
	repos = json.load(json_file)
	for repo in repos:
	    print(",".join(str(repo[s]) for s in PROPERTIES)) 

# write the downloaded content to CSV file
def main_makecsv(user, csvfile):
     print "pulling repo information from " + user, " ..."
     repos = get_repo_json(user)
     print "repos count = ", len(repos)
     f = open(csvfile, 'w')
     f.write(",".join(s for s in PROPERTIES))
     f.write('\n')
     for repo in repos:
	s = (",".join(str(repo[s]) for s in PROPERTIES)) + "\n"
	f.write(s)

     f.close()

# write the downloaded content to JSON file
def main_dumpjson(user, jsonfile):
     print "pulling repo information from " + user, " ..."
     d = get_repo_json(user)
     print "repos count = ", len(d)
     with open(jsonfile, 'w') as outfile:
	json.dump(d, outfile)

     print "data has be exported to ", jsonfile


if __name__ == '__main__':
   user = ''
   outputfile = ''
   SYNOSIS = sys.argv[0] + ' -u <user> [-o <csvfile> | -j <jsonfile>]'
   _dumpJson = False

   try:
      opts, args = getopt.getopt(sys.argv[1:],"hu:oj:",["ifile=","ofile=","jfile="])
   except getopt.GetoptError:
      print SYNOSIS
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print SYNOSIS
         sys.exit()
      elif opt in ("-u", "--user"):
         user = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-j", "--jfile"):
	 outputfile = arg
	 _dumpJson = True

   if user == '':
	print SYNOSIS
	sys.exit(3)
   if outputfile == '':
	outputfile = user + ".csv"

   print 'User Account is',user
   print 'Output file is',outputfile

   if _dumpJson:
	main_dumpjson(user, outputfile)
   else:
	main_makecsv(user, outputfile) 
