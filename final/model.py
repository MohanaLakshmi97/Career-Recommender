def calculate_match_score(student_skills, job_skills):
    student_skills = {s.strip().lower() for s in student_skills.replace(",", ";").split(";")}
    job_skills = {s.strip().lower() for s in job_skills.split(";")}
    if not job_skills:
        return 0
    return len(student_skills & job_skills) / len(job_skills)

def get_missing_skills(student_skills, job_skills):
    student_skills = {s.strip().lower() for s in student_skills.replace(",", ";").split(";")}
    job_skills = {s.strip().lower() for s in job_skills.split(";")}
    return list(job_skills - student_skills)

def get_learning_resources(missing_skills, resource_df, grouped=False):
    resources = {}

    for skill in missing_skills:
        matches = resource_df[resource_df["Skill"].str.lower() == skill.lower()]
        if not matches.empty:
            # Split the comma-separated links into a list
            links = matches["Resources"].values[0].split(",")
            # Strip whitespace and filter out any empty strings
            resources[skill] = [link.strip() for link in links if link.strip()]

    return resources if not grouped else {"All": resources}



def get_skill_description(skill):
    descriptions = {
        "python": "Popular programming language for data and software development.",
        "sql": "Used for managing and querying relational databases.",
        "excel": "Spreadsheet tool used for data organization and analysis.",
        "tableau": "Data visualization tool for BI and dashboards.",
        "tensorflow": "Open-source ML framework for deep learning.",
        "java": "Widely used programming language for backend and app development.",
        "spring": "Java framework for building web applications.",
        "pandas": "Python library for data analysis and manipulation.",
        "numpy": "Python library for numerical computations.",
        "html": "Standard markup language for creating web pages.",
        "css": "Stylesheet language used to describe the look of a webpage.",
        "javascript": "Scripting language for interactive web applications.",
        "react": "JavaScript library for building user interfaces.",
        "node.js": "JavaScript runtime used for building server-side applications.",
        "mongodb": "NoSQL database program for high-volume data storage.",
        "aws": "Amazon Web Services – cloud computing platform.",
        "linux": "Open-source operating system widely used in servers and development.",
        "docker": "Platform for developing, shipping, and running applications in containers.",
        "kubernetes": "System for automating deployment and management of containerized apps.",
        "git": "Version control system for tracking changes in code.",
        "ci/cd": "Continuous Integration and Delivery for software development automation.",
        "networking": "Concepts and tools for managing computer networks.",
        "firewalls": "Security systems that monitor and control network traffic.",
        "ethical hacking": "Practice of legally bypassing system security to identify vulnerabilities.",
        "spark": "Big data processing engine for large-scale data analytics.",
        "etl": "Extract, Transform, Load – process for integrating data from multiple sources.",
        "power bi": "Microsoft tool for interactive data visualization and business intelligence.",
        "communication": "Skills for effectively conveying ideas and information.",
        "kotlin": "Modern programming language used for Android development.",
        "android studio": "IDE used for developing Android applications.",
        "scikit-learn": "Python library for machine learning models and tools.",
        "manual testing": "Process of manually checking software for defects.",
        "selenium": "Automated testing tool for web applications.",
        "bugzilla": "Bug-tracking tool for managing software issues.",
        "mysql": "Relational database management system based on SQL.",
        "performance tuning": "Optimizing system or database for better performance.",
        "backup & recovery": "Strategies to protect and restore data in case of failure.",
        "figma": "Web-based design tool for UI/UX prototyping and collaboration.",
        "adobe xd": "UI/UX design and prototyping tool by Adobe.",
        "design thinking": "Problem-solving approach focusing on user-centric design."
    }

    return descriptions.get(skill.lower(), "No description available for this skill.")
