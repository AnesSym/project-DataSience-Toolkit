import numpy as np
from collections import defaultdict
from itertools import islice
import pandas as pd


def convert_Column_Value_to_Bool(dataset: object) -> bool:
    """Converting column values to bool values 

    Args:
        entry (object): column consisted of objects

    Returns:
        bool : bool type column
    """
    
    if dataset == "-1":
        return False
    return True

def replace_to_nan(dataset: pd.DataFrame) -> pd.DataFrame:
    """replaces all objects -1, -1.0 and "-1" as NaN

    Args:
        dataset (object): entire datatset

    Returns:
        DataFrame: returns a new dataframe where the change is applied
    """
    return dataset.replace((['-1',"-1.0",-1]), [np.nan,np.nan,np.nan], inplace=True)

def salary_parser_min(salary_string: str):
  """Creating a new column for minimum salary

  Args:
      salary_string (str): Salary Estitmate column which we are splitting into 2 new columns being minimum and maximum

  Returns:
      str : returns the first column after splitting the args column
  """
  salary_split = salary_string.split()
  salary = salary_split[0]
  del salary_split
  salary = salary.replace("K", "")
  salary = salary.replace("$", "")
  salary_range = salary.split("-")
  return salary_range[0]

def salary_parser_max(salary_string: str):
  """Creating a new column for maximum salary

  Args:
      salary_string (str): Salary Estitmate column which we are splitting into 2 new columns being minimum and maximum

  Returns:
      str : returns the second column after splitting the args column
  """
  salary_split = salary_string.split()
  salary = salary_split[0]
  del salary_split
  salary = salary.replace("K", "")
  salary = salary.replace("$", "")
  salary = salary.replace("(Employer","")
  salary_range = salary.split("-")
  return salary_range[-1]

def splitting_department_from_job_title (entry : str, key_word : str) -> str:
    """Splitting Department from Job title in the column "Job Title"
    
    Args:
        entry (str, str): parse the column as an str, 2nd argument is either job_title or department.
    Returns:
        str: returns a new column at the end of the dataset
    """
    
    department_job_title = entry.split(",")
    job_title = department_job_title[0]
    department = department_job_title[-1]
    if key_word == "Job Title":
        return job_title
    else:
        
        return department
    
def spliting_location_and_HQ (entry : object, geo_type : str) -> str:
    """Splits the location and HQ column to a city column and a state column.

    Args:
        entry (object,str): Location column we want to split. 2nd argument is either "city" or "state"

    Returns:
        str: returns either a locaton_city, locaton_state, HQ_city or HQ_state column
    """
    entry = str(entry)
    
    if entry == "nan":
        return None
    entry = entry.replace(" ", "")
    location_HQ_split = entry.split(",")
    location_HQ_city_state = location_HQ_split
    if geo_type == "city":
        return location_HQ_city_state[0]
    else:
        return location_HQ_city_state[1]
    
def splitting_revenue(entry: object, key_word: str) -> str:
    """splits the revenue to a max and a min revenue column

    Args:
        entry (object), key_word (str): Revenue column 

    Returns:
        str: returns either a minimum or maximum column dependent on key_word
    """
    entry = str(entry)
    
    if entry == "nan":
        return None
    min_max = entry.split("to")
    if key_word == "min":
        return min_max[0]
    else:
        return min_max[-1]
    
def cleaning_column (entry:str) -> str:
    """Cleans the text 

    Args:
        entry (str): takes in a column of text

    Returns:
        str: returns an all lowered text that is cleaned from special chars and common stopowords.
    """
    entry = entry.lower()
    entry = entry.replace(",","")
    entry = entry.replace("\n"," ")
    entry = entry.replace(".","")
    entry = entry.replace("/ ","")
    entry = entry.replace("/","|")
    entry = entry.replace("(","")
    entry = entry.replace(")","")
    entry = entry.replace("  "," ")
    entry = entry.replace(" and "," ")
    entry = entry.replace(" a "," ")
    entry = entry.replace(" the "," ")
    entry = entry.replace(" our "," ")
    entry = entry.replace(" we "," ")
    entry = entry.replace(" to "," ")
    entry = entry.replace(" of "," ")
    entry = entry.replace(" is "," ")
    entry = entry.replace(" in "," ")
    entry = entry.replace(" with "," ")
    entry = entry.replace(" as "," ")
    entry = entry.replace(" has "," ")
    entry = entry.replace(" you "," ")
    entry = entry.replace(" that "," ")
    entry = entry.replace(" are "," ")
    entry = entry.replace(" at "," ")
    entry = entry.replace(" like "," ")
    entry = entry.replace(" on "," ")
    entry = entry.replace(" about "," ")
    entry = entry.replace(" have "," ")
    entry = entry.replace(" us "," ")
    entry = entry.replace(" help "," ")
    entry = entry.replace(" for "," ")
    entry = entry.replace(" what "," ")
    entry = entry.replace(" real "," ")
    entry = entry.replace(" their "," ")
    entry = entry.replace(" new "," ")
    entry = entry.replace(" an "," ")
    entry = entry.replace(" or "," ")
    entry = entry.replace(" this "," ")
    entry = entry.replace(" in "," ")
    entry = entry.replace(" into "," ")
    entry = entry.replace("•"," ")
    entry = entry.replace(" will "," ")
    entry = entry.replace(" from "," ")
    entry = entry.replace(" be "," ")
    entry = entry.replace(" by "," ")
    
    return entry

def word_frequency(text: str)-> dict:
    """takes in a column of text, and returns a dictionary of words sorted by frequency

    Args:
        text (str): sentences 

    Returns:
        dict: column of sorted dictionaries
    """
    
    words = text.split()
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    sorted_frequency = {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)} #sort by descending order
    return sorted_frequency

def merge_dict_from_word_frequency (entry: dict) -> dict:
    """merges all rows from a column of dictionaries into a single dictionary

    Args:
        entry (dict): dictionary we want to merge

    Returns:
        dict: a single dictionary with combined values 
    """
    merged_dict = defaultdict(int)
    for d in entry:
        for key, value in d.items():
            merged_dict[key] += value

    new_frequency_sorted = {k: v for k, v in sorted(merged_dict.items(), key=lambda item: item[1], reverse=True)} #sorts the dict by descending order
    return new_frequency_sorted
    
def take(n :int, iterable: dict)->list:
    """Return the first n items of the iterable as a list.

    Args:
        n (int): number of words 
        iterable (dict): dictionary we want to return as a list

    Returns:
        list: first n items from the dict 
    """
    
    return list(islice(iterable, n))

def n_most_searched_words(entry):
    """this method only loops thru the list and prints the top n words searched

    Args:
        entry (list): list of items 
    """
    for item in entry:
         print(item[0])