#!/usr/bin/env python
#coding: utf-8

import math
from scipy.stats import mode

from Radius_Change import MarkTreeDer
from TreeNodes import AllTreeNodes


def _Fstretch(list):
    m, M = min(list), max(list)
    lmode = mode(list)[0][0]
    scale = max(lmode - m, M - lmode)

    def fstretch(x):
        return int(255/(1+math.exp(-(12./scale)*(x-lmode)))) #logistic

    return fstretch

def is_der_loc_min(node):
    if node.is_root or node.is_leaf:
        return False
    if node.der > node.parent.der:
        return False
    for child in node.children:
        if node.der > child.der:
            return False
    return True

def stretch_type(tree):
    MarkTreeDer(tree)

    all_nodes = AllTreeNodes(tree)
    all_der = [node.der for node in all_nodes]

    fstretch = _Fstretch(all_der)
    for node in all_nodes:
        node.sd_type = node.type 
        node.type = fstretch(node.der)
        node.is_swollen = True if node.der <= 0 else False        
        node.is_der_loc_min = is_der_loc_min(node)


def Stretch_Type(forest):
    map(stretch_type, forest)