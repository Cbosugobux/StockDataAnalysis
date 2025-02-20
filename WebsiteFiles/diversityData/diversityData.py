import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import json

def create_figure():
    # Load data
    df2017 = pd.read_excel('Resources/Employee Diversity.xlsx', sheet_name='2017')
    df2021 = pd.read_excel('Resources/Employee Diversity.xlsx', sheet_name='2021')

    df2017.replace(0, np.nan, inplace=True)
    df2021.replace(0, np.nan, inplace=True)

    companies = df2017['Company'].tolist()
    x = np.arange(len(companies))

    ethnicities = ['Female', 'Asian', 'Black', 'Latino']
    normal_data = {}
    for eth in ethnicities:
        col_name = f'{eth} %' if eth == 'Female' else f'% {eth}'
        normal_data[f"{eth} (2017)"] = df2017[col_name].values
        normal_data[f"{eth} (2021)"] = df2021[col_name].values

    # Convert data to JSON for API
    df2017["year"] = 2017
    df2021["year"] = 2021
    df_combined = pd.concat([df2017, df2021])
    
    df_combined.rename(columns={
        "Company": "company",
        "Female %": "gender_female",
        "% Asian": "race_asian",
        "% Black": "race_black",
        "% Latino": "race_hispanic"
    }, inplace=True)

    json_data = df_combined.to_dict(orient="records")
    with open("data/diversityData.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    # Create Matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(companies, df2017["Female %"], label="2017 Female %", color="blue")
    ax.barh(companies, df2021["Female %"], label="2021 Female %", color="pink")
    ax.set_xlabel("Percentage")
    ax.set_ylabel("Company")
    ax.set_title("Diversity Trends (2017 vs 2021)")
    ax.legend()

    return fig
