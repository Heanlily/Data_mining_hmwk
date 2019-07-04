# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 09:59:16 2018

@author: Lilylove Huang
"""
import numpy as np
import pandas as pd
import time


def findc1(D):
    can1 = {}
    for k in D:
        for i in k:
            if i in can1:
                can1[i] += 1
            else:
                can1[i] = 1
    a = can1.keys()
    C1 = []
    for i in a:
        C1.append([i])
    return list(map(frozenset, C1))

def counters(D, itemset, minSupport):
    num = {}
    for i in D:
        for j in itemset:
            if j.issubset(i):
                if not j in num:
                    num[j] = 1
                else:
                    num[j] += 1
    length = float(len(D))
    re = []

    for i in num:
        support = num[i] / length
        if support >= minSupport:
            re.append(i)

    return re


def generate(Lk, k):
    res = []
    leng = len(Lk)
    for i in range(leng):
        for j in range(i + 1, leng):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            if L1 == L2:
                res.append(Lk[i] | Lk[j])
    return res


def apriori(D, minSupport=0.23):
    C1 = findc1(D)
    D = list(map(set, D))
    L1 = counters(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = generate(L[k - 2], k)
        Lk= counters(D, Ck, minSupport)
        L.append(Lk)
        k += 1

    return L

def calculate(lstt):
    start=time.time()
    leng=len(lstt)
    a = apriori(lstt)
    res = []
    for i in a:
        for j in i:
            res.append(j)
    res = list(set(res))
    num_support={}
    for i in res:
        for j in lstt:
            if i.issubset(j):
                if i in num_support:
                    num_support[i]+=1/leng
                else:
                    num_support[i]= 1/leng

    end = time.time()
    print("Run time is:", end - start)
    return num_support,len(res)

lst = pd.read_csv("D:\PPT\DM\hmwk\\newdata.csv", header=None)
ls = np.array(lst)
lstt = ls.tolist()
print(calculate(lstt))

