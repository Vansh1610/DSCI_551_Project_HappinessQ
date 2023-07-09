import requests as r
import pandas as pd
import random
import io
import numpy as np
from itertools import chain
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

def cat(file_path,country,subject):
  map_ls=[]
  partition_tables=getPartitionloc(file_path)
  explain.clear()
  if type(partition_tables)==str:
    return partition_tables
  for i in partition_tables:
    total_content=r.get('https://happinessq-fc061-default-rtdb.firebaseio.com/'+i+'/.json').json()+'\n'
    content=total_content.replace('$$$','\n')
    y=pd.read_csv(io.StringIO(content),sep=",",on_bad_lines='skip')
    y=y.drop('Unnamed: 0',axis=1)
    y=y.reset_index().drop('index',axis=1)
    map_ls.append(max_month_country_subject(partition=y,country=country,subject=subject))
  return map_ls

def max_month_country_subject(partition,country,subject):
    key_list=[]
    partition=partition[(partition['LOCATION']==country) & (partition['SUBJECT']==subject) ]
    
    top_df=partition.sort_values(by=['Value'],ascending=False)
    #print(top_df)
    if top_df.shape[0]==0:
        if 'map' in explain:
            explain['map'].append([[]])
        else:
            explain['map']=[[]]
        return []
    key_list.append([top_df.iloc[0]['Value'],top_df.iloc[0]['MONTH']])
    if 'map' in explain:
      explain['map'].append([key_list,1])
    else:
      explain['map']=[[key_list,1]]
    return [key_list,1]


def reduce_max_month_country_subject(map_list):
    max_val=0
    #print(map_list)
    for val in map_list:
        print(val)
        if(len(val)==0):
                continue
        for innerval in val[0]:    
            if innerval[0]>max_val:
                max_val=innerval[0]
                max_month=innerval[1]
    if max_val==0:
      max_month=None
      max_val= None
      explain['reducer']='Sorry no information available for above combination'
    else:
      explain['reducer']=[max_val,max_month]
    return [max_val,max_month]
        
def max_main(file_path,country,subject):
    
    map_ls=cat(file_path,country,subject)
    month_map={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    v,m=reduce_max_month_country_subject(map_ls)
    if v is None or m is None:
      return explain,pd.DataFrame([['','']],columns=['Maximum Unemployent Value','Month for maximum value for gender {} for country {}'.format(subject,country)])
    m=month_map[m]
    return explain,pd.DataFrame([[v,m]],columns=['Maximum Unemployent Value','Month for maximum value for gender {} for country {}'.format(subject,country)])