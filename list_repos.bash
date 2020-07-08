#!/bin/bash
#============================================================================
#  bash script to list github repos for the user
#  
#  Dependency:
#	curl
#	jq
#   
#  Synopsis:
#	./list_repos.bash <github user>
#
#  Output:
#	A csv file with header and sorted rows of repo information
#  
#============================================================================
if [[ $# -lt 1 ]]; then
    echo "Synopsis: $0  <github user>"
    exit 1
fi
user=$1
#user="AgoraIO-Community"
csvfile=$user.csv
Csvheader=''

PROPS=("name" "language" "description" "html_url" "contributors_url" "created_at" 
       "updated_at" "forks" "open_issues_count" "watchers")


function get_repo_count {
    username=$1
    cmd="curl -s https://api.github.com/users/$username | jq '. | .public_repos'"
    echo `eval $cmd`
}

# echo ${#PROPS[@]}
pcount=${#PROPS[@]}
Fields='['
for i in ${!PROPS[@]}; do
    prop=${PROPS[$i]}
    Csvheader="${Csvheader}$prop"
    Fields="${Fields}.$prop"
    if [[ $i -lt $(expr pcount-1) ]];
    then
	Csvheader="${Csvheader},"
	Fields="${Fields},"
    fi
done

Fields="${Fields}]"
jsonfile="github.json"

# create temp file for the parse csv columns
tmpfile="tmpfile.txt"
:> $tmpfile

# eval $cmd
repocnt=$(get_repo_count $user)
page=1
echo "$repocnt public repos are found for $user"
while [[ $repocnt > 0 ]]; do
    let repocnt-=100
    cmd="curl -s https://api.github.com/orgs/$user/repos?per_page=100\&page=$page"
    echo $cmd
    eval $cmd > $jsonfile
    cmd="cat $jsonfile | jq -r '.[] | $Fields | @csv' | sort -f"
    echo $cmd
    eval $cmd >> $tmpfile
    let page+=1
done

# Write the header
echo "$Csvheader" > $csvfile
# sort the result and append under the header
sort -f $tmpfile >> $csvfile
echo "CSV file has been saved to $csvfile"

# cleanup
rm $tmpfile
