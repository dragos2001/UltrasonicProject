# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 09:04:55 2025

@author: BRD5CLJ
"""
import sys    
print( "In module products sys.path:" , sys.path )
print("Package and name __package__,__name__ ==",  __package__,"and ",__name__,"end")
import pandas as pd
import matplotlib.pyplot as plt
from ..utils.utils import FileHandler



if __name__=="__main__":
    print("hello")