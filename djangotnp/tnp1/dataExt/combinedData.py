import pandas as pd
import json


def get_placement_data_combined():
    """
    Reads placement data from Excel and CSV files for the years 2023 and 2024,
    calculates total placements for each year, and compares branch-wise placements
    between the two years.
    Returns:
        dict: A dictionary containing:
            - 'Total_placements_2023' (int): Total number of placements in 2023.
            - 'Total_placements_2024' (int): Total number of placements in 2024.
            - 'branch_comparison' (dict): A dictionary with branch-wise placement
              comparison between 2023 and 2024.
    """

    df_2023 = pd.read_excel(
        r"Y:\Projects\TnP\TNPProject\TnP\djangotnp\dataExt\alumni2023.xlsx"
    )
    df_2024 = pd.read_csv(
        r"Y:\Projects\TnP\TNPProject\TnP\djangotnp\dataExt\cleaned_file-alumni-2024.csv"
    )

    total_placements_2023 = int(df_2023["Name of the Employer"].notnull().sum())
    total_placements_2024 = int(df_2024["Name of the Employer"].notnull().sum())
    res = {}
    res["Total_placements_comparison"] = {
        "Total_placements_2023": total_placements_2023,
        "Total_placements_2024": total_placements_2024,
    }
    branch_placements_2023 = df_2023.groupby("BRANCH           /DIV")[
        "Name of the Employer"
    ].count()
    branch_placements_2024 = df_2024.groupby("BRANCH/DIV")[
        "Name of the Employer"
    ].count()

    branch_comparison_df = pd.DataFrame(
        {"2023": branch_placements_2023, "2024": branch_placements_2024}
    ).fillna(0)

    # Convert the DataFrame to a dictionary and ensure all values are Python native types
    res["branch_comparison"] = branch_comparison_df.astype(int).to_dict()

    return res


# Get the placement data
result = get_placement_data_combined()

# Specify the JSON file path
json_file_path = r"Y:\Projects\TnP\TNPProject\TnP\djangotnp\dataExt\placement_data.json"

# Save the result to a JSON file
with open(json_file_path, "w") as json_file:
    json.dump(result, json_file, indent=4)

print(f"Data saved to {json_file_path}")
