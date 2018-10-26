import http.client, json, csv, math, datetime

endpoint = 'experiments?page=1&per_page=100&project_id=10561433763'

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
    for exp in json_data:
        curr_exp = exp['key']
        if curr_exp == exp_key:
            return exp['id']

# returns control group id as int, based on experiment name and control name 
def get_control_id(exp_key, control_name):
    variants = get_variants(exp_key)
    if control_name in variants:
        print(variants[control_name])
        return variants[control_name]
    else:
        print('no control group named ' + control_name + ' exists for this experiment')
        return 'undefined'

# returns variant id's as a list, based on experiment name and control name
def get_variant_ids(exp_key, control_name):
    variants = get_variants(exp_key)
    var_list = []
    for v in variants:
        if v != control_name:
            var_list.append(variants[v])
    print(var_list)
    return var_list

# returns variant names as a list, based on experiment name and control name
def get_variant_names(exp_key, control_name):
    variants = get_variants(exp_key)
    var_list = []
    for v in variants:
        if v != control_name:
            var_list.append(v)
    print(var_list)
    return var_list

def get_data(endpoint):
    conn = http.client.HTTPSConnection("api.optimizely.com")
    payload = "{}"
    headers = {'Authorization':'Bearer 2:ayle4zlejAQMYZPxDAVPwRmIGzga8n-ytxYzDpyGuDiyx7s5Qrp0'}
    conn.request("GET", '/v2/'+endpoint, payload, headers)
    getres = conn.getresponse()
    data = getres.read().decode('utf-8')
    json_response = json.loads(data)
    return json_response

if __name__ == '__main__':
    #get_experiment('no-defaults')
    #get_variants('no-defaults')
    #get_control_id('no-defaults', 'control')
    #get_variant_ids('no-defaults', 'control')
    get_variant_names('no-defaults', 'control')
