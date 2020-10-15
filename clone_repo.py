# CLONING GITHUB REPOSITORIES



### IMPORT
import requests
import re
import os
import json
import itertools
import tqdm

from bs4 import BeautifulSoup
from git import Repo # add 'git' module through anaconda navigator + pip install gitpython


### VARIABLES
url = "https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks"
new_folder = "repos"


### FUNCTIONS
def try_link_getter(ul_list):
    """
    The function takes a list of unordered lists (ul's) as input and returns a list 
    of all the list items (li) of the ul's that contain a href link 
    """
    links = []
    for ul in ul_list:
        for line in ul:
            try:
                links.append(line.a.get('href'))
            except:
                pass
    return links


def scan_page_not_found(repositories_list):
    """
    Ëxplanation
    """
    error_list = []
    for url in tqdm.tqdm(list(repositories_list)):
        r  = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data,features="html.parser")
        try:
            if 'Page not found · GitHub' in soup.title.string:
                error_list.append(url)
        except:
            error_list.append(url)
    return error_list


def clone_repositories(repositories_list,error_list,folder_dir):
    """ 
    Explanaition 
    """
    cwd = os.getcwd()
    for url in tqdm.tqdm(repositories_list):
        if url not in error_list:
            repo_name = "("+url.split('/')[3]+")"+url.split('/')[4]
            repo_dir = cwd+'\\'+folder_dir+'\\'+repo_name
            if not os.path.exists(folder_dir+'/'+repo_name): # skip already downloaded repo
                try:
                    Repo.clone_from(url,repo_dir)
                except:
                    print('Failed for:',repo_name,url)


def count_ipynb(folder):
    """
    Explanation
    """
    path = os.getcwd()+'\\'+folder
    try:
        dir_list = os.listdir(path)
    except:
        return "this repository doesn't exist"

    file_id = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".ipynb"):
                file_id += 1
    return file_id


def valid_check_samplesize(user_input,max_size):
    try:
        size = int(user_input)
        if max_size > size > 0:
            print("Creating a error_list of 'Page not found' github repositories url's... (approx 2 min)")
            error_list = scan_page_not_found(github_repositories)
            print("Downloading sample size of",size)
            clone_repositories(list(github_repositories)[:size],error_list,new_folder)
        else:
            print("Choose within the delimiters of 0 and",max_size)
            print(),start_cloning(max_size)
    except:
        print("Type a integer")
        print(),start_cloning(max_size)


def start_cloning(max_size):
    """ 
    Functions that interacts with the user via the shells, the user gives 
    variables to start the cloning
    """
    print("A total of",max_size,"repositories have been found.")
    print("Download all(Y) or use a sample size(N)? Type (Y) to clone all repos or type (N) to choose a sample size or (Q) to quit" )
    user_input1 = input()
    if user_input1 == "Y" or user_input1 == "y":
        print("Are you sure to download all",max_size,"repositories? Type (Y) to confirm")
        user_input2 = input()
        if user_input2 == "Y" or user_input2 == "y":
            print("Creating a error_list of 'Page not found' github repositories url's... (approx 2 min)")
            error_list = scan_page_not_found(github_repositories)
            print("Downloading sample size of",max_size)
            clone_repositories(list(github_repositories),error_list,new_folder)
        else:
            print("Type the size of your sample size")
            user_input3 = input()
            valid_check_samplesize(user_input3,max_size)

    elif user_input1 == "N" or user_input1 == "n":
        print("Type the size of your sample size")
        user_input3 = input()
        valid_check_samplesize(user_input3,max_size)

    elif user_input1 == "Q" or user_input1 == "q":
        return

    else:
        print("Type a 'y' or 'n'")
        print(),start_cloning(max_size)


### WEBSCRAPING JUPYTER GALLERY (CREATE LIST OF GITHUB REPOS URL'S)
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data,features="html.parser")

body = soup.find_all("div", {"class": "markdown-body"})[0] # using [0] at the end since there is only 1 result of a div with class 'markdown-body'
all_links_in_body = set([link.get('href') for link in body.find_all('a')])
remaining = set()

r1 = re.compile(".*github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$") # get all links the same as .....github.com/..../....$ 
r2 = re.compile(".*github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+")  # get all links the same as .....github.com/..../....+ 
r3 = re.compile("github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+")    # get all links the same as github.com/..../....+ 

github_repositories = set(filter(r1.match, all_links_in_body)) # There are 9 duplicates 112->103 correct url
all_github_links = set(filter(r2.match, all_links_in_body))
github_repo_remaining = all_github_links - github_repositories # the difference between a - b

created_github_repos = [r3.findall(line) for line in github_repo_remaining] # list of list with all matches within a single url
created_github_repos = itertools.chain.from_iterable(created_github_repos) # flatten the list of lists to a list
created_github_repos = set(['https://'+url for url in created_github_repos]) # add 'https://' to created a valid url

github_repositories.update(created_github_repos)
remaining = all_links_in_body - all_github_links

r4 = re.compile(".*github.com/[a-zA-Z0-9_-]+$") # get all links the same as .....github.com/..../.... 
github_users = set(filter(r4.match, remaining)) # There are 9 duplicates 112->103
remaining = remaining - github_users

r5 = re.compile(".*/github/") # get all links the same as /github/ 
r6 = re.compile("github/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+")    # get all links the same as github/..../....+ 
github_links2 = set(filter(r5.match, remaining)) # There are 7 duplicates 202=>195
created_github_repos2 = set(['https://github.com'+r6.findall(line)[0][6:] for line in github_links2 if r6.findall(line)!=[]])

github_repositories.update(created_github_repos2)
print("Scraped",len(github_repositories),"github repositories url's from the gallery page")



### CLONE REPOSITORIES (USE LIST OF GITHUB REPOS URL'S)
if not os.path.exists(new_folder): # create folder in which to put all the repositories (if it does not exist)
    os.makedirs(new_folder)


# print("Creating a error_list of 'Page not found' github repositories url's... (approx 2 min)")
# error_list = scan_page_not_found(github_repositories)
# line 98 / 119
# error_list = ['https://github.com/blog/2012',
#  'https://github.com/downloads/notebooks',
#  'https://github.com/cfangmeier/Small',
#  'https://github.com/JuliaLang/IJulia',
#  'https://github.com/yoavram/CS1001',
#  'https://github.com/raw/master',
#  'https://github.com/Arn-O/py-gridmancer',
#  'https://github.com/jakevdp/jakevdp',
#  'https://github.com/tree/master',
#  'https://github.com/kernc/backtesting',
#  'https://github.com/GaelVaroquaux/nilearn_course',
#  'https://github.com/carljv/cython_testing',
#  'https://github.com/lgiordani/blog_source']

start_cloning(int(len(github_repositories)))
