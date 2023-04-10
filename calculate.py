import pandas as pd
import numpy as np
import methods
from visuals import plot_


def convert_easy_apply(df: pd.DataFrame, entry: str) -> pd.DataFrame:
    """Converts the  column values to bool 

    Args:
        df (pd.DataFrame): column consisted of object values

    Returns:
        pd.DataFrame: returns a column with bool values 
    """
    df[entry] = df[entry].apply(lambda x: methods.convert_Column_Value_to_Bool(x))
    return df

def clean(df: pd.DataFrame, entry: dict) -> pd.DataFrame:
    """
    Cleans the specified column in the input DataFrame by replacing a set of
    input values with a set of output values using regular expressions.

    Args:
        df (pd.DataFrame): The DataFrame to be cleaned.
        entry (dict): A dictionary containing the following keys:
            - 'col' (str): The name of the column to be cleaned.
            - 'input' (list of str): A list of strings to be replaced in the column.
            - 'output' (list of str): A list of strings to replace the input strings with.

    Returns:
        pd.DataFrame: The cleaned DataFrame.

    Raises:
        ValueError: If the 'col', 'input', or 'output' keys are missing from the 'entry' dictionary.

    """
    column_name = entry["col"]
    input_name = entry["input"]
    output_name = entry["output"]
    df[column_name] = df[column_name].replace((input_name), output_name, regex = True)
    return df

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """This methods collects all methods for cleaning and transforming the dataframe

    Args:
        df (pd.DataFrame): 

    Returns:
        pd.DataFrame: returns the dataframe
    """
    
    convert_easy_apply(df, "Easy Apply")
    methods.replace_to_nan(df)
    
    cols = ["Size","Company Name","Job Title","Revenue"]
    inputs = [["employees", "\+", " ", "Unknown"],["\n.*"],[" â"],["Unknown / Non-Applicable", '\$', '(USD)', '\(', '\)', ' ', '\+', '2to5billion', '5to10billion ', 'million', '10billion', 'Lessthan1million', 'million', 'billion', ' to']]
    outputs = [["", "to10001","",np.nan],[""],[""],[np.nan, ' ', ' ', ' ', ' ', '', '', '2billionto5billion', '5billionto10billion', ' ', '10billionto11billion', '0millionto1million', ' ', '000 ', 'to']]
    for i in range (len(cols)):
        temp_dict = {"col": cols[i], "input": inputs[i], "output": outputs[i]}
        df = clean(df, temp_dict)
    
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
    
    return df

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

def split_column(df: pd.DataFrame, column_name: str, new_column_prefix: str) -> pd.DataFrame:
    """
    Splits a column in a DataFrame into 'min' and 'max' values using the methods.splitting_revenue function.
    Appends the resulting columns to the DataFrame with the given new_column_prefix.

    Args:
        df (pandas.DataFrame): The DataFrame containing the column to be split.
        column_name (str): The name of the column to be split.
        new_column_prefix (str): The prefix to be used for the new column names.

    Returns:
        pandas.DataFrame: The original DataFrame with the new columns appended.
    """
    df[f"{new_column_prefix}_min"] = df[column_name].apply(lambda x: methods.splitting_revenue(x, "min"))
    df[f"{new_column_prefix}_max"] = df[column_name].apply(lambda x: methods.splitting_revenue(x, "max"))
    return df

def split_location(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Splits a column in a DataFrame into 'city' and 'state' values using the methods.spliting_location_and_HQ function.
    Appends the resulting columns to the DataFrame with the given new_column_name.

    Args:
        df (pandas.DataFrame): The DataFrame containing the column to be split.
        column_name (str): The name of the column to be split.
        new_column_prefix (str): The prefix to be used for the new column names.

    Returns:
        pandas.DataFrame: The original DataFrame with the new columns appended.
    """
    df[f"{column_name}_City"] = df[column_name].apply(lambda x: methods.spliting_location_and_HQ(x, "city"))
    df[f"{column_name}_State"] = df[column_name].apply(lambda x: methods.spliting_location_and_HQ(x, "state"))
    return df

def align_index(df: pd.DataFrame) -> pd.DataFrame:
    """fixing the index column to align the  default index

    Args:
        df (pd.DataFrame): the DataFrame were working with

    Returns:
        pd.DataFrame: returns a DataFrame where the dataframe index is the same as the default index column
    """
    for i in df.index: 
        df.loc[i,"index"] = i
    return df

def transform_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """This Methods collects all other methods and is supposed to be run in the main module.

    Args:
        df (pd.DataFrame): DataFrame were transforming

    Returns:
        pd.DataFrame: returns a new transformed DataFrame.
    """
    get_min_max_salary(df)
    split_Department_from_Job_Title(df)
    align_index(df)
    
    df = split_location(df, "Location")
    df = split_location(df, "Headquarters")
    
    df = split_column(df, "Size", "size_emp")
    
    df = replace_country_names(df, ["Headquarters_State"], replacing_dict = {
        "Sweden": "SWE",
        "Belgium": "BE",
        "Iran": "IR",
        "United Kingdom": "UK",
        "Canada": "CA" })
    
    df["Company Name"] = df["Company Name"].astype(str)
    df["Median Salary"]=(df["Maximum Salary"] + df["Minimum Salary"])/2
    
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
    return methods.take(10, merged_sorted_freq.items())
    
def plot_graphs(df):
    x1 = df["Minimum Salary"]
    x2 = df["Maximum Salary"]
    return plot_(x1, x2 , graph_type = ["hist"], colors= "blue", title="Salary Distribution", grid=True, separate=False, label_x="Salary", figure_size=(10,4), bins = 100)

def view_specific_table(df: pd.DataFrame) -> pd.DataFrame:
    """returns a dataframe of specific columns

    Args:
        df (pd.DataFrame): original dataframe were exctracting columns from.

    Returns:
        pd.DataFrame: returns the same dataframe but with specific columns.
    """
    list_columns = ["index", "Job Title", "Rating", "Maximum Salary", "Median Salary"]
    return methods.view_table(df, list_columns)