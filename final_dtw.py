from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np
import pandas as pd
import os
import math
import random
def dtw_correlation_with_cluster(data,relative_time,sensing,EMA,sensing_cluster,EMA_cluster):
    data1 = data.dropna(subset=[EMA_cluster],axis=0)
    data1 = data.dropna(subset=[sensing_cluster],axis=0)
    EMA_data = data1.dropna(subset=[EMA],axis=0)
    sensing_data = data1.dropna(subset=[EMA],axis=0)
    correaltion_matrix=pd.DataFrame(columns=list(set(EMA_data[EMA_cluster])),index=list(set(sensing_data[sensing_cluster])))
    for u in list(set(sensing_data[sensing_cluster])):
        subset = sensing_data[sensing_data[sensing_cluster] == u]
        list1 = list(subset[relative_time])
        list2 = list(subset[EMA])
        listx = []
        for w in range(len(list1)):
            listx.append([float(list1[w]),float(list2[w])])
        x = np.array(listx)
        for v in list(set(EMA_data[EMA_cluster])):
            if pd.isnull(v):
                continue
            subset = EMA_data[EMA_data[EMA_cluster] == v]
            list1 = list(subset[relative_time])
            list2 = list(subset[EMA])
            listx = []
            for w in range(len(list1)):
                listx.append([float(list1[w]),float(list2[w])])
            y = np.array(listx)
            distance, path = fastdtw(x,y,dist = euclidean)
            correaltion_matrix.loc[u,v] = distance
    # indicates the distance bwtween EMA data of each clusters
    
    EMA_data = data.dropna(subset=[EMA],axis=0)
    EMA_data = EMA_data.dropna(subset=[EMA_cluster],axis=0)
    sensing_data = data.dropna(subset=[sensing],axis=0)
    sensing_data = sensing_data.dropna(subset=[sensing_cluster],axis=0)
    correlation_matrix=pd.DataFrame(columns=list(set(EMA_data[EMA_cluster])),index=list(set(sensing_data[sensing_cluster])))
    for u in list(set(sensing_data[sensing_cluster])):
        subset = sensing_data[sensing_data[sensing_cluster] == u]
        list1 = list(subset[relative_time])
        list2 = list(subset[sensing])
        listx = []
        for w in range(len(list1)):
            listx.append([float(list1[w]),float(list2[w])])
        x = np.array(listx)
        for v in list(set(EMA_data[EMA_cluster])):
            if pd.isnull(v):
                continue
            subset = EMA_data[EMA_data[EMA_cluster] == v]
            list1 = list(subset[relative_time])
            list2 = list(subset[EMA])
            listx = []
            for w in range(len(list1)):
                listx.append([float(list1[w]),float(list2[w])])
            y = np.array(listx)
            distance, path = fastdtw(x,y,dist = euclidean)
            correlation_matrix.loc[u,v] = distance
    return [correaltion_matrix,correlation_matrix]


