import pandas as pd
import numpy as np
import methods
from visuals import plot_




def clean_dataset(df):
    """Cleans the dataset"""
    df["Easy Apply"] = df["Easy Apply"].apply(lambda x : methods.convert_Column_Value_to_Bool(x))
    methods.replace_to_nan(df)
    df['Company Name'] = df['Company Name'].str.replace('\n.*', ' ',regex=True)
    #clean job title
    df["Job Title"] = df["Job Title"].str.replace(" â","")
    df["Job Title"] = df["Job Title"].str.replace("/","|")
    #clean revenue column
    df["Revenue"] = df["Revenue"].replace("Unknown / Non-Applicable",np.nan)
    df['Revenue'] = df['Revenue'].str.replace('$', ' ',regex=True)
    df['Revenue'] = df['Revenue'].str.replace('(USD)', ' ',regex=True)
    df['Revenue'] = df['Revenue'].str.replace('(', ' ',regex=True)
    df['Revenue'] = df['Revenue'].str.replace(')', ' ',regex=True)
    df['Revenue'] = df['Revenue'].str.replace(' ', '',regex=True)
    df['Revenue'] = df['Revenue'].str.replace('+', '',regex=True)
    df['Revenue'] = df['Revenue'].str.replace('2to5billion', '2billionto5billion')
    df['Revenue'] = df['Revenue'].str.replace('5to10billion ', '5billionto10billion')
    df['Revenue'] = df['Revenue'].replace('million', ' ')
    df['Revenue'] = df['Revenue'].replace('10billion', '10billionto11billion')
    df['Revenue'] = df['Revenue'].str.replace('Lessthan1million', '0millionto1million')
    df['Revenue'] = df['Revenue'].str.replace('million', ' ')
    df['Revenue'] = df['Revenue'].str.replace('billion', '000 ')
    df["Revenue"] = df["Revenue"].str.replace(" to","to")
     #clean Size column
    df["Size"] = df["Size"].str.replace("employees","",regex=True)
    df["Size"] = df["Size"].str.replace("+","to10001",regex=True)
    df["Size"] = df["Size"].str.replace(" ","",regex=True)
    df["Size"] = df["Size"].replace("Unknown",np.nan)
    
def transform_dataset(df):
    """Transforms the dataset so its more readable and easier to use"""
    
    df["Minimum Salary"] = df["Salary Estimate"].apply(lambda x : methods.salary_parser_min(x))
    df["Minimum Salary"] = df["Minimum Salary"].astype(float)
    df["Maximum Salary"] = df["Salary Estimate"].apply(lambda x : methods.salary_parser_max(x))
    df["Maximum Salary"] = df["Maximum Salary"].astype(float)
    df.drop("Salary Estimate",axis=1, inplace=True)
    
    
    df["Department"] = df["Job Title"].apply(lambda x: methods.splitting_department_from_job_title(x,"department"))    
    df["Job Title"] = df["Job Title"].apply(lambda x: methods.splitting_department_from_job_title(x,"Job Title"))
    df["Job_title"] = df["Job Title"]
    
    df.drop("Job Title",axis=1, inplace=True)
    
    df["Location_City"]=df["Location"].apply(lambda x: methods.spliting_location_and_HQ(x,"city"))
    df["Location_State"]=df["Location"].apply(lambda x: methods.spliting_location_and_HQ(x,"state"))
    df["HQ_City"]=df["Headquarters"].apply(lambda x: methods.spliting_location_and_HQ(x,"city"))
    df["HQ_State"]=df["Headquarters"].apply(lambda x: methods.spliting_location_and_HQ(x,"state"))
    
    df["min_revenue_in_milions"]=df["Revenue"].apply(lambda x: methods.splitting_revenue(x,"min"))
    df["max_revenue_in_milions"]=df["Revenue"].apply(lambda x: methods.splitting_revenue(x,"max"))
    
    df["HQ_State"] = df["HQ_State"].str.replace("Sweden","SWE")
    df["HQ_State"] = df["HQ_State"].str.replace("Belgium","BE")
    df["HQ_State"] = df["HQ_State"].str.replace("Iran","IR")
    df["HQ_State"] = df["HQ_State"].str.replace("United Kingdom","UK")
    
    df["Company Name"] = df["Company Name"].astype(str)
    df["Type of ownership"] = df["Type of ownership"].str.replace("/","|")
    
    df["min_size_emp"]=df["Size"].apply(lambda x: methods.splitting_revenue(x,"min")) #using splitting_revenue method to split size aswell since they have the same deno.
    df["max_size_emp"]=df["Size"].apply(lambda x: methods.splitting_revenue(x,"max"))
    df["max_size_emp"] = df["max_size_emp"].astype(float)
    df["min_size_emp"] = df["min_size_emp"].astype(float)
    
    print(df.head(10))
    
def top_10_words_in_column(df) -> str:
    """returns 10 most common words in a column

    Args:
        df (str): column consisted of strings

    Returns:
        str : returns 10 strings
    """
    df["Job Description"]=df["Job Description"].apply(lambda x: methods.cleaning_column(x))
    df['frequency'] = df["Job Description"].apply(methods.word_frequency)
    merged_sorted_freq = methods.merge_dict_from_word_frequency(df["frequency"])
    items = methods.take(10, merged_sorted_freq.items())
    return methods.n_most_searched_words(items)
    
def plot_graphs(df):
    x1 = df["Minimum Salary"]
    x2 = df["Maximum Salary"]
    return plot_(x1, x2 , graph_type = ["hist"], colors= "blue", title="Salary Distribution", grid=True, separate=False, label_x="Salary", figure_size=(10,4), bins = 100)

