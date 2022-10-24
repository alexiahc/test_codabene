#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 13:25:51 2022

@author: Alexia Huc-Lhuillery
Technical Test - JUNIOR DATA ENGINEER
"""

import pandas as pd

# Directory where the csv files are located 
rep = ""

df_app = pd.read_table(rep+"references initialized in shop.csv", delimiter=';')
df_shop = pd.read_table(rep+"retailer extract.csv", delimiter=';')

#%% Task 1

# Verification that all products are food
# df_shop['Libellé  Groupe de Famille '].unique()

# Recovery of products really present in the store 
df_shop_en_rayon = df_shop[df_shop['Date déréf.'].isnull()]
df_shop_en_rayon = df_shop_en_rayon[df_shop_en_rayon['Date Deb Cad.'].notnull()]

# The products with null or negative stock quantity are considered as not present 
df_shop_en_rayon['Stock en quantité'] = pd.to_numeric(df_shop_en_rayon['Stock en quantité'], errors='coerce')
df_shop_en_rayon = df_shop_en_rayon[df_shop_en_rayon['Stock en quantité'] > 0]

# We are looking for a correspondence between reference_id and EAN
# len(set(df_app['reference_id']).intersection(set(df_shop['EAN']))) # 3081
# len(list(set(df_app['reference_id']) & set(df_shop_en_rayon['EAN']))) # 2598
# df_shop['EAN'].nunique() # 39136
# df_app['reference_id'].nunique() # 5902

# We will assume that reference_id corresponds to the EAN of the product, 
# because almost half of the EAN that can be found for the products on the 
# shelf are in the application data in the reference_id column, and some 
# products in the application are more than 30 years out of date so will not 
# correspond to products currently in the store

# Calculation of untracked references 
df_ref_not_tracked = df_shop_en_rayon.loc[~df_shop_en_rayon['EAN'].isin(df_app['reference_id'])]
nb_ref_not_tracked = df_ref_not_tracked.shape[0]

print()
print("Total number of references not tracked in the app but present in the shop assortment :")
print(nb_ref_not_tracked)
print()

#%% Task 2 

df_ref_tracked = df_shop_en_rayon.loc[df_shop_en_rayon['EAN'].isin(df_app['reference_id'])]
list_lib_ssfam = df_ref_tracked['Libellé  Sous-Famille '].drop_duplicates()
df_ref_relevant = df_ref_not_tracked[df_ref_not_tracked['Libellé  Sous-Famille '].isin(list_lib_ssfam)]

print("List of products which are not tracked by the app, but are relevant :")
print()
print(df_ref_relevant[['EAN', 'Article Libellé Long']])
print() 

# Many frozen foods have been added to the list because a frozen food is 
# present in the application data, but they may not be very interesting 
# products to track

#%% Task 3 

print("Total size of the list of relevant but not tracked products :")
print(df_ref_relevant.shape[0])
print()

#%% Task 4 

# This function will be used on each row of the relevant product dataset to 
# find an aisle that matches 
# We are looking for the most present aisle for items that have the same 
# Libellé Sous-Famille label as our current product

def find_aisle(l):
    lib_ss_fam = l['Libellé  Sous-Famille ']
    ref_tracked_ss_fam = df_ref_tracked.loc[df_ref_tracked['Libellé  Sous-Famille '] == lib_ss_fam, :]
    ref_tracked_ss_fam = ref_tracked_ss_fam.merge(df_app, left_on='EAN', right_on='reference_id')
    return ref_tracked_ss_fam['allee'].value_counts().index[0]

df_ref_relevant['Proposition d\'allée'] = df_ref_relevant.apply(find_aisle, axis=1)

print("Suggestion of an aisle where the reference could be found by the user :")
print()
print(df_ref_relevant[['EAN', 'Article Libellé Long', 'Proposition d\'allée']])
print() 

# All frozen foods have the same aisle proposal because the feature I'm 
# proposing here is based on the products that are already in the app and 
# their current aisle, and there is only one frozen food in the app, but surely 
# not all products will match this aisle which is Halal & Casher 




