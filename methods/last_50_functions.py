import pandas as pd
import numpy as np 

def create_last_50_df():
    df = pd.read_csv("inputs_from_processing/comments_cleaned.csv", sep='|')
    df_2 = pd.read_csv("inputs_from_processing/basic_data_cleaned.csv", sep='|', index_col=[0])
    df_merge = df.groupby(['name', 'address'])['comment_rate'].mean().to_frame()
    df_3 = df_2.merge(df_merge['comment_rate'], how='left', on=['name', 'address'])
    return df_3

def create_last_50_boolean_column():
    df = create_last_50_df()
    df['last_50_better?'] = np.where(df['comment_rate'] == df['average_rate'], "Equal", np.where(df['comment_rate'] >= df['average_rate'], "Better", "Worse"))
    return df

def last_50_better_analysis():
    df = create_last_50_boolean_column()
    return df.groupby(['last_50_better?'])['last_50_better?'].count()

def have_changed_share():
    a = last_50_better_analysis()
    return int(round((a.sum()-a['Equal'])/a.sum() * 100,0))