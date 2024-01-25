import json
import requests
import csv
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

import os

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                commit_author = shaObject['commit']['author']['name']
                commit_date = shaObject['commit']['author']['date']

                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']

                for filenameObj in filesjson:
                    filename = filenameObj['filename']

                    if 'src' not in filename:
                        continue

                    if filename not in dictfiles:
                        dictfiles[filename] = {'count': 0, 'commits': []}
                    dictfiles[filename]['count'] += 1
                    dictfiles[filename]['commits'].append({'author': commit_author, 'date': commit_date, 'filename': filename})
            ipage += 1
    except Exception as e:
        print(f"Error receiving file data: {e}")
        exit(0)

def scatter_plot(file):
    data = pd.read_csv(file)

    # Convert dates to datetime objects
    data['Date'] = pd.to_datetime(data['Date'])

    # Extract the week number from the date
    data['Week'] = data['Date'].dt.isocalendar().week

    # Create a scatter plot
    plt.figure(figsize=(12, 6))

    # Assign unique colors to each author
    authors = data['Author'].unique()
    colors = plt.cm.rainbow(np.linspace(0, 1, len(authors)))

    for author, color in zip(authors, colors):
        subset = data[data['Author'] == author]
        plt.scatter(subset['Filename'], subset['Week'], s=subset['Touches'], color=color, label=author)

    plt.xlabel('Filename')
    plt.ylabel('Week Number')
    plt.title('File Touches Over Time by Different Authors')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # GitHub repo
    repo = 'scottyab/rootbeer'
    # repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
    # repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
    # repo = 'mendhak/gpslogger'


    # put your tokens here
    # Remember to empty the list when going to commit to GitHub.
    # Otherwise they will all be reverted and you will have to re-create them
    # I would advise to create more than one token for repos with heavy commits
    lstTokens = ["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"]

    dictfiles = dict()
    countfiles(dictfiles, lstTokens, repo)

    for key, value in dictfiles.items():
        print(f"{key}: {value}\n\n")

    print('Total number of files: ' + str(len(dictfiles)))

    file = repo.split('/')[1]
    # change this to the path of your file
    fileOutput = 'data/file_' + file + '.csv'
    rows = ["Filename", "Touches"]
    fileCSV = open(fileOutput, 'w')
    writer = csv.writer(fileCSV)
    writer.writerow(rows)

    bigcount = None
    bigfilename = None
    for filename, count in dictfiles.items():
        rows = [filename, count]
        writer.writerow(rows)
        if bigcount is None or count > bigcount:
            bigcount = count
            bigfilename = filename
    fileCSV.close()
    print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')


    scatter_plot(fileOutput)
