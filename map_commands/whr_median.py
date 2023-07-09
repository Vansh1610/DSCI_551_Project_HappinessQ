import requests as r
import pandas as pd
import random
import io
explain={}
namenode_link='https://happinessq-fc061-default-rtdb.firebaseio.com/Namenode/'
structure_link='https://happinessq-fc061-default-rtdb.firebaseio.com/structure/root/'
datanode_link='https://happinessq-fc061-default-rtdb.firebaseio.com/datanode/'
partition_id_link ='https://happinessq-fc061-default-rtdb.firebaseio.com/'

def getPartitionloc(file_path):
  if file_path[0]=="/":
    file_path=file_path[1:]
  check_path='/'.join(file_path.split('/')[:-1])
  name=file_path.split('/')[-1].replace('.','%')
  if r.get(structure_link+check_path+'/'+name+'/.json').json()==None:
    return "'{}': No such file".format(file_path)
  else:
    values=r.get(namenode_link+name+'/.json').json()
    inode=values['inode']
    part=values['part']
    loc_list=[]
    for i in part:
      loc_list.append(str(inode)+'_'+str(i))
    return loc_list

def cat(file_path,whr_col,country):
  map_ls=[]
  partition_tables=getPartitionloc(file_path)
  explain={}
  if type(partition_tables)==str:
    return partition_tables
  for i in partition_tables:
    total_content=r.get('https://happinessq-fc061-default-rtdb.firebaseio.com/'+i+'/.json').json()+'\n'
    content=total_content.replace('$$$','\n')
    y=pd.read_csv(io.StringIO(content),sep=",",on_bad_lines='skip')
    y=y.drop('Unnamed: 0',axis=1)
    y=y.reset_index().drop('index',axis=1)
    #map_ls.append(map_lowest_10_whr(partition=y,year=2019,whr_col='Happiness_Score'))
    map_ls.append(map_median_score_country(y,whr_col,country))
    
  return map_ls

def map_median_score_country(partition,whr_col,country):
    key_list=[]
    partition=partition[(partition['Country']==country)]
    if partition.shape[0]==0:
        return []
    for i in range(partition.shape[0]):
        key_list.append([partition.iloc[i][whr_col],1])
    if 'map' in explain:
      explain['map'].append(key_list)
    else:
      explain['map']=[key_list]
    return key_list
def reduce_median_score_country(map_ls):
    median_arr=[]
    for val in map_ls:
        for inner_val in val:
            if len(inner_val)==0:
                continue
            median_arr.append(inner_val[0])
        
    sorted(median_arr)
    l=len(median_arr)
    length=int(l/2)
    if l%2!=0:
        explain['reducer']=median_arr[length-1] 
        return median_arr[length-1] 
       
    else:
        explain['reducer']=(median_arr[length]+median_arr[length-1])/2
        return (median_arr[length]+median_arr[length-1])/2
def median_main(file_path,whr_col,country):
    map_ls=cat(file_path,whr_col,country)
    #dict_ls=combiner_lowest_10_whr(map_ls)
    return explain,pd.DataFrame([reduce_median_score_country(map_ls)],columns=['Median value for {} for country {}'.format(whr_col,country)])

