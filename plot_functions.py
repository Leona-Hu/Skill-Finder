import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def plot_job_dis_by_state(df):
    '''
    This function plots the job position distribution heat map 
    among all the states in US.
    :param df: dataframe that stores the dataset
    :type df: pd.DataFrame
    '''
    assert isinstance(df, pd.DataFrame)
    
    import plotly.graph_objects as go
    state_dict = dict()
    for state_value in df['state']:
        if state_value in state_dict:
            state_dict[state_value] += 1
        else:
            state_dict[state_value] = 1
    # the only state with no jobs posted
    state_dict['MT'] = 0
    state_dict = dict(sorted(state_dict.items(), key=lambda item:item[1], reverse=True))
    state_df = pd.DataFrame({'state': list(state_dict.keys()), 'num_of_jobs': list(state_dict.values())})
    print(state_df)
    fig = go.Figure(data=go.Choropleth(
        locations=state_df['state'], # Spatial coordinates
        z = state_df['num_of_jobs'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "# of positions",
    ))

    fig.update_layout(
        title_text = 'Number of technology positions available by state',
        geo_scope='usa', # limite map scope to USA
    )
    fig.show()
    
def plot_top_ca_cities(df):
    '''
    This function plots the bar plot for the top 10 cities 
    in California with most technology positions available.
    :param df: dataframe that stores the dataset
    :type df: pd.DataFrame
    '''
    assert isinstance(df, pd.DataFrame)
    
    ca_cnt = df[df['state'] == 'CA']
    ca_data = ca_cnt['city'].value_counts()[:10]
    ca_labels = ca_cnt['city'].value_counts().index.tolist()[:10]
    plt.barh(range(10), ca_data, height=0.7, color='green', alpha=0.8)
    plt.yticks(range(10), ca_labels)
    plt.xlim(0,950)
    plt.xlabel("# of positions")
    plt.title("Top 10 cities in California with most positions available")
    plt.savefig('graphs/top_ca_cities.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_top_cities_usa(df):
    '''
    This function plots the bar plot for the top 15 cities 
    among all cities in US with most technology positions available.
    :param df: dataframe that stores the dataset
    :type df: pd.DataFrame
    '''
    assert isinstance(df, pd.DataFrame)
    
    data = df['joblocation_address'].value_counts()[0:15]
    labels = df['joblocation_address'].value_counts().index.tolist()[0:15]
    
    plt.barh(range(15), data, height=0.7, color='green', alpha=0.8)
    plt.yticks(range(15), labels)
    plt.xlim(0,1500)
    plt.xlabel("# of positions")
    plt.title("Top 15 cities with most positions available")
    plt.savefig('graphs/top_cities.png', dpi=300, bbox_inches='tight')
    plt.show()

def top_companies(df):
    '''
    This function plots the bar plot for the top 10 companies that 
    post most technology positions.
    :param df: dataframe that stores the dataset
    :type df: pd.DataFrame
    '''
    assert isinstance(df, pd.DataFrame)
    
    data = df['company'].value_counts()[0:11]
    labels = df['company'].value_counts().index.tolist()[0:11]
    rht_id = labels.index('Robert Half Technology')
    del labels[rht_id]
    data = list(data)
    del data[rht_id]
    
    plt.barh(range(10), data, height=0.7, color='green', alpha=0.8)
    plt.yticks(range(10), labels)
    plt.xlim(0,350)
    plt.xlabel("# of positions")
    plt.title("Top 10 companies with most positions available")
    plt.savefig('graphs/top_companies.png', dpi=300, bbox_inches='tight')
    plt.show()
    
def count_skill(df, skills):
    '''
    This function count the occurrence of each skill in the skills list.
    :param df: dataframe that stores the dataset
    :type df: pd.DataFrame
    
    :param skills: a list of skills that we want to consider
    :type skills: list
    '''
    assert isinstance(df, pd.DataFrame)
    assert isinstance(skills, list)
    assert len(skills) > 0
    
    dic = {}
    for col in df.columns[5:][:-2]: 
        cnt = df[col].value_counts().get(1)
        if cnt is not None and col in skills:
            dic[col] = cnt
    dic = sorted(dic.items(), key=lambda item: item[1], reverse=True)
    label = []
    cnt = []
    for each in dic:
        label.append(each[0])
        cnt.append(each[1])
    return label, cnt

def plot_yoe_graph(df):
    '''
    This function plots the number of positions posted for different YoE.
    :param df: dataframe that stores the dataset
    :type df: pd.DataFrame
    '''
    assert isinstance(df, pd.DataFrame)
    
    yoe_cnt_dict = {}
    for key in df['YOE'].value_counts().index:
        yoe_cnt_dict[key] = df['YOE'].value_counts()[key]
    yoe_cnt_dict = dict(sorted(yoe_cnt_dict.items(), key=lambda item: item[0], reverse=False))
    print(yoe_cnt_dict)
    plt.bar(range(10), list(yoe_cnt_dict.values()), width=0.7, color='green', alpha=0.8)
    plt.xticks(range(10), list(yoe_cnt_dict.keys()))
    plt.xlabel("year of experience")
    plt.ylabel("# of positions")
    plt.title("Number of technology positions posted which required YOE")
    plt.savefig('graphs/yoe.png', dpi=300, bbox_inches='tight')
    plt.show()
    
def plot_edu_job(df):
    '''
    This function plots the number of positions posted for different education levels.
    :param df: dataframe that stores the dataset
    :type df: pd.DataFrame
    '''
    assert isinstance(df, pd.DataFrame)
    
    ass_yoe_data = df[df['Min Ed Level'] == 'associate']
    ass_yoe_data = ass_yoe_data['YOE'].dropna()
    ass_avg_yoe = len(ass_yoe_data)
    ba_yoe_data = df[df['Min Ed Level'] == 'bachelor']
    ba_yoe_data = ba_yoe_data['YOE'].dropna()
    ba_avg_yoe = len(ba_yoe_data)
    ma_yoe_data = df[df['Min Ed Level'] == 'master']
    ma_yoe_data = ma_yoe_data['YOE'].dropna()
    ma_avg_yoe = len(ma_yoe_data)
    plt.bar(range(3), [ass_avg_yoe, ba_avg_yoe, ma_avg_yoe], width=0.65, color='green', alpha=0.8)
    plt.xticks(range(3), ['associate', 'bachelor', 'master'])
    plt.ylim(0,5000)
    plt.ylabel("# of positions")
    plt.title("Number of technology positions posted for different edu level")
    plt.savefig('graphs/edu_job.png', dpi=300, bbox_inches='tight')
    plt.show()
    
def plot_level_job(df):
    '''
    This function plots the number of positions posted for different experience level
    - new grad with 1 year of experience
    - junior with 2-4 years of experience
    - senior with more than 5 years of experience
    :param df: dataframe that stores the dataset
    :type df: pd.DataFrame
    '''
    assert isinstance(df, pd.DataFrame)
    
    new_grad_data = df[df['YOE'] == 1.0]['YOE'].value_counts()
    junior_data = df[(df['YOE'] == 4.0) | (df['YOE'] == 3.0) | (df['YOE'] == 2.0)]['YOE'].value_counts()
    senior_data = df[df['YOE'] >= 5.0]['YOE'].value_counts()
    data = [sum(new_grad_data), sum(junior_data), sum(senior_data)]
    labels = ['New Grad (1 yr)', 'Junior (2-4 yrs)', 'Senior (>5 yrs)']
    plt.figure()
    plt.bar(range(3), data, width=0.7, color='green', alpha=0.8)
    plt.xticks(range(3), labels)
    plt.title("Number of technology positions posted for different experience level")
    plt.ylabel("# of positions")
    plt.savefig('graphs/yoe_job.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    patches, l_text, p_text = plt.pie(data, labels=labels, labeldistance=1.1, autopct="%1.1f%%", shadow=False, startangle=90, pctdistance=0.6)
    plt.axis("equal")
    plt.legend( loc = 'upper right',bbox_to_anchor=(1., 1.4), fontsize=14, borderaxespad=0.3)
    plt.savefig('graphs/yoe_job_pie.png', dpi=300, bbox_inches='tight')
    plt.show()
    
def plot_compliment(original_df):
    '''
    This function plots the correlation between skills.
    Given you are proficient in one skill, what else can you learn to better 
    help you prepared for job finding.
    :param original_df: dataframe that stores the dataset
    :type original_df: pd.DataFrame
    '''
    assert isinstance(original_df, pd.DataFrame)
    
    original_df['aws'] += original_df['amazon web services']
    original_df['golang'] += original_df['go lang']
    del original_df['amazon web services']
    del original_df['go lang']
    
    program_languages = ['python', 'scala', 'c#', 'matlab', 'java', 'javascript', 
                        'css', 'sql', 'perl', 'swift', 'verilog', 'golang',
                       'c++', 'rust', 'haskell', 'erlang', 'clojure']

    import collections

    def tree():
        return collections.defaultdict(tree)

    d = tree()
    for key1 in program_languages:
        for key2 in program_languages:
            d[key1][key2] = 0

    top6 = ['sql', 'java', 'scala', 'javascript', 'css', 'python']
    
    for row in original_df.iterrows():
        rowval = row[1]
        for topkey in top6:
            for key in program_languages:
                if (rowval[key] != 0 and rowval[topkey] !=0 and key != topkey):
                    d[topkey][key] += 1
    
    import seaborn as sns

    vals = []
    for val in top6:
        vals_intermediate = []
        for key in program_languages:
            vals_intermediate.append(d[val][key])

        vals_intermediate = vals_intermediate / np.max(vals_intermediate)

        vals.append(vals_intermediate)
    
    plt.figure(figsize=(8,8))
    ax = sns.heatmap(np.transpose(np.array(vals)) / np.max(vals), xticklabels=top6, yticklabels=program_languages, cmap=sns.diverging_palette(220, 20, as_cmap=True))
    ax.xaxis.set_ticks_position('top')
    plt.savefig('graphs/heatmap_2.png', dpi=300)
    
    skills= ['python', 'scala', 'c#', 'matlab', 'java', 'javascript', 
              'css', 'sql', 'perl', 'swift', 'verilog', 'golang',
              'c++', 'rust', 'haskell', 'erlang', 'clojure', 
              'android', 'ios', 
              'linux', 'unix', 'arm', 
              'tcp/ip', 'udp', 
              'mongodb', 'mysql', 'nosql', 't-sql', 'spark', 'maven', 
              'google cloud', 'aws', 'azure', 'oracle cloud', 
              'react', 'backbone', 'angular', 'html', 'express.js', 'rest api', 
              'kafka', 'django', 'redux', 'hadoop', 'junit', 'docker']

    # changed restful to rest, oracle cloud to oracle, azure to azure paas

    d_skills = tree()
    for key1 in skills:
        for key2 in skills:
            d_skills[key1][key2] = 0
    
    for row in original_df.iterrows():
        rowval = row[1]
        for topkey in top6:
            for key in skills:
                if (rowval[key] != 0 and rowval[topkey] !=0 and key != topkey):

                    d_skills[topkey][key] += 1
    
    vals = []
    for val in top6:
        i=0
        vals_intermediate = []
        for key in skills:
            i+=1
            vals_intermediate.append(d_skills[val][key])

        vals_intermediate = vals_intermediate / np.max(vals_intermediate)
        vals.append(vals_intermediate)
    
    plt.figure(figsize=(10,10))
    ax = sns.heatmap(np.transpose(vals), xticklabels=top6, yticklabels=skills, cmap=sns.diverging_palette(220, 20, as_cmap=True))
    ax.xaxis.set_ticks_position('top')
    plt.savefig('graphs/heatmap.png', dpi=300)
    
    from heapq import nlargest
    from operator import itemgetter
    flattened = ((outerkey, innerkey, value) for outerkey, innerdict in d_skills.items() 
                     for innerkey, value in innerdict.items())
    result = nlargest(30, flattened, key=itemgetter(2))
    
    from collections import OrderedDict, Counter

    colors = ['r', 'b', 'g', 'k', 'c', 'm']

    for idx, val in zip(range(len(top6)), top6):
        intermediate = d_skills[val].items()
        tmp = []
        for skill in skills:
            tmp.append(d_skills[val][skill])
        tmp2 = Counter(d_skills[val])
        tmp = sorted(tmp)
        vals = tmp2.most_common(5)
        vals = [list(elem) for elem in vals]
        nums = [row[1] for row in vals]
        skills = [row[0] for row in vals]

        fontsize=10
        plt.figure(figsize=(4,4), dpi=120)
        plt.bar(range(len(nums)), nums/np.max(nums), color=colors[idx], width=0.7)
        plt.title(val, fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.ylabel('Normalized co-occurrence', fontsize=fontsize)
        plt.xticks(range(len(nums)), skills, rotation=20, fontsize=fontsize)
        plt.xlabel('Skills to learn', fontsize=fontsize)
        plt.savefig('graphs/skill_'+val+'.png', dpi=300, bbox_inches='tight')