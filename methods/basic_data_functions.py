import pandas as pd
import numpy as np 

def basic_data_df():
    df = pd.read_csv('inputs_from_exterior/basic_data.csv', delimiter = '|')
    new_df = pd.read_csv('inputs_from_exterior/basic_data_75020_75007.csv', delimiter = '|')
    df = pd.concat([df, new_df])
    df.reset_index(drop=True, inplace=True)
    return df

def clean_basic_data_df(df):
    df = df.drop_duplicates(subset=['name', 'address'], keep='last')

    # Examine the address of the restaurant that has no city in the address
    df[df['name'].str.contains('CAMPISI')]
    df.at[369, 'address'] = 'Angle rue de Boulanvilliers, 1 Rue des Bauches, 75016 Paris'

    # Keep all the restaurants that have Paris in their address
    df = df[df['address'].str.contains('Paris')]
    
    # Average rate to numeric type
    df['average_rate'] = df['average_rate'].str.replace(',','.')
    df['average_rate'] = pd.to_numeric(df['average_rate'])
    return df

def create_city_and_postal_code_columns(df):
    # Split the column and transform it into Series
    splitted_series = df.address.str.split(expand=False)

    list_of_cities = []
    # create a list of the cities
    for city in splitted_series:
        list_of_cities.append(city[-1])
        
    df['city'] = list_of_cities

    splitted_series = df.address.str.split(expand=False)

    list_of_postal_code = []
    for string in splitted_series:
        list_of_postal_code.append(string[-2])
        
    df['postal_code'] = list_of_postal_code

    # Modification of the 75116 by 75016
    df['postal_code'] = df['postal_code'].replace('75116', '75016')
    return df

def df_graph_top_5_by_rating(df, district_number):
    return df[df.postal_code == district_number].sort_values(by=['average_rate'], ascending=False).head(5)

def df_graph_top_5_by_nb_reviews(df, district_number):
    return df[df.postal_code == district_number].sort_values(by=['nb_of_reviews'], ascending=False).head(5)

def top_5_district_by_average_rate(df):
    return df.groupby(['postal_code'])['average_rate'].mean().nlargest(5)

def top_5_district_by_nb_reviews(df):
    return df.groupby(['postal_code'])['nb_of_reviews'].mean().nlargest(5)

def top_8_by_nb(df):
    return df.groupby(['postal_code'])['name'].count().nlargest(8)

def top_20_by_average_rate(df):
    df =  df.drop(['postal_code', 'city'], axis=1)
    return df[['name', 'average_rate', 'address']][df['nb_of_reviews'] > 100].sort_values(by='average_rate', ascending = False).head(20)

def nb_pizzerias():
    return len(clean_basic_data_df(basic_data_df()))

def average_rate_pizzerias():
    df = clean_basic_data_df(basic_data_df())
    return round(df['average_rate'].mean(),2)