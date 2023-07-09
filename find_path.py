import requests as r


namenode_link='https://happinessq-fc061-default-rtdb.firebaseio.com/Namenode/'
structure_link='https://happinessq-fc061-default-rtdb.firebaseio.com/structure/root/'
partition_id_link ='https://happinessq-fc061-default-rtdb.firebaseio.com/'


def find_key_path(data, target_key, current_path=''):
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f'{current_path}/{key}' if current_path else key
            if key == target_key:
                return new_path
            result = find_key_path(value, target_key, new_path)
            if result:
                return result
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f'{current_path}/{i}' if current_path else str(i)
            result = find_key_path(item, target_key, new_path)
            if result:
                return result
    return None

def get_path():
    paths={}
    data=r.get(structure_link+'/.json').json()

    if find_key_path(data,'whr%csv') is not None:
        paths['whr']={'name':'World Happiness Report','path':'/'+find_key_path(data,'whr%csv').replace('%','.')}
    if find_key_path(data,'unemployment-2020%csv') is not None:
        paths['unemp']={'name':'Unemployment','path':'/'+find_key_path(data,'unemployment-2020%csv').replace('%','.')}

    if find_key_path(data,'GDP_updated%csv') is not None:
        paths['GDP']={'name':'GDP','path':'/'+find_key_path(data,'GDP_updated%csv').replace('%','.')}
    
    return paths





