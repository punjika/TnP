import pandas as pd
import numpy as np
import json


def convert_to_native_types(data):
    """
    Recursively converts all NumPy and Pandas data types in a dictionary to native Python types
    to make them JSON serializable. Also converts any tuple dictionary keys into strings.
    """
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
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
    Reads data from two Excel files, processes it, and returns a dictionary with various statistics.
    """
    # Use raw string (r"") to prevent escape sequences from causing issues
    df2 = pd.read_excel(
        r"Y:\Projects\TnP\TNPProject\TnP\djangotnp\dataExt\filetered2023data (1).xlsx"
    )
    df = pd.read_excel(
        r"Y:\Projects\TnP\TNPProject\TnP\djangotnp\dataExt\alumni2023.xlsx"
    )

    df["Consent"] = df["Consent"].str.lower()

    res = {}

    # Count occurrences of each 'Consent' value
    consent_counts = dict(df["Consent"].value_counts())
    res["Consent_graph"] = consent_counts

    # Group 'Consent' counts by 'BRANCH /DIV'
    consent_counts_by_branch = dict(
        df.groupby(["BRANCH           /DIV", "Consent"]).size()
    )
    res["consent_counts_by_branch"] = consent_counts_by_branch

    # Get top 10 employers
    employer_counts = df["Name of the Employer"].value_counts()
    top_10_employers = employer_counts.head(10)
    res["top_10_employers"] = dict(top_10_employers)

    # Category-wise student distribution from the second Excel file
    res["Category_wise_student_distribution"] = dict(df2["Category"].value_counts())

    # Convert NumPy/Pandas types to native Python types
    res = convert_to_native_types(res)

    return res


def save_data_to_json(data, json_file_path):
    """
    Saves the provided data to a JSON file.
    """
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data successfully written to {json_file_path}")


# Generate the data
data = get_data()

# Define the path where the JSON file will be saved
json_file_path = (
    r"Y:\Projects\TnP\TNPProject\TnP\djangotnp\dataExt\alumni_data_2023.json"
)

# Save the generated data to a JSON file
save_data_to_json(data, json_file_path)
