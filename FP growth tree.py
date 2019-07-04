import numpy as np
import pandas as pd
import time

class treeNode:
    def __init__(self, name, num, parentnode):
        self.name = name
        self.count = num
        self.parent = parentnode
        self.children = {}
        self.nodeLink = None


    def counters(self, num):
        self.count += num

def create(D, minSup):

    table = {}
    for i in D:
        for j in i:
            table[j] = table.get(j, 0) + D[i]

    for k in list(table.keys()):
        if table[k] < minSup:
            del (table[k])

    freq = set(table.keys())
    if len(freq) == 0:
        return None, None
    for k in table:
        table[k] = [table[k], None]
    head = treeNode('null', 1, None)
    for key, count in D.items():
        l = {}
        for item in key:
            if item in freq:
                l[item] = table[item][0]
        if len(l) > 0:
            order = [v[0] for v in sorted(l.items(), key=lambda p: p[1], reverse=True)]
            new(order, head, table, count)
    return head, table


def new(items, tree, table, count):
    if items[0] in tree.children:
        tree.children[items[0]].counters(count)

    else:
        tree.children[items[0]] = treeNode(items[0], count, tree)

        if table[items[0]][1] == None:
            table[items[0]][1] = tree.children[items[0]]
        else:
            newhead(table[items[0]][1], tree.children[items[0]])

    if len(items) > 1:
        new(items[1::], tree.children[items[0]], table, count)

def newhead(node, target):
    while (node.nodeLink != None):
        node = node.nodeLink
    node.nodeLink = target

def buildset(D):
    retDict = {}
    for trans in D:
        retDict[frozenset(trans)] = 1
    return retDict


def getpath(base, node):
    re = {}
    while node != None:
        tmp = []
        backtrap(node, tmp)
        if len(tmp) > 1:
            re[frozenset(tmp[1:])] = node.count
        node = node.nodeLink

    return re



def backtrap(node, path):
    if node.parent != None:
        path.append(node.name)
        backtrap(node.parent, path)


def mine(tree, table, minSup, path, freq):
    bigL = [v[0] for v in sorted(table.items(), key=lambda p: p[1])]
    for base in bigL:
        newfreq = path.copy()
        newfreq.add(base)
        freq.append(newfreq)
        pathbase = getpath(base, table[base][1])
        newtree, newhead =create(pathbase, minSup)

        if newhead != None:
            mine(newtree, newhead, minSup, newfreq, freq)



def fp(D, minSup):
    start=time.time()
    firstset = buildset(D)
    newtree, newhead = create(firstset, minSup)
    freq = []
    mine(newtree, newhead, minSup, set([]), freq)
    re=[]
    for i in freq:
        for j in i:
            re.append(j)
    end=time.time()
    print(end-start)
    return len(re),re

lst = pd.read_csv("D:\PPT\DM\hmwk\\newdata.csv", header=None)
ls = np.array(lst)
lstt = ls.tolist()
print(fp(lstt,0.23*len(lstt)))