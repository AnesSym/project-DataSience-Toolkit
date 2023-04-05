import pandas as pd
import numpy as np
import methods
from visuals import plot_


def convert_easy_apply(df: pd.DataFrame) -> pd.DataFrame:
    """Converts the  "Easy Apply" column values to bool 

    Args:
        df (pd.DataFrame): column consisted of object values

    Returns:
        pd.DataFrame: returns a column with bool values 
    """
    df["Easy Apply"] = df["Easy Apply"].apply(lambda x: methods.convert_Column_Value_to_Bool(x))
    return df["Easy Apply"]

def clean_company_name(df: pd.DataFrame) -> pd.DataFrame:
    """Removes the \n character inside the "Company Name" column

    Args:
        df (pd.DataFrame)

    Returns:
        pd.DataFrame: returns a column wihtout \n.
    """
    df['Company Name'] = df['Company Name'].str.replace('\n.*', ' ', regex=True)
    return df['Company Name']

def clean_job_title(df: pd.DataFrame) -> pd.DataFrame:
    """Removes "â" and replaces "/" with "|"

    Args:
        df (pd.DataFrame): 

    Returns:
        pd.DataFrame: returns a column
    """
    df["Job Title"] = df["Job Title"].str.replace(" â","")
    df["Job Title"] = df["Job Title"].str.replace("/","|")
    return df["Job Title"] 

def clean_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """transforms the strings so we can split it easier

    Args:
        df (pd.DataFrame):

    Returns:
        pd.DataFrame: returns a transformed "revenue" column
    """
    df["Revenue"] = df["Revenue"].replace("Unknown / Non-Applicable", np.nan)
    df['Revenue'] = df['Revenue'].str.replace('$', ' ', regex=True)
    df['Revenue'] = df['Revenue'].str.replace('(USD)', ' ', regex=True)
    df['Revenue'] = df['Revenue'].str.replace('(', ' ', regex=True)
    df['Revenue'] = df['Revenue'].str.replace(')', ' ', regex=True)
    df['Revenue'] = df['Revenue'].str.replace(' ', '', regex=True)
    df['Revenue'] = df['Revenue'].str.replace('+', '', regex=True)
    df['Revenue'] = df['Revenue'].str.replace('2to5billion', '2billionto5billion')
    df['Revenue'] = df['Revenue'].str.replace('5to10billion ', '5billionto10billion')
    df['Revenue'] = df['Revenue'].replace('million', ' ')
    df['Revenue'] = df['Revenue'].replace('10billion', '10billionto11billion')
    df['Revenue'] = df['Revenue'].str.replace('Lessthan1million', '0millionto1million')
    df['Revenue'] = df['Revenue'].str.replace('million', ' ')
    df['Revenue'] = df['Revenue'].str.replace('billion', '000 ')
    df["Revenue"] = df["Revenue"].str.replace(" to","to")
    return df["Revenue"]

def clean_size(df: pd.DataFrame) -> pd.DataFrame:
    """cleans the "Size" column and prepares it for separation 

    Args:
        df (pd.DataFrame): 

    Returns:
        pd.DataFrame: returns a clean "Size" column
    """
    df["Size"] = df["Size"].str.replace("employees","",regex=True)
    df["Size"] = df["Size"].str.replace("+","to10001",regex=True)
    df["Size"] = df["Size"].str.replace(" ","",regex=True)
    df["Size"] = df["Size"].replace("Unknown",np.nan)
    return df["Size"]

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """This methods collects all methods for cleaning and transforming the dataframe

    Args:
        df (pd.DataFrame): 

    Returns:
        pd.DataFrame: returns the dataframe
    """
    convert_easy_apply(df)
    methods.replace_to_nan(df)
    clean_company_name(df)
    clean_job_title(df)
    clean_revenue(df)
    clean_size(df)
    
    return df

def get_min_max_salary(df: pd.DataFrame) -> pd.DataFrame:
    """Splits "salary estimate" column into min and max salary 

    Args:
        df (pd.DataFrame): df["Minimum Salary"]

    Returns:
        pd.DataFrame: returns 2 new columns ["Minimum Salary"], ["Maximum Salary"]
    """
    df["Minimum Salary"] = (df["Salary Estimate"].apply(lambda x : methods.salary_parser_min(x))).astype(float)
    df["Maximum Salary"] = (df["Salary Estimate"].apply(lambda x : methods.salary_parser_max(x))).astype(float)
    df.drop("Salary Estimate",axis=1, inplace=True)
    
    return df["Minimum Salary"], df["Maximum Salary"]

def split_Department_from_Job_Title(df: pd.DataFrame) -> pd.DataFrame:
    """splits the Job Title into 2 new columns, "Department" and "Job Title"

    Args:
        df (pd.DataFrame): 

    Returns:
        pd.DataFrame: two columns ["Department"], ["Job Title"]
    """
    df["Department"] = df["Job Title"].apply(lambda x: methods.splitting_department_from_job_title(x,"department"))    
    df["Job Title"] = df["Job Title"].apply(lambda x: methods.splitting_department_from_job_title(x,"Job Title"))
    
    return df["Department"], df["Job Title"]

def replace_country_names(df: pd.DataFrame, column: str, replacing_dict: dict) -> pd.DataFrame:
    """ Replaces certain country names with their corresponding country codes in the specified column of a DataFrame.

    Args:
        df (pd.DataFrame): the dataframe where were applying this method
        column (str): the name of the column in which to replace the country names with country codes.
        replacing_dict (dict): dictionary containing what is being replaced

    Returns:
        pd.DataFrame: returns a new column with replaced values
    """
    df[column] = df[column].replace(replacing_dict)
    return df

def transform_dataset(df: pd.DataFrame) -> pd.DataFrame:
    
    
    df["Location_City"]=df["Location"].apply(lambda x: methods.spliting_location_and_HQ(x,"city"))
    df["Location_State"]=df["Location"].apply(lambda x: methods.spliting_location_and_HQ(x,"state"))
    df["HQ_City"]=df["Headquarters"].apply(lambda x: methods.spliting_location_and_HQ(x,"city"))
    df["HQ_State"]=df["Headquarters"].apply(lambda x: methods.spliting_location_and_HQ(x,"state"))
    
    df["min_revenue_in_milions"]=df["Revenue"].apply(lambda x: methods.splitting_revenue(x,"min"))
    df["max_revenue_in_milions"]=df["Revenue"].apply(lambda x: methods.splitting_revenue(x,"max"))
    
    df = replace_country_names(df, ["HQ_state"], replacing_dict = {
        "Sweden": "SWE",
        "Belgium": "BE",
        "Iran": "IR",
        "United Kingdom": "UK"})
    
    df["Company Name"] = df["Company Name"].astype(str)
    df["Type of ownership"] = df["Type of ownership"].str.replace("/","|")
    
    df["min_size_emp"]=df["Size"].apply(lambda x: methods.splitting_revenue(x,"min")) #using splitting_revenue method to split size aswell since they have the same deno.
    df["max_size_emp"]=df["Size"].apply(lambda x: methods.splitting_revenue(x,"max"))
    df["max_size_emp"] = df["max_size_emp"].astype(float)
    df["min_size_emp"] = df["min_size_emp"].astype(float)
    
    return df
 
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

