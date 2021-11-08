import pandas as pd
import csv  
import os
from operator import itemgetter
import re

df = pd.read_stata('ai_model_predictions.dta')
pd.to_datetime(df['pub_dt'],format="%Y-%m-%d",errors='ignore')
df[['year','month','day']]=df['pub_dt'].str.split('-',expand=True)
df['day']=pd.to_numeric(df['day'], errors='coerce')
df['month']=pd.to_numeric(df['month'], errors='coerce')
df['year']=pd.to_numeric(df['year'], errors='coerce')
df.dropna(subset=['year','month','day'])
filtered_data_df = df.loc[df['year'] >=2010]


# Pre-Grant Publication (PGPub) --> Patent flag: 1 for patent, 0 for PGPub
filtered_flag_df = filtered_data_df.loc[df['flag_patent'] ==1]

# Filter only AI
filtered_ai_df = filtered_flag_df.loc[df['predict50_any_ai'] ==1]

# Correct document id
filtered_ai_df['doc_id'] = "US"+filtered_ai_df['doc_id']

# A value is trying to be set on a copy of a slice from a DataFrame.
# Try using .loc[row_indexer,col_indexer] = value instead
# See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy

# Save file
filtered_ai_df[['doc_id','pub_dt','appl_id']].to_csv('../get_abstracts/filtered_ai_documents.csv', index=False)
