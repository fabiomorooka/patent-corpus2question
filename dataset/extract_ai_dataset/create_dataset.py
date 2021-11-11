#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd

from utils import file_handling as file

def generate_dataset():
    header = ['doc_id','pub_dt','appl_id','predict50_any_ai','ai_score_ml', 'predict50_ml', 'ai_score_evo', 'predict50_evo', 'ai_score_nlp', 'predict50_nlp', 'ai_score_speech', 'predict50_speech', 'ai_score_vision', 'predict50_vision', 'ai_score_kr', 'predict50_kr', 'ai_score_planning', 'predict50_planning', 'ai_score_hardware', 'predict50_hardware']
    output_filename = "filtered_ai_documents_2.csv"
    file.delete_file(filename=output_filename)
    file.create_file(filename=output_filename, header=header)

    df = pd.read_stata('ai_model_predictions.dta')
    pd.to_datetime(df['pub_dt'],format="%Y-%m-%d",errors='ignore')
    df[['year','month','day']]=df['pub_dt'].str.split('-',expand=True)
    df['day']=pd.to_numeric(df['day'], errors='coerce')
    df['month']=pd.to_numeric(df['month'], errors='coerce')
    df['year']=pd.to_numeric(df['year'], errors='coerce')
    df.dropna(subset=['year','month','day'])
    filtered_data_df = df.loc[(df['year']>=2010)&(df['year']<=2020)]

    # Pre-Grant Publication (PGPub) --> Patent flag: 1 for patent, 0 for PGPub
    filtered_flag_df = filtered_data_df.loc[df['flag_patent'] ==1]

    # Filter only AI
    filtered_ai_df = filtered_flag_df.loc[df['predict50_any_ai'] ==1]

    # Fileter by each AI fields
    df_filtered = df.loc[(df['ai_score_speech']==1)|(df['ai_score_vision']==1)|(df['ai_score_nlp']==1)|(df['ai_score_evo']==1)|(df['ai_score_ml']==1)]

    # Correct document id, since the dataset does not containt the US initials
    filtered_ai_df['doc_id'] = "US"+filtered_ai_df['doc_id']

    df.loc[df['year']>2020].to_csv("wrong_lines.csv", index=False)
    df.to_csv("complete_dataset.csv", index=False)
    df_filtered[header].to_csv("filtered_ai_documents.csv", index=False)
    filtered_ai_df[header].to_csv(output_filename, index=False)

generate_dataset()