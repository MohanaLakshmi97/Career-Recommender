from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def predict_career(skills, cgpa):
    job_data = pd.read_csv("data/job_roles.csv")
    labels = job_data["Job Role"].tolist()
    feature_matrix = []
    label_vector = []
    all_skills = set()
    for _, row in job_data.iterrows():
        for skill in row["Required Skills"].split(";"):
            all_skills.add(skill.strip().lower())
    all_skills = sorted(all_skills)
    skill_to_index = {skill: i for i, skill in enumerate(all_skills)}

    for _, row in job_data.iterrows():
        row_skills = row["Required Skills"].split(";")
        vector = [0] * len(all_skills)
        for skill in row_skills:
            vector[skill_to_index[skill.strip().lower()]] = 1
        vector.append(7.5)  # Assume average CGPA
        feature_matrix.append(vector)
        label_vector.append(row["Job Role"])

    model = RandomForestClassifier()
    model.fit(feature_matrix, label_vector)

    # Prepare student vector
    input_vector = [0] * len(all_skills)
    for skill in skills.replace(",", ";").split(";"):
        if skill.strip().lower() in skill_to_index:
            input_vector[skill_to_index[skill.strip().lower()]] = 1
    input_vector.append(cgpa)
    return model.predict([input_vector])[0]