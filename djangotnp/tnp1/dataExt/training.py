import pandas as pd
import json
import os


def Training():
    # Update the path to your data.csv file accordingly
    df = pd.read_csv("y:/Projects/TnP/TNPProject/TnP/djangotnp/dataExt/data.csv")

    res = {}

    res["Student_consent_for_Trainning_Institute"] = {
        "CC": int(
            df["Test Score average_Consent for Trainning_CC"].value_counts().sum()
        ),
        "CPLC": int(
            df["Test Score average_Consent for Trainning_CPLC"].value_counts().sum()
        ),
        "TIME": int(
            df["Test Score average_Consent for Trainning_TIME"].value_counts().sum()
        ),
    }

    res["Test_score"] = {
        "Aptitude": float(
            df["Aptitude (PPT)_Total"][
                df["Aptitude (PPT)_Total"].ne(0) & df["Aptitude (PPT)_Total"].notna()
            ].mean()
        ),
        "Technical": float(
            df["Corporate Traning_Total"][
                df["Corporate Traning_Total"].ne(0)
                & df["Corporate Traning_Total"].notna()
            ].mean()
        ),
    }

    # Specify the path for the JSON file
    json_file_path = (
        "y:/Projects/TnP/TNPProject/TnP/djangotnp/dataExt/training_data.json"
    )

    # Generate JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(res, json_file, indent=4)

    print(f"Data saved to {json_file_path}")
    return res


# Call the function to generate and save the JSON file
Training()
