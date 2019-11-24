import pandas as pd
import os
import re
import numpy as np
    
def read_data():
    data_folder = 'C:\\Users\\kevin\\Desktop\\ECE 143\\Project\\TextFiles'
    descritopnList = {}
    for filename in os.listdir(data_folder):
        with open('C:\\Users\\kevin\\Desktop\\ECE 143\\Project\\TextFiles\\'+filename, errors = 'ignore') as f:
            text = f.read()
            filename = filename[:-4]
            descritopnList[filename] = text.lower()
    return descritopnList
    

def create_df(text):
    skill_file = 'C:\\Users\\kevin\\Desktop\\ECE 143\\Project\\Keywords.xlsx'
    df  = pd.DataFrame(text.values(), columns=['description'], index = text.keys())
    skills = pd.read_excel(skill_file)
    skillsLower = skills.apply(lambda i: i.str.lower())
    for i in skillsLower['Skills']:
        df[i] = df['description'].apply(skill_required, args= (i,))
    locations = find_locations()
    new = pd.concat([df,locations], axis=1, join='inner')
    new.loc['Sum'] = df.sum()
    new['YOE'] = new['description'].apply(find_years_of_experience)
    new['Min Ed Level'] = new['description'].apply(find_education_level)
    return new


def make_int(x):
    if x is numpy.float64:
        x = int(x)

def find_education_level(string):
    indeces = []
    for m in re.finditer('degree', string):
        indeces.append(m.start())
    seg = []
    for i in indeces:
        seg.append(string[i-50:i+10])
    degrees = {'associate':'associate', 'bachelor':'bachelor', 'master':'master','b.s.':'bachelor', 'm.s.':'master', '4':'bachelor', 'four':'bachelor', '2':'associate', 'two':'associate'}
    degree_list = []
    for i in seg:
        degree_list = [degrees[j] for j in degrees.keys() if j in i]
    if not degree_list:
        return np.NaN
    elif 'associate' in degree_list:
        return 'associate'
    elif 'bachelor' in degree_list:
        return 'bachelor'
    elif 'master' in degree_list:
        return 'master'
    else:
        return np.NaN

def find_years_of_experience(string):
    numbers = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10,'1':1, '2':2, '3':3, '4':4,  
'5':5, '6':6, '7':7, '8':8, '9':9, '10':10}
    indeces = []
    for m in re.finditer('year', string):
        indeces.append(m.start())
    seg = []
    for i in indeces:
        seg.append(string[i-30:i+10])
    noeList = []
    for i in seg:
        noeList.append([numbers[j] for j in numbers.keys() if j in i])
    for i in noeList:
        if not i:
            noeList[noeList.index(i)] = np.NaN
    try:
        if min(noeList) == 'A':
            return np.NaN
    except:
        pass
    try:
        if min(min(noeList)) == 'A':
            return np.NaN
    except:
        pass
    try:
        return min(min(noeList))
    except:
        try:
            return min(noeList)
        except:
            return np.NaN

def find_locations():
    links_file = 'C:\\Users\\kevin\\Desktop\\ECE 143\\Project\\links.txt'
    chunk = 'https://jobs.thejobnetwork.com/job/'
    chunk2 = 'software-engineer-job-in-'
    with open(links_file, errors='ignore') as f:
        df = pd.read_csv(f)
    df['links'] = df['links'].apply(lambda i:i[len(chunk):])
    df['split'] = df.apply(lambda i:i.str.split('/'))
    df['id'] = df['split'].apply(lambda i: i[0])
    df['location'] = df['split'].apply(lambda i: i[1])
    df.index = df['id']
    del df['split'], df['links'], df['id']
    df['location'] = df['location'].apply(lambda i:i[len(chunk2):])
    df['split'] = df.apply(lambda i: i.str.split('-'))
    df['zip'] = df['split'].apply(is_zip)
    df['nozip'] = df['split'].apply(pop_zip)
    df['state'] = df['nozip'].apply(lambda i: i[-1])
    df['city'] = df['nozip'].apply(lambda i:i[:-1])
    df['city'] = df['city'].apply(lambda i: ' '.join(i))
    del df['location'], df['split'], df['nozip']
    return df

def pop_zip(l):
    try:
        if RepresentsInt(l[-1]):
            l.pop(-1)
        return l
    except:
        pass

def is_zip(l):
    try:
        if RepresentsInt(l[-1]):
            return l[-1]
        else:
            return None
    except:
        pass

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def skill_required(string, skill):
    if skill in string:
        return 1
    else:
        return 0
   