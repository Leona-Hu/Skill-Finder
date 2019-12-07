import pandas as pd

def pre_clean(original):
    '''
    This function parse the location column and combine similar columns in the dataframe.
    :param original: dataframe that stores the raw data
    :type original: pd.DataFrame
    '''
    assert isinstance(original, pd.DataFrame)
    
    df = original.drop(columns=['employmenttype_jobstatus', 'jobid', 'shift', 'site_name']).drop('Sum').set_index('uniq_id')
    ids = df.index
    state_list = list()
    city_list = list()
    for index in ids:
        loc = df['joblocation_address'][index]
        if pd.isna(loc):
            df = df.drop(index)
        else:
            loc_split = loc.split(', ')
            if len(loc_split) == 1:
                df = df.drop(index)
            else:
                city = loc.split(', ')[0]
                state = loc.split(', ')[1].upper()
                if len(state) != 2:
                    df = df.drop(index)
                else:
                    state_list.append(state)
                    city_list.append(city)
    df.insert(loc=2, column='city', value=city_list)
    df.insert(loc=3, column='state', value=state_list)
    # df = df.drop(columns=['joblocation_address'])
    df['aws'] += df['amazon web services']
    df['golang'] += df['go lang']
    df = df.drop(columns=['amazon web services', 'go lang'])
    return df