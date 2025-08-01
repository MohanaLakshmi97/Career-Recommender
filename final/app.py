import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from streamlit_lottie import st_lottie

# ── Lottie Loader ──────────────────────────────────────
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

from model import (
    calculate_match_score,
    get_missing_skills,
    get_learning_resources,
    get_skill_description,
)
from ml_model import predict_career
from pdf_generator import generate_pdf_report, generate_skill_plan_pdf

# ── Page Config ─────────────────────────────────────────
st.set_page_config(page_title="AI Career Recommender", page_icon="🎓", layout="wide")

# ── Custom CSS ───────────────────────────────────────────
st.markdown("""
<style>
body {
    background-color: #f5f6fa;
}
.main {
    padding: 2rem;
}
h1, h2, h3 {
    color: #2c3e50;
    font-family: 'Segoe UI', sans-serif;
}
.block-container {
    padding-top: 2rem;
}
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 10px 16px;
    border: none;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #45a049;
}
.stDownloadButton > button {
    background-color: #3498db;
    color: white;
    border-radius: 8px;
    padding: 10px 16px;
    border: none;
    font-weight: bold;
}
.stDownloadButton > button:hover {
    background-color: #2980b9;
}
.card {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────
job_data       = pd.read_csv("data/job_roles.csv")
student_data   = pd.read_csv("data/student_profiles.csv")
resources_data = pd.read_csv("data/skill_resources.csv")

# ── Sidebar Navigation ───────────────────────────────────
PAGES = ["🏠 Welcome", "🎯 Career Recommender", "📘 Interest‑Based Skill Planner"]
page = st.sidebar.radio("Navigate", PAGES)
student_name = ""

# ───────────────────────────── 1. Welcome ─────────────────────────────
if page == "🏠 Welcome":
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    .card {
        background-color: rgba(0, 0, 0, 0.55);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 2px 6px 10px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color:#1abc9c;'>🤖 Welcome to the AI Career Recommender System</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="card">
            <p style='font-size:18px;'>✨ Empower your future with AI-driven career guidance.</p>
            <ul style='font-size:17px; line-height:1.6;'>
                <li>🔍 <b>Discover</b> careers based on your skills and CGPA.</li>
                <li>📈 <b>Analyze</b> gaps and plan your learning path.</li>
                <li>📄 <b>Download</b> a custom career roadmap as PDF.</li>
            </ul>
            <p style='font-size:16px; margin-top:20px;'>Use the <b>sidebar</b> to navigate:</p>
            <ul style='font-size:17px; line-height:1.6;'>
                <li>🎯 Career Recommender</li>
                <li>📘 Interest-Based Skill Planner</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        lottie_robot = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_puciaact.json")
        if lottie_robot:
            st_lottie(lottie_robot, height=250, key="robot_hello")

    st.markdown("""
    <div class="pulse-box">
    ✅ You're ready! Use the <b>sidebar</b> to begin your personalized career journey 🚀✨
    </div>
    <style>
    @keyframes pulse {
      0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(26, 188, 156, 0.7); }
      70% { transform: scale(1.02); box-shadow: 0 0 0 10px rgba(26, 188, 156, 0); }
      100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(26, 188, 156, 0); }
    }
    .pulse-box {
      animation: pulse 2s infinite;
      background-color: #16a085;
      padding: 15px 25px;
      border-radius: 12px;
      font-size: 18px;
      font-weight: bold;
      color: white;
      box-shadow: 2px 4px 12px rgba(0,0,0,0.2);
      text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ───────────────────── 2. Career Recommender ──────────────────────────
elif page == "🎯 Career Recommender":
    st.markdown("""
    <style>
    .career-page {
        background: linear-gradient(to right, #f5f7fa, #c3cfe2);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .career-page h1 {
        font-size: 36px;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    lottie_ai = load_lottieurl("https://lottie.host/7d40581c-9488-4407-b8a2-d9ce7b77e8cb/KWmRPtqfRR.json")
    if lottie_ai:
        st_lottie(lottie_ai, height=200, key="ai_matcher")

    st.markdown("""
    <div class='career-page'>
        <h1>🎯 Career Recommender</h1>
        <p style='font-size:18px; text-align:center; color:#34495e;'>Get AI-powered suggestions based on your current skills and academic profile.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    student_name = col1.text_input("👤 Enter your name")
    skills = col1.text_input("🛠️ Enter your skills (e.g., Python;SQL;Tableau)")
    cgpa = col2.slider("🎓 Your CGPA", 5.0, 10.0, 8.0)

    if st.button("🚀 Recommend Career"):
        if not student_name or not skills:
            st.warning("⚠️ Please enter both your name and skills.")
            st.stop()

        results = []
        for _, row in job_data.iterrows():
            score = calculate_match_score(skills, row["Required Skills"])
            results.append((row["Job Role"], score, row["Category"], row["Avg Salary"], row["Required Skills"]))

        results.sort(key=lambda x: x[1], reverse=True)
        top_role, top_score, top_cat, top_salary, top_req = results[0]

        st.subheader(f"👋 Hello, {student_name}!")
        st.markdown(f"<h2 style='color:#27ae60;'>🌟 Best Match: {top_role}</h2>", unsafe_allow_html=True)
        st.markdown(f"""
            <p style='font-size:17px;'>
                💡 <b>Match Score:</b> {round(top_score*100, 2)}%<br>
                📂 <b>Category:</b> {top_cat}<br>
                💰 <b>Avg Salary:</b> ₹{top_salary:,.0f}
            </p>
        """, unsafe_allow_html=True)

        missing = get_missing_skills(skills, top_req)
        if missing:
            st.markdown("### ❌ Missing Skills & Meanings")
            for sk in missing:
                st.markdown(f"- <b>{sk}</b>: {get_skill_description(sk)}", unsafe_allow_html=True)

            st.markdown("### 🧠 Learning Resources")
            res = get_learning_resources(missing, resources_data, grouped=False)
            for sk, links in res.items():
                st.markdown(f"<p style='font-size:18px; font-weight:bold;'>{sk.title()}</p>", unsafe_allow_html=True)
                for link in links:
                    st.markdown(f"<a href='{link}' target='_blank'>🔗 Learn here</a>", unsafe_allow_html=True)
        else:
            st.success("✅ You already have all required skills for this role!")

        st.markdown("### 🔍 Other Matches")
        other_jobs = []
        for job, score, cat, salary, _ in results[1:3]:
            st.markdown(f"• {job} ({round(score*100, 1)}% match, {cat}, ₹{salary:,.0f})")
            other_jobs.append((job, round(score*100, 1)))

        st.markdown("### 📊 Match Score Chart")
        labels  = [top_role] + [j for j, _ in other_jobs]
        scores  = [round(top_score*100, 1)] + [s for _, s in other_jobs]
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.barh(labels[::-1], scores[::-1], color="#1abc9c")
        ax.set_xlabel("Match Score (%)")
        ax.set_title("Top Career Matches")
        st.pyplot(fig)

        prediction = predict_career(skills, cgpa)
        st.info(f"🤖 ML Predicted Role: {prediction}")

        if st.button("📄 Download PDF Report"):
            pdf_path = generate_pdf_report(student_name, results[:3], missing, get_learning_resources(missing, resources_data))
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download Report", f, file_name="Career_Recommendation_Report.pdf")
# ── 3. Interest‑Based Skill Planner ─────────────────────────────
else:
    st.markdown("<h1 style='color:#8e44ad;'>📘 Interest‑Based Skill Planner</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    interested_role = st.selectbox("🎯 Select Your Dream Job Role", job_data["Job Role"].unique())
    existing_skills = st.text_input("🔎 Skills You Already Have (e.g., Python;SQL;Excel)", key="existing_input")
    st.markdown("</div>", unsafe_allow_html=True)

    if interested_role:
        row = job_data[job_data["Job Role"] == interested_role].iloc[0]
        required = [s.strip() for s in row["Required Skills"].split(";")]
        existing = [s.strip().lower() for s in existing_skills.split(";")] if existing_skills else []
        missing = [s for s in required if s.lower() not in existing]

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(
            f"<h4>🔑 Skill Breakdown for <span style='color:#8e44ad'>{interested_role}</span></h4>",
            unsafe_allow_html=True,
        )
        for sk in required:
            status = "✅" if sk.lower() in existing else "❌"
            st.markdown(f"{status} <b>{sk}</b> — {get_skill_description(sk)}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        res = {}
        if missing:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🚀 Skills to Add & Resources")
            res = get_learning_resources(missing, resources_data, grouped=False)
            for sk, links in res.items():
                st.markdown(f"**{sk.title()}**:")
                for link in links:
                    st.markdown(f"- [🔗 Learn here]({link})")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.success("🎉 You already have all the required skills for your dream role!")

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🗘️ Short Roadmap Guidance")
        st.info("""
1. **Start** with free beginner tutorials (Docs, Coursera, etc.)  
2. **Build** small hands-on projects to apply the skills  
3. **Contribute** to GitHub or open-source if possible  
4. **Certify** yourself with relevant credentials (AWS, TensorFlow, etc.)  
5. **Showcase** your work on LinkedIn and GitHub regularly
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("📥 Download Skill Plan as PDF"):
            try:
                pdf_path = generate_skill_plan_pdf(
                    name=student_name if student_name else "Student",
                    dream_role=interested_role,
                    existing_skills=existing,
                    missing_skills=missing,
                    resources=res
                )
                with open(pdf_path, "rb") as f:
                    st.download_button("Download PDF", f, file_name=pdf_path.split("/")[-1])
            except Exception as e:
                st.error(f"⚠️ Could not generate PDF: {e}")


