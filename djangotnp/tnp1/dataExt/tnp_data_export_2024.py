import os
import pandas as pd
import json
import numpy as np


def convert_to_native_types(data):
    """
    Recursively converts all NumPy and Pandas data types in a dictionary to native Python types
    to make them JSON serializable. Also converts any tuple dictionary keys into strings.

    Args:
        data (dict): The dictionary containing data with NumPy/Pandas types and tuple keys.

    Returns:
        dict: A dictionary with all NumPy/Pandas types converted to Python-native types,
              and tuple keys converted to strings.
    """
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            # Convert tuple keys to string representation
            if isinstance(key, tuple):
                key = str(key)
            new_data[key] = convert_to_native_types(value)
        return new_data
    elif isinstance(data, list):
        return [convert_to_native_types(item) for item in data]
    elif isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, pd.Series):
        return data.to_list()
    elif isinstance(data, pd.DataFrame):
        return data.to_dict()
    elif pd.isna(data):
        return None
    else:
        return data


def get_data():
    """
    Reads alumni data from a CSV file and generates various statistics.
    Writes the generated data into a new JSON file.
    Returns:
        dict: A dictionary containing various statistics.
    """
    # File path to the CSV file
    file_path = (
        "Y:\Projects\TnP\TNPProject\TnP\djangotnp\dataExt\cleaned_file-alumni-2024.csv"
    )

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return {}

    # Reading the CSV file
    df = pd.read_csv(file_path)
    res = {}

    # Generate statistics for consents
    res["Consent_graph"] = dict(df["Consent"].value_counts())

    # Generate statistics for consents by branch/division
    res["consent_counts_by_branch"] = dict(df.groupby(["BRANCH/DIV", "Consent"]).size())

    # Top 10 employers
    employer_counts = df["Name of the Employer"].value_counts()
    top_10_employers = employer_counts.head(10)
    res["top_10_employers"] = dict(top_10_employers)

    # Filter placed students (those with employer name and salary)
    placed_students = df[
        df["Name of the Employer"].notnull()
        & df["Appointment Ref No. _Salary"].notnull()
    ]

    # Placement distribution by branch/division
    placement_distribution = dict(placed_students.groupby("BRANCH/DIV").size())
    res["placement_distribution_by_branch"] = dict(placement_distribution)

    # Convert salary column to numeric, handling errors
    df["Appointment Ref No._Salary"] = pd.to_numeric(
        df["Appointment Ref No. _Salary"], errors="coerce"
    )

    # Filter placed students again to handle cases where salary might be null or non-numeric
    placed_students = df.dropna(
        subset=["Name of the Employer", "Appointment Ref No._Salary"]
    )

    # Average salary by branch/division
    average_salary_by_branch = placed_students.groupby("BRANCH/DIV")[
        "Appointment Ref No._Salary"
    ].mean()
    res["average_salary_by_branch"] = dict(average_salary_by_branch)

    # Convert NumPy/Pandas types to native Python types
    res = convert_to_native_types(res)

    return res


def save_data_to_json(data, json_file_path):
    """
    Saves the provided data to a JSON file.

    Args:
        data (dict): The dictionary containing data to be saved.
        json_file_path (str): The path where the JSON file will be saved.
    """
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data successfully written to {json_file_path}")


# Generate the data
data = get_data()

# Check if the data was generated
if data:
    # Define the path where the JSON file will be saved
    json_file_path = "./alumni_data_2024.json"

    # Save the generated data to a JSON file
    save_data_to_json(data, json_file_path)