def dtw_correlation_with_cluster2(data,relative_time,sensing,EMA,sensing_cluster,EMA_cluster):
    EMA_list = list(set(data[EMA_cluster]))
    EMA_list = sorted([x for x in EMA_list if math.isnan(x) == False])
    sensing_list = list(set(data[sensing_cluster]))
    sensing_list = sorted([x for x in sensing_list if math.isnan(x) == False])
    correlation_matrix=pd.DataFrame(0,columns=EMA_list,index=sensing_list)
    for u in sensing_list:
        if pd.isnull(u):
            continue
        for v in EMA_list:
            if pd.isnull(v):
                continue
            subset = data[data[EMA_cluster] == v]
            subset = subset[subset[sensing_cluster] == u]
            uid = list(set(list(subset['uid'])))
            EMA_data = data.dropna(subset=[EMA],axis=0)
            sensing_data = data.dropna(subset=[sensing],axis=0)
            divider = 0
            if uid != []:
                for w in uid:
                    uid_EMA = EMA_data[EMA_data['uid'] == w]
                    uid_sensing = sensing_data[sensing_data['uid'] == w]
                    list1 = list(uid_EMA[relative_time])
                    list2 = list(uid_EMA[EMA])
                    listx = []
                    for x in range(len(list1)):
                        listx.append([float(list1[x]),float(list2[x])])
                    x = np.array(listx)
                    list1 = list(uid_sensing[relative_time])
                    list2 = list(uid_sensing[sensing])
                    listx = []
                    for y in range(len(list1)):
                        listx.append([float(list1[y]),float(list2[y])])
                    y = np.array(listx)
                    if len(uid_EMA) > 10 and len(uid_sensing) > 10:
                        distance, path = fastdtw(x,y,dist = euclidean)
                        correlation_matrix.loc[u,v] = correlation_matrix.loc[u,v] + distance/len(uid_EMA)/len(uid_sensing)
                        divider = divider +1
                correlation_matrix.loc[u,v] = correlation_matrix.loc[u,v]/divider
    return correlation_matrix



def dtw_correlation_with_background(data,relative_time,sensing,EMA,sensing_cluster,EMA_cluster):
    EMA_data = data.dropna(subset=[EMA_cluster],axis=0)
    sensing_data = data.dropna(subset=[sensing_cluster],axis=0)
    list1 = list(EMA_data[EMA_cluster])
    print(list1)
    random.shuffle(list1)
    EMA_data[EMA_cluster] = list1
    list1 = list(sensing_data[sensing_cluster])
    print(list1)
    random.shuffle(list1)
    sensing_data[sensing_cluster] = list1
    EMA_data = EMA_data[['uid','day', 'relative time', EMA, 'EMA_cluster']]
    sensing_data = sensing_data[['uid','day', 'relative time', sensing, 'sensing_cluster']]
    data = pd.merge(sensing_data,EMA_data,on=['uid','day', 'relative time'], how = 'outer')
    EMA_list = list(set(data[EMA_cluster]))
    EMA_list = sorted([x for x in EMA_list if math.isnan(x) == False])
    sensing_list = list(set(data[sensing_cluster]))
    sensing_list = sorted([x for x in sensing_list if math.isnan(x) == False])
    correlation_matrix=pd.DataFrame(0,columns=EMA_list,index=sensing_list)
    for u in sensing_list:
        if pd.isnull(u):
            continue
        for v in EMA_list:
            if pd.isnull(v):
                continue
            subset = data[data[EMA_cluster] == v]
            subset = subset[subset[sensing_cluster] == u]
            uid = list(set(list(subset['uid'])))
            EMA_data = data.dropna(subset=[EMA],axis=0)
            sensing_data = data.dropna(subset=[sensing],axis=0)
            divider = 0
            if uid != []:
                for w in uid:
                    uid_EMA = EMA_data[EMA_data['uid'] == w]
                    uid_sensing = sensing_data[sensing_data['uid'] == w]
                    list1 = list(uid_EMA[relative_time])
                    list2 = list(uid_EMA[EMA])
                    listx = []
                    for x in range(len(list1)):
                        listx.append([float(list1[x]),float(list2[x])])
                    x = np.array(listx)
                    list1 = list(uid_sensing[relative_time])
                    list2 = list(uid_sensing[sensing])
                    listx = []
                    for y in range(len(list1)):
                        listx.append([float(list1[y]),float(list2[y])])
                    y = np.array(listx)
                    if len(uid_EMA) > 10 and len(uid_sensing) > 10:
                        distance, path = fastdtw(x,y,dist = euclidean)
                        correlation_matrix.loc[u,v] = correlation_matrix.loc[u,v] + distance/len(uid_EMA)/len(uid_sensing)
                        divider = divider +1
                correlation_matrix.loc[u,v] = correlation_matrix.loc[u,v]/divider
    return correlation_matrix