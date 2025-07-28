import json

import pandas as pd
import numpy as np


def extract_salary(salary: str):
    if pd.isna(salary):
        return np.nan, np.nan, np.nan
    # '60000-120000 грн, Залежить від рівня...', exclude small numbers
    if sum(char.isdigit() for char in salary) > 3:            
        parts = salary.replace("грн", "").strip().split(",", 1)
        # 'Заробітна плата від 40 000...'
        salary_cols = "".join(char for char in parts[0] if char.isdigit() or char == "-")
        salary_cols = salary_cols.split("-")
        # '10000 грн, За результатами...'
        salary_up_to = int(salary_cols[1]) if len(salary_cols) > 1 else int(salary_cols[0])
        salary_from = int(salary_cols[0])
        salary_conditions = parts[1] if len(parts) > 1 else np.nan

        return salary_from, salary_up_to, salary_conditions
    else:
        return np.nan, np.nan, salary.strip()


def classify_skills(skill_list):

    with open("skills_by_classe.json", "r", encoding="utf-8") as f:
        skills_data = json.load(f)

    tech_skills = set(skills_data["Tech"])
    soft_skills = set(skills_data["Soft"])
    general_skills = set(skills_data["General"])


    tech = []
    soft = []
    general = []
    not_classified = []

    for skill in skill_list:
        if skill in tech_skills:
            tech.append(skill)
        elif skill in soft_skills:
            soft.append(skill)
        elif skill in general_skills:
            general.append(skill)
        else:
            not_classified.append(skill)
    return pd.Series(
        {"Tech": tech, 
         "Soft": soft, 
         "General": general, 
         "Not_classified": not_classified}
        )


# if __name__ == "__main__":
#     print(extract_salary("'10000 грн, За результатами."))
