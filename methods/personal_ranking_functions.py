import pandas as pd
import numpy as np 

def create_last_50_df():
    df = pd.read_csv("inputs_from_processing/comments_cleaned.csv", sep='|')
    df_2 = pd.read_csv("inputs_from_processing/basic_data_cleaned.csv", sep='|', index_col=[0])
    df_merge = df.groupby(['name', 'address'])['comment_rate'].mean().to_frame()
    df_3 = df_2.merge(df_merge['comment_rate'], how='left', on=['name', 'address'])
    return df_3

def create_personal_ranking_df():

    df = create_last_50_df()
    # Add the quantile columns
    df['decile_rank_average_rate'] = pd.qcut(df['average_rate'],10, labels = False) + 1
    df['decile_rank_nb_of_reviews'] = pd.qcut(df['nb_of_reviews'],4, labels = False) + 1
    df['decile_rank_average_comment_rate'] = pd.qcut(df['comment_rate'],10, labels = False) + 1 
    
    # Decile rank **3 if decile rank > 5
    df.loc[df["decile_rank_average_rate"] > 5, "decile_rank_average_rate"] = df["decile_rank_average_rate"] ** 3
    df.loc[df["decile_rank_average_comment_rate"] > 5, "decile_rank_average_comment_rate"] = df["decile_rank_average_comment_rate"] ** 3 

    # Create the scores columns and their ranks columns
    df['average_score'] = df['decile_rank_average_rate'] * df['decile_rank_nb_of_reviews']
    df['average_score_rank'] = df['average_score'].rank(method='min', ascending=False)
    df['last_score'] = df['decile_rank_average_comment_rate'] * df['decile_rank_nb_of_reviews']
    df['last_score_rank'] = df['last_score'].rank(method='min', ascending=False)
    return df

def personal_ranking_df_sorted_by_dynamic_rank():
    return create_personal_ranking_df().sort_values(by=['last_score'])

def top_x_personal_ranking(x):
    return personal_ranking_df_sorted_by_dynamic_rank().head(x)

def add_long_lat_to_df():
    df = top_x_personal_ranking(20)
    list_of_long = []
    list_of_lat = []

    for point in df['point']:
        sub_str  = point.replace('(','').replace('(','')
        list_of_long.append(sub_str.split(',')[0])
        list_of_lat.append(sub_str.split(',')[1])


    df['long'] = list_of_long
    df['lat'] = list_of_lat

    df['long'] = pd.to_numeric(df['long'])
    df['lat'] = pd.to_numeric(df['lat'])

    return df

