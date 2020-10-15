# Create Elastic search local

### import

# imports
import os
import json
import re
import tqdm

import pandas as pd
import numpy as np

from elasticsearch import Elasticsearch

### functions

def count_ipynb(folder):
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


def code_output(cell,temp_dict):
    """
    Explanation function
    """
    if cell['outputs']==[]:
        temp_dict['output_type'] = []
        temp_dict['output'] = []
    else:
        if type(cell['outputs']) is list and len(cell['outputs'])>2:
#             print(len(cell['outputs']),temp_dict['location'],temp_dict['file_cell'],cell['outputs'])
            pass #D NOG AANPASSEN OM MET ENORM LANGE OUTPUTS OM TE GAAN
        output_type = cell['outputs'][0]['output_type']
        temp_dict['output_type'] = output_type
        if output_type == 'stream':
            temp_dict['output'] = cell['outputs'][0]['text']
        elif output_type == 'error':
            temp_dict['output'] = cell['outputs'][0]['traceback']
        elif temp_dict['output_type'] == 'display_data':
            temp_dict['output'] = 'displayed data'
        elif temp_dict['output_type'] == 'pyout':
#             temp_dict['output'] = cell['outputs'][0]['html']
            temp_dict['output'] = 'unkown'
        elif 'data' in cell['outputs'][0].keys():
            temp_dict['output'] = list(cell['outputs'][0]['data'].values())
        elif 'text' in cell['outputs'][0].keys():
            temp_dict['output'] = cell['outputs'][0]['text']
        elif 'ename' in cell['outputs'][0].keys():
            temp_dict['output'] = cell['outputs'][0]['ename']+cell['outputs'][0]['evalue']
        else:
            temp_dict['output'] = 'unknown'
#             print(temp_dict['location'],temp_dict['file_cell'],cell)

    return temp_dict


def read_ipynb_cell(cell_id,cell_dict,file,folder,location,repo,user):
    """
    Explanation function
    """
    # os_system = platform.system()
    # if os_system == "Windows":
    #     location = location
    # if os_system == "Mac":
    #     pass

    with open(location,encoding="utf8") as notebook:
        try: 
            data = json.load(notebook) #does the file have a correct json format
        except Exception as e:
            print(e,file)
            return cell_id,cell_dict
        
        file_cell = 0
        nbformat = data['nbformat']
        if nbformat == 4: # current nbformat
            data_cells =  data['cells']
        elif nbformat == 3: # old nbformat
            data_cells =  data['worksheets'][0]['cells']
        elif nbformat == 2: # even older format
            data_cells = data['worksheets'][0]['cells']

        for cell in data_cells:
            temp_dict = {}
            if cell['cell_type'] == 'code' and (nbformat == 3 or nbformat == 2): #cell['source'] doesn't exist within this condition, use cell['input']
                text = cell['input']
            else:
                text = cell['source']
            # remove the '\n' at the end of each string in the list
            clean_cell = list(map(lambda s: s.strip(), text))         
            single_string = ' '.join(clean_cell)
            lines = len(clean_cell)

            temp_dict['file_cell'] = file_cell
            temp_dict['file'] = file
            temp_dict['nbformat'] = data['nbformat']
            temp_dict['folder'] = folder
            temp_dict['user'] = user
            temp_dict['repo'] =  repo
            temp_dict['location'] = location
            temp_dict['string'] = clean_cell
#             temp_dict['char'] = single_string
            temp_dict['lines'] = lines
            temp_dict['cell_type'] = cell['cell_type']
            if cell['cell_type'] == 'code':
                temp_dict = code_output(cell,temp_dict)

            cell_dict[cell_id] = temp_dict
            cell_id += 1
            file_cell += 1
            
    return cell_id,cell_dict


def files_to_dict(file_dict):
    """
    Explanation function
    """
    cell_id = 0
    cell_dict = {}

    for file in file_dict.keys():
        file_name = file_dict[file]['file']
        user = file_dict[file]['user']
        folder = file_dict[file]['folder']
        location = file_dict[file]['location']
        repo = file_dict[file]['repo']
        #kan ik dit niet in één regel schrijven, ff controleren nog bijv a,b,c = dict.values()

        cell_id_dict = read_ipynb_cell(cell_id,cell_dict,file_name,folder,location,repo,user)
        cell_id = cell_id_dict[0]
        cell_dict = cell_id_dict[1]
    return cell_id,cell_dict


def rec_to_actions(df):
    for record in df.to_dict(orient="records"):
        yield ('{ "index" : { "_index" : "%s", "_type" : "%s" }}'% (INDEX, TYPE))
        yield (json.dumps(record, default=int))
      

def index_marks(nrows, chunk_size):
    return range(1 * chunk_size, (nrows // chunk_size + 1) * chunk_size, chunk_size)


def split(dfm, chunk_size):
    indices = index_marks(dfm.shape[0], chunk_size)
    return np.split(dfm, indices)


def decompose_folder_name(folder_name):
    r1 = re.compile("([a-zA-Z0-9_-]+)")
    decompose = r1.findall(folder_name)
    user,repo = decompose[0],decompose[1]
    return user,repo

def create_SE_from_folder(es,folder,file_id,split_size):
    """
    Explenation
    """
    cwd = os.getcwd()
    path = cwd+'\\'+folder
    print(path)
    file_dict = {}
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".ipynb"):
                # location = os.path.join(root,file)
#                 fn = root.split('\\')[6] # root verschilt per pc, documents\\test_thesis vs documents\\uni\\jaarx\\test_thesis
                folder_name = root.split(folder)[1].split('\\')[1]
                user,repo = decompose_folder_name(folder_name)
                temp_dict = {}
                temp_dict['file'] = file
                temp_dict['folder'] = root.split('\\')[-1]
                temp_dict['location'] = os.path.join(root,file)
                temp_dict['user'] = user
                temp_dict['repo'] = repo
                
                file_dict[file_id] = temp_dict
                file_id += 1
    
    # CREATE DICT FOR ALL CELLS
    cell_dict = files_to_dict(file_dict)[1]
 

    # CREATE DATAFRAME FROM DICT
    cell_df = pd.DataFrame.from_dict(cell_dict,orient='index')
    cell_df.index = cell_df.index.set_names(['cell_id'])
    cell_df = cell_df.fillna('empty').reset_index()
    
    # PUT DATAFRAME INTO ELASTIC SEARCH
    for chuck in tqdm.tqdm(split(cell_df, split_size)): # r = es.bulk(rec_to_actions(cell_df))
        try:
            r = es.bulk(rec_to_actions(chuck))
        except Exception as e:
            print('Bulk failed at df cell_id:',chuck.cell_id.iloc[0],'-',chuck.cell_id.iloc[-1])
    return es,file_id,cell_df


### Create local elastic search variable

#### CHEATSHEET Elastic Search curl's
# !curl "http://localhost:9200/test"
# !curl -XDELETE "localhost:9200/restart"
# !curl -XPOST "http://localhost:9200/_shutdown"
# !curl "http://localhost:9200/_cat/indices?v"

### Count .ipynb files in current repository
# count_ipynb('repos_sample'),count_ipynb('repos')

### Put repositories into elastic search
HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST]) 

INDEX = "repos_cell"
TYPE = "record"

# %%time
gallery_es,file_id,gallery_df = create_SE_from_folder(es,'repos',0,1000)
# gallery_df
