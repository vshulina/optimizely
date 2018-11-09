import http.client, json
import os
import pandas as pd

# do not change
endpoint = 'experiments?page=1&per_page=100&project_id=10561433763'

######## VARIABLES TO BE CHANGED FOR EVERY EXPERIMENT ########

# experiment name (or key) as it appears in Optimizely
opt_exp_name = 'no-defaults'
# control group as it is called in Optimizely
control_name = 'control'

start_date = '2018-10-01'
end_date = '2018-11-06'

# output file name
output_name = 'VAS_No-Defaults'

# main working directory - where you want your CSV file saved
main_dir = '/Users/viktoriya.shulina/Documents/Optimizely/Output/'

# data directory - where you extracted Optimizely files from the S3 bucket. Do not remove the r in the beginning
data_dir = r"/Users/viktoriya.shulina/Documents/Optimizely/Data/"
######## END OF VARIABLES THAT NEED TO BE CHANGED ########

### functions for getting experiment and variant id's from Optimizely API ###
# returns experiment variations as a dictionary where key is variation name, value is variant id
def get_variants(exp_key):
    json_data = get_data(endpoint)
    variants = {}
    for exp in json_data:
        curr_exp = exp['key']
        if curr_exp == exp_key:
            for var in exp['variations']:
                variants[var['key']] = var['variation_id']
    return variants

# returns experiment id as int, based on experiment key provided
def get_experiment(exp_key):
    json_data = get_data(endpoint)
    print('Retreiving experiment id...')
    for exp in json_data:
        curr_exp = exp['key']
        if curr_exp == exp_key:
            return exp['id']

# connects to Optimizely API and returns response in JSON format
def get_data(endpoint):
    conn = http.client.HTTPSConnection("api.optimizely.com")
    payload = "{}"
    headers = {'Authorization':'Bearer 2:ayle4zlejAQMYZPxDAVPwRmIGzga8n-ytxYzDpyGuDiyx7s5Qrp0'}
    print('Downloading Optimizely data...')
    conn.request("GET", '/v2/'+endpoint, payload, headers)
    getres = conn.getresponse()
    data = getres.read().decode('utf-8')
    json_response = json.loads(data)
    return json_response

# returns control group id as int, based on experiment name and control name 
def get_control_id(exp_key, control_name):
    variants = get_variants(exp_key)
    print('Getting control id...')
    if control_name in variants:
        return variants[control_name]
    else:
        print('no control group named ' + control_name + ' exists for this experiment')
        return 'undefined'

# returns variant id's as a list, based on experiment name and control name
def get_variant_ids(exp_key, control_name):
    variants = get_variants(exp_key)
    var_list = []
    print('Getting variant id...')
    for v in variants:
        if v != control_name:
            var_list.append(variants[v])
    return var_list

# returns variant names as a list, based on experiment name and control name
def get_variant_names(exp_key, control_name):
    variants = get_variants(exp_key)
    var_list = []
    print('Getting variant names...')
    for v in variants:
        if v != control_name:
            var_list.append(v)
    return var_list   
### END functions for getting experiment and variant id's from Optimizely API ###
    
# downloads files from Optimizely S3 bucket
#def download_data():
    

## still need to change definition of HF week later

control_var_id = get_control_id(opt_exp_name, control_name)
var_experiment_id = get_experiment(opt_exp_name)
test_var_id = get_variant_ids(opt_exp_name, control_name)
test_var_name = get_variant_names(opt_exp_name, control_name)
var_i = len(test_var_id)

#########%%############
def create_file():

    os.chdir(main_dir)  
    
    file_pathes = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".gz"):
                path = os.path.join(root, file)
                print(path)
                file_pathes.append(path)
    
    df = pd.read_csv(file_pathes[0], compression='gzip',sep='\t')
    
    for file_path in file_pathes[1:]:
        new_df = pd.read_csv(file_path, compression='gzip',sep='\t')
        df = pd.concat([df, new_df])
    
    timestamps = df['timestamp'] 
    
    df['time_stamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    #select experiment ID
    
    filtered_data = df[(df.experiment_id == var_experiment_id) & 
                       (df.time_stamp >= start_date) & 
                       (df.time_stamp <= end_date) &
                       (pd.isnull(df.event_type)) &
                       (pd.isull(df.event_name))]
    
    #get the list by experiment 
    variation = filtered_data.groupby(['experiment_id','variation_id', 'end_user_id']) ['time_stamp'].agg(['min','max']).reset_index()
    variation.rename(columns = {'end_user_id':'customer_id'}, inplace = True)
    variation['ranking'] = variation.groupby(by = 'customer_id')['min'].rank(method = 'min')
    variation = variation[variation.ranking == 1]   
    
    #turn the columns to what we want
    variation.loc[variation.variation_id == control_var_id, 'ab_group'] = 'Control'
    
    for i in range(var_i):
    	variation.loc[variation.variation_id == test_var_id[i], 'ab_group'] = test_var_name[i]    
    
    variation.groupby(by = 'ab_group').apply(lambda x: x.customer_id.nunique())
    
    variation[['customer_id', 'ab_group']].to_csv((main_dir+output_name+'.csv'), index = None)
    
    print('Customer list created')

if __name__ == '__main__':
    #create_file()
    print(get_experiment('no-defaults'))

#%%

# for generating csvs for AB Testing Tool:

# variation.loc[np.logical_and(variation['min'].dt.date >= datetime.date(2018,9,10), variation['min'].dt.date <= datetime.date(2018,9,14)), 'start_week'] = '2018-W37'
# variation.loc[np.logical_and(variation['min'].dt.date >= datetime.date(2018,9,15), variation['min'].dt.date <= datetime.date(2018,9,21)), 'start_week'] = '2018-W38'
# variation.loc[np.logical_and(variation['min'].dt.date >= datetime.date(2018,9,22), variation['min'].dt.date <= datetime.date(2018,9,28)), 'start_week'] = '2018-W39'
# variation.loc[np.logical_and(variation['min'].dt.date >= datetime.date(2018,9,29), variation['min'].dt.date <= datetime.date(2018,10,5)), 'start_week'] = '2018-W40'
# variation.loc[np.logical_and(variation['min'].dt.date >= datetime.date(2018,10,6), variation['min'].dt.date <= datetime.date(2018,10,12)), 'start_week'] = '2018-W41'
# variation.loc[np.logical_and(variation['min'].dt.date >= datetime.date(2018,10,13), variation['min'].dt.date <= datetime.date(2018,10,19)), 'start_week'] = '2018-W42'
# variation.loc[:,'country'] = 'US'
# variation.loc[:,'end_week'] = var_end_week

#%%
# for i in range(var_i):
#     output = variation.loc[np.logical_or(variation.ab_group == 'Control', variation.ab_group == test_var_name[i]),['ab_group', 'country', 'customer_id', 'start_week', 'end_week']]
#     output.loc[output.ab_group == test_var_name[i], 'ab_group'] = 'Test'
#     if var_i> 1:
#         output.loc[:, 'experiment'] = output_name + "_" + test_var_name[i]
#     else:
#         output.loc[:, 'experiment'] = output_name
#     output[['experiment', 'ab_group', 'country', 'customer_id', 'start_week', 'end_week']].to_csv((os.getcwd()+'/Output/'+output_name + "_" + test_var_name[i]+'.csv'), index = None)

#%%
