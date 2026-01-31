import streamlit as st
from math import ceil

# ----------- PDF IMPORTS (ADDED) -----------
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CurricuForge",
    page_icon="📘",
    layout="wide"
)

st.title("📘 CurricuForge – AI Curriculum Generator")

# ---------------- COURSE LIST ----------------
COURSE_LIST = [
    "C Programming","C++ Programming","Java Programming","Python Programming",
    "Go Programming","Rust Programming","Kotlin Programming","Swift Programming",
    "Data Structures & Algorithms","Competitive Programming",
    "Frontend Web Development","Backend Web Development",
    "Full Stack Web Development","MERN Stack Development","MEAN Stack Development",
    "Django Web Development","Flask Web Development","Spring Boot Development",
    "REST API Development","GraphQL APIs",
    "Data Science with Python","Machine Learning Fundamentals",
    "Deep Learning","Artificial Intelligence","NLP","Computer Vision",
    "Big Data Analytics","Power BI","Tableau",
    "AWS Cloud Practitioner","Azure Fundamentals","Google Cloud Platform",
    "DevOps Engineering","Docker & Kubernetes","CI/CD Pipelines","Terraform",
    "Android App Development","iOS App Development","Flutter Development",
    "React Native Development",
    "Cyber Security Fundamentals","Ethical Hacking","Web Security",
    "Blockchain Development","Web3","IoT",
    "Manual Testing","Automation Testing","API Testing",
    "System Design","Agile & Scrum","Git & GitHub"
]

# ---------------- DOMAIN IDENTIFICATION ----------------
def detect_domain(course):
    c = course.lower()
    if any(k in c for k in ["python","java","c ","c++","go","rust","kotlin","swift"]):
        return "programming"
    if any(k in c for k in ["web","frontend","backend","mern","mean","django","flask","spring"]):
        return "web"
    if any(k in c for k in ["data","ml","ai","deep","nlp","vision"]):
        return "data_ai"
    if any(k in c for k in ["cloud","aws","azure","gcp","devops","docker","kubernetes","terraform"]):
        return "cloud"
    if any(k in c for k in ["android","ios","flutter","react native"]):
        return "mobile"
    if any(k in c for k in ["security","hacking","cyber"]):
        return "security"
    if any(k in c for k in ["testing","automation"]):
        return "testing"
    return "general"

# ---------------- REFERENCES ----------------
def generate_reference(domain):
    refs = {
        "programming": "https://www.geeksforgeeks.org",
        "web": "https://developer.mozilla.org",
        "data_ai": "https://scikit-learn.org",
        "cloud": "https://docs.aws.amazon.com",
        "mobile": "https://developer.android.com",
        "security": "https://owasp.org",
        "testing": "https://www.selenium.dev",
        "general": "https://www.coursera.org"
    }
    return refs.get(domain, refs["general"])

# ---------------- CONTENT GENERATOR ----------------
def generate_topics(course):
    domain = detect_domain(course)

    base = [
        "Introduction","Environment Setup","Core Concepts",
        "Syntax & Structure","Control Flow","Functions",
        "Data Handling","Error Handling","Best Practices",
        "Mini Project","Capstone Project","Interview Preparation"
    ]

    domain_map = {
        "programming": ["Variables","Loops","OOP","Memory","Files","Libraries"],
        "web": ["HTML","CSS","JavaScript","Frameworks","APIs","Deployment"],
        "data_ai": ["Data Cleaning","Statistics","Models","Evaluation","Deployment"],
        "cloud": ["Compute","Storage","Networking","CI/CD","Monitoring"],
        "mobile": ["UI Design","Navigation","Storage","API Integration","Publishing"],
        "security": ["Threats","Networking","Vulnerabilities","Pentesting","Defense"],
        "testing": ["Test Cases","Automation Tools","Frameworks","CI Integration"]
    }

    topics = []
    for t in base + domain_map.get(domain, []):
        topics.append({
            "title": f"{t} in {course}",
            "subtopics": [
                f"Concepts of {t}",
                f"Hands-on with {t}",
                f"Common mistakes in {t}"
            ],
            "ref": generate_reference(domain)
        })

    return topics

# ---------------- CURRICULUM BUILDER ----------------
def build_curriculum(topics, weeks, plan):
    curriculum = {}
    if plan == "Week-wise":
        per_week = ceil(len(topics) / weeks)
        index = 0
        for w in range(1, weeks + 1):
            curriculum[f"Week {w}"] = topics[index:index + per_week]
            index += per_week
    else:
        for i, topic in enumerate(topics, start=1):
            curriculum[f"Day {i}"] = [topic]
    return curriculum

# ---------------- INPUTS ----------------
course = st.selectbox("Select Course", COURSE_LIST)
duration = st.selectbox("Course Duration", ["2 Weeks","4 Weeks","6 Weeks"])
plan_type = st.radio("Curriculum Type", ["Week-wise","Day-wise"])
generate = st.button("🚀 Generate Curriculum")

# ---------------- OUTPUT ----------------
if generate:
    weeks = int(duration.split()[0])
    topics = generate_topics(course)
    curriculum = build_curriculum(topics, weeks, plan_type)

    st.success(f"Curriculum Generated for **{course}**")

    for period, items in curriculum.items():
        st.subheader(period)
        for item in items:
            st.markdown(f"### {item['title']}")
            for s in item["subtopics"]:
                st.write("•", s)
            st.markdown(f"🔗 Reference: {item['ref']}")

    # ----------- PDF GENERATION (ADDED AT LAST) -----------
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"<b>{course} Curriculum</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    for period, items in curriculum.items():
        elements.append(Paragraph(f"<b>{period}</b>", styles["Heading2"]))
        for item in items:
            elements.append(Paragraph(item["title"], styles["Heading3"]))
            for s in item["subtopics"]:
                elements.append(Paragraph(f"- {s}", styles["Normal"]))
            elements.append(Paragraph(f"Reference: {item['ref']}", styles["Normal"]))
            elements.append(Spacer(1, 8))

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf = SimpleDocTemplate(temp_pdf.name, pagesize=A4)
    pdf.build(elements)

    with open(temp_pdf.name, "rb") as f:
        st.download_button(
            "📥 Download Curriculum as PDF",
            f,
            file_name=f"{course.replace(' ','_')}_Curriculum.pdf",
            mime="application/pdf"
        )

st.caption("© CurricuForge | Auto-Generated Curriculum Engine")
