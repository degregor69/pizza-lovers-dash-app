import pandas as pd
import numpy as np 

def create_last_50_df():
    df = pd.read_csv("inputs_from_processing/comments_cleaned.csv", sep='|')
    df_2 = pd.read_csv("inputs_from_processing/basic_data_cleaned.csv", sep='|', index_col=[0])
    df_merge = df.groupby(['name', 'address'])['comment_rate'].mean().round(2).to_frame()
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

def show_repartition(str):
    a = last_50_better_analysis()
    return int((round(a[str])/a.sum()*100))

def top_20_by_average_rate():
    df = create_last_50_df()
    df =  df.drop(['postal_code', 'city', 'average_rate'], axis=1)
    df = df[df['nb_of_reviews']>100]
    return df[['name', 'comment_rate', 'address']].sort_values(by='comment_rate', ascending = False).head(20)

def top_5_district_by_comment_rate(df):
    return df.groupby(['postal_code'])['comment_rate'].mean().nlargest(5)