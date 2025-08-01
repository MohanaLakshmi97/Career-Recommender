from fpdf import FPDF
import re

# Helper to remove emojis and unsupported Unicode
def remove_emojis(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

# ----------------------------------------------------------------------
# 1️⃣ CAREER‑RECOMMENDER PDF
# ----------------------------------------------------------------------
def generate_pdf_report(name, top_result, missing_skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    pdf.cell(0, 10, "Career Recommendation Report", ln=True, align='C')

    pdf.ln(6)
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 8, remove_emojis(f"Name: {name}"), ln=True)
    pdf.cell(0, 8, remove_emojis(f"Top Career Role: {top_result[0]}"), ln=True)
    pdf.cell(0, 8, f"Match Score: {round(top_result[1]*100, 2)}%", ln=True)
    pdf.cell(0, 8, remove_emojis(f"Category: {top_result[2]}"), ln=True)
    pdf.cell(0, 8, f"Average Salary: ₹{top_result[3]:,.0f}", ln=True)

    pdf.ln(4)
    if missing_skills:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Missing Skills:", ln=True)
        pdf.set_font("Helvetica", size=12)
        for skill in missing_skills:
            pdf.cell(0, 8, remove_emojis(f"- {skill}"), ln=True)
    else:
        pdf.cell(0, 8, remove_emojis("You have all the required skills!"), ln=True)

    pdf.ln(8)
    pdf.set_font("Helvetica", 'I', 12)
    pdf.multi_cell(0, 8, remove_emojis(
        "🌟 Believe in yourself and keep learning. "
        "Your dream career is just one step away!"
    ))

    safe_name = re.sub(r'\W+', '_', name)
    file_path = f"/mnt/data/{safe_name}_career_report.pdf"
    pdf.output(file_path)
    return file_path


# ----------------------------------------------------------------------
# 2️⃣ SKILL‑PLANNER PDF
# ----------------------------------------------------------------------
def generate_skill_plan_pdf(name, dream_role, existing_skills, missing_skills, resources):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Skill Planner Roadmap", ln=True, align="C")

    pdf.set_font("Helvetica", "", 12)
    pdf.ln(4)
    pdf.cell(0, 8, remove_emojis(f"Name: {name}"), ln=True)
    pdf.cell(0, 8, remove_emojis(f"Dream Role: {dream_role}"), ln=True)

    # Existing / missing skills
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Skill Status:", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, remove_emojis(f"✅ Existing Skills: {', '.join(existing_skills) if existing_skills else 'None'}"))
    pdf.multi_cell(0, 8, remove_emojis(f"❌ Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}"))

    # Learning resources
    if resources:
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, "Learning Resources:", ln=True)
        pdf.set_font("Helvetica", "", 12)
        for skill, links in resources.items():
            pdf.multi_cell(0, 8, remove_emojis(f"{skill.title()}:"))
            for link in links:
                pdf.set_text_color(0, 0, 255)
                pdf.cell(0, 8, f"  {link}", ln=True, link=link)
                pdf.set_text_color(0, 0, 0)

    # Roadmap tips
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 11)
    pdf.multi_cell(0, 8,
        "Roadmap Tips:\n"
        "• Start with beginner tutorials.\n"
        "• Build mini‑projects to apply each skill.\n"
        "• Contribute to GitHub / open‑source.\n"
        "• Pursue relevant certifications.\n"
        "• Showcase progress on LinkedIn and GitHub."
    )

    # Motivational quote
    pdf.ln(6)
    pdf.multi_cell(0, 8, remove_emojis("“Believe you can and you're halfway there.”"))

    safe_name = re.sub(r'\W+', '_', name)
    path = f"/mnt/data/{safe_name}_skill_plan.pdf"
    pdf.output(path)
    return path
