import os
import json
import re
import pandas as pd
import numpy as np



def extract_salary(salary: str):
    if pd.isna(salary):
        return np.nan, np.nan, np.nan
    if sum(char.isdigit() for char in salary) > 3:            # '60000-120000 грн, Залежить від рівня...', exclude small numbers
        parts = salary.replace("грн", "").strip().split(",", 1)
        salary_cols = "".join(char for char in parts[0] if char.isdigit() or char == "-")   # 'Заробітна плата від 40 000...'
        salary_cols = salary_cols.split("-")

        salary_up_to = int(salary_cols[1]) if len(salary_cols) > 1 else int(salary_cols[0])     # '10000 грн, За результатами...'
        salary_from = int(salary_cols[0])
        salary_conditions = parts[1] if len(parts) > 1 else np.nan

        return salary_from, salary_up_to, salary_conditions
    else:
        return np.nan, np.nan, salary.strip()


def classify_skills(skill_list):
    tech_skills = {
        "Python", "SQL", "Linux", "Git", "Docker", "PostgreSQL", "HTML", "CSS", "JavaScript", "AWS", "MySQL",
        "GitLab", "Kubernetes", "CI/CD", "Jenkins", "FastAPI", "PHP", "PowerShell", "Unity", "Django", "HTTP",
        "pandas", "MongoDB", "Redis", "NumPy", "Node.js", "Tableau", "Zabbix", "Terraform", "Scripting", "Arduino",
        "DHCP", "TensorFlow", "RabbitMQ", "SIEM", "UNIX", "GO", "OpenAI", "Nginx", "Google Sheets", "Debian",
        "TypeScript", "GitHub", "CentOS", "Hardware", "AJAX", "PyTorch", "Machine learning", "Flask",
        "Cisco", "VMware", "DAX", "Construct", "Selenium", "Elasticsearch", "STM32", "Power Query", "Reporting",
        "VLAN", "Android", "Kotlin", "JSON", "UART", "Postman", "Playwright", "Apache Airflow", "OpenVPN", "UDP",
        "Laravel", "Active Directory", "Databricks", "QGIS", "I2C", "HTML5", "ArduPilot", "MS SQL Server",
        "Altium Designer", "Apache Kafka", "FPGA", "DBT", "Figma", "Web development", "Debugging", "Redux",
        "Bitbucket", "WordPress", "Next.js", "Matplotlib", "ArcGIS", "Data Warehouse", "MikroTik", "MS Excel",
        "SSIS", "Power Pivot", "T-SQL", "MATLAB", "Docker Compose", "cron", "MAVlink", "Angular", "Google Analytics",
        "Looker Studio", "AI Agents", "BASH", "Java", "React", "Jira", "NoSQL", "TCP/IP", "Grafana", "REST API",
        "Scratch", "ClickHouse", "Blender", "GraphQL", "Vue.js", "XML", "jQuery", "WebSocket", "SDK", "MVVM",
        "UI/UX", "Stripe", "SQLite", "OpenCV", "UML",
    }
    soft_skills = {
        "Комунікабельність", "Відповідальність", "Креативність", "Викладання", "Стабільність", "Відкритість",
        "Англійська", "Уважність", "Ініціативність", "Критичне мислення", "Стресостійкість", "Організованість",
        "Дисциплінованість", "Самостійність", "problem-solving", "Responsibility", "Надійність", "Бажання навчатися",
        "Логічне мислення", "Flexibility", "Чесність", "Командна робота", "Менторство", "Гнучкість", "Цілеспрямованість",
        "Орієнтація на результат", "Аналітичні здібності", "Teamwork", "Project management", "Troubleshooting",
        "Робота в команді",
    }
    general_skills = {
        "Програмування", "Розробка", "Тестування", "AI", "Google", "BI", "REST", "Support",
        "Моделювання", "Engineering", "ML", "digital", "R&D", "Ведення", "Проєктування",
        "Дизайн", "робототехніка", "Графічний дизайн", "математика", "Marketing", "Prompt",
        "Ведення технічної документації", "Canva", "Creativity", "Meta", "Аудит", "Резервне копіювання",
        "Відеомонтаж", "Візуалізація", "ГІС", "Foundation", "Розробка", "Оператор", "SOLID", "LLM", "Agile",
        "Scrum", "Roblox", "Системний аналіз", "Аналіз даних", "Технічна грамотність", "SEO", "Clean Architecture"
    }

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
    return pd.Series({'Tech': tech, 'Soft': soft, 'General': general, "Not_classified": not_classified})




def skills(data_path: str):
    """
    Creates a complete list of skills from the hard-tech or soft skill?)
    """
    set_requirements = set()

    it_jobs_path = os.path.join(data_path, "it_jobs.jl")

    if os.path.exists(it_jobs_path):
        with open(it_jobs_path, encoding="utf-8") as f:
            for line in f:
                try:
                    item = json.loads(line)
                    set_requirements.update(set(item["requirements"]))
                except Exception:
                    pass
        print(f"List of {len(set_requirements)=} requirements for IT jobs")
    else:
        print("File it_jobs.jl not found. This set still is empty. ")

    reqs = sorted(list(set_requirements))

    # List dicts of IT jobs
    data = []
    for skill in reqs:
        is_tech = bool(re.fullmatch(r"[a-zA-Z0-9()-_;:,.<>/?|# ]+", skill))
        data.append({"skill": skill, "is_tech": is_tech, "original": skill})

    # To DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    it_jos_skills_path =  os.path.join(data_path, "it_job_skills.csv")
    df.to_csv(it_jos_skills_path, index=False, encoding="utf-8")




def jobs_skills_cleanser(data_path):
    """
    The skill cleaner updates the skills of each job to a single list according to the adjusted skills list.
    """

    list_changed_skills_path = os.path.join(data_path, "changed_skills.csv")
    changed_skills = pd.read_csv(list_changed_skills_path)
    list_changed_skills = changed_skills["skill"].tolist()

    in_jobs_path = os.path.join(data_path, "it_jobs.jl")
    out_jobs_path = os.path.join(data_path, "out_it_jobs.jl")

    if os.path.exists(in_jobs_path):
        with (open(in_jobs_path, "r", encoding="utf-8") as infile,
            open(out_jobs_path, "w", encoding="utf-8") as outfile):
            for line in infile:

                item = json.loads(line)
                if any(elem in item["requirements"] for elem in list_changed_skills):
                    # updating job requirements
                    item["requirements"] = upgrade_skills_of_job(item["requirements"], changed_skills)
                outfile.write(json.dumps(item, ensure_ascii=False) + "\n")


    else:
        print("File it_jobs.jl not found. This set still is empty. ")


def upgrade_skills_of_job(reqs: list, changed_skills: pd.DataFrame) -> list:
    result = []
    for req in reqs:
        match = changed_skills[changed_skills["skill"] == req]
        if not match.empty:
            req = match["original"].values[0]
        result.append(req)
    return result

#
#
# if __name__ == "__main__":
#     print(extract_salary("'10000 грн, За результатами."))