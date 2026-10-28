import os
from datetime import datetime

import pandas as pd
import streamlit as st


NAME = "Josh Gabriel E. de la Cerna"
SECTION = "F1"            
PROGRAM = "BS Computer Science"
YEAR = "3rd Year"
EMAIL = "joshgabrieldelacernz@gmail.com"
GITHUB = "https://github.com/juicegebrel"
PHOTO_PATH = "josh.jpg"         

SKILLS = {                       
    "Python": 70,
    "Streamlit": 60,
    "SQL": 70,
    "HTML/CSS": 65,
    "Data Analysis": 75,
    "Communication": 70,
    "C++" : 70,
    "Math" : 80,
}

PROJECTS = [
    {
        "title": "Project One: CebuHeritage",
        "role": "Solo developer",
        "tools": ["C#", "Blazor", "Tailwind"],
        "outcome": "Educational website about the cities and municipalities of Cebu.",
        "link": "https://github.com/juicegebrel/CebuHeritage",
        "type": "Web", 
    },
    {
        "title": "Project Two: Wildcats Price Checker",
        "role": "Back-End developer (team of 2)",
        "tools": ["PHP", "SQL", "Xampp"],
        "outcome": "Shows prices of canteen foods in the convenience of your phone.",
        "link": "https://github.com/Kianbel/WildcatsPriceChecker",
        "type": "Web",
    },
    {
        "title": "Project Three: Tn-spector",
        "role": "Front-End developer (team of 5)",
        "tools": ["Java", "JavaFX", "JDBC"],
        "outcome": "Calculates runtime of algorithms. Useful in design and analysis of algorithms.",
        "link": "https://github.com/Kianbel/Tn-spector",
        "type": "App",
    },
]

# ---------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(
    page_title=f"{NAME} | Portfolio",
    page_icon="👋",
    layout="wide",
)

# Session state: remember submitted messages and a visit counter
if "messages" not in st.session_state:
    st.session_state.messages = []
if "visits" not in st.session_state:
    st.session_state.visits = 0
st.session_state.visits += 1

# ---------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------
with st.sidebar:
    st.header("Navigate")
    st.write(f"**{NAME}**")
    st.caption(f"{PROGRAM} · {YEAR} · {SECTION}")
    show_projects = st.checkbox("Show projects", value=True)
    show_contact = st.checkbox("Show contact form", value=True)
    st.divider()
    st.write("Links")
    st.markdown(f"- [GitHub]({GITHUB})\n- [Email](mailto:{EMAIL})")
    st.caption(f"Page views this session: {st.session_state.visits}")

# ---------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------
st.title(NAME)
st.markdown(f"##### {PROGRAM} · {YEAR} · **{SECTION}**")
st.divider()

# ---------------------------------------------------------------
# ABOUT ME
# ---------------------------------------------------------------
st.header("About Me")
col_photo, col_bio = st.columns([1, 2], gap="medium")

with col_photo:
    if os.path.exists(PHOTO_PATH):
        st.image(PHOTO_PATH, caption=NAME, use_container_width=True)
    else:
        st.info("📷 PHOTO PLACEHOLDER")

with col_bio:
    st.write(
        f"Hi, I'm {NAME}, a {YEAR.lower()} {PROGRAM} student ({SECTION}). "
        "I strive to become software developer one project at a time. "
        "I love to solve problems and to learn more about technology."
    )
    m1, m2, m3 = st.columns(3)
    m1.metric("Projects", len(PROJECTS))
    m2.metric("Skills listed", len(SKILLS))
    m3.metric("Top skill", max(SKILLS, key=SKILLS.get), f"{max(SKILLS.values())}/100")

st.divider()

# ---------------------------------------------------------------
# AUTOBIOGRAPHY 
# ---------------------------------------------------------------
st.header("Autobiography")
tab_bg, tab_edu, tab_int, tab_mile = st.tabs(
    ["Background", "Education", "Interests", "Milestones"]
)

with tab_bg:
    st.write(
        "I grew up in Basak Pardo, Cebu City. I like to solve problems like math and puzzles. "
        "This trait is what made me choose to become a computer science student. "
        "Computer science is by no means easy but I manage and have come to appreciate learning more about it. "
    )

with tab_edu:
    st.markdown(
        "- **Senior High School:** Cebu Institute of Technology - University, STEM, 2022-2024\n"
        "- **College:** Cebu Institute of Technology - University, BS in Computer Science, 2024-Now\n"
    )

with tab_int:
    interests = st.multiselect(
        "Pick the interests to display",
        ["Coding", "Music", "Basketball", "Photography", "Gaming", "Cooking", "Reading"],
        default=["Coding", "Music", "Reading"],
    )
    st.write("I enjoy: " + (", ".join(interests) if interests else "(nothing selected)"))

with tab_mile:
    milestones = pd.DataFrame(
        {
            "Year": [2022, 2023, 2024, 2026],
            "Milestone": [
                "Graduated junior high school",
                "Turned 18 years old",
                "Started college (BSCS)",
                "Built my first Streamlit site",
            ],
        }
    )
    st.table(milestones)

st.divider()

# ---------------------------------------------------------------
# SKILLS
# ---------------------------------------------------------------
st.header("Skills")
skills_df = pd.DataFrame({"Skill": list(SKILLS.keys()), "Level": list(SKILLS.values())})

left, right = st.columns(2, gap="large")

with left:
    st.write(
        "These are my own self-ratings out of 100. Use the slider to hide skills "
        "below a minimum level."
    )
    min_level = st.slider("Minimum skill level", 0, 100, 50, step=5)
    sort_by = st.selectbox("Sort by", ["Level (high to low)", "Skill name (A-Z)"])
    view = skills_df[skills_df["Level"] >= min_level]
    if sort_by.startswith("Level"):
        view = view.sort_values("Level", ascending=False)
    else:
        view = view.sort_values("Skill")
    st.dataframe(view, hide_index=True, use_container_width=True)

with right:
    chart_type = st.radio("Chart type", ["Bar", "Line"], horizontal=True)
    chart_data = view.set_index("Skill")
    if chart_data.empty:
        st.warning("No skills match that minimum level.")
    elif chart_type == "Bar":
        st.bar_chart(chart_data)
    else:
        st.line_chart(chart_data)

st.divider()

# ---------------------------------------------------------------
# PROJECTS
# ---------------------------------------------------------------
if show_projects:
    st.header("Projects")
    project_type = st.selectbox("Filter by type", ["All"] + sorted({p["type"] for p in PROJECTS}))
    shown = [p for p in PROJECTS if project_type == "All" or p["type"] == project_type]

    cols = st.columns(len(shown)) if shown else []
    for col, p in zip(cols, shown):
        with col:
            with st.container(border=True):
                st.subheader(p["title"])
                st.write(f"**Role:** {p['role']}")
                st.write(f"**Tools:** {', '.join(p['tools'])}")
                st.write(f"**Outcome:** {p['outcome']}")
                st.link_button("View project", p["link"])
    st.divider()

# ---------------------------------------------------------------
# CONTACT / FEEDBACK FORM
# ---------------------------------------------------------------
if show_contact:
    st.header("Contact & Feedback")
    with st.form("contact_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        sender = c1.text_input("Your name")
        sender_email = c2.text_input("Your email")
        topic = st.selectbox("Topic", ["Feedback", "Collaboration", "Question", "Other"])
        message = st.text_area("Message", height=120)
        submitted = st.form_submit_button("Send")

    if submitted:
        if not sender.strip() or not message.strip():
            st.error("Please enter your name and a message.")
        else:
            st.session_state.messages.append(
                {
                    "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Name": sender,
                    "Email": sender_email,
                    "Topic": topic,
                    "Message": message,
                }
            )
            st.success(f"Thanks, {sender}! Your {topic.lower()} was received.")
            st.balloons()

    if st.session_state.messages:
        with st.expander(f"Messages received this session ({len(st.session_state.messages)})"):
            msgs = pd.DataFrame(st.session_state.messages)
            st.dataframe(msgs, hide_index=True, use_container_width=True)
            st.download_button(
                "Download messages (CSV)",
                msgs.to_csv(index=False).encode("utf-8"),
                file_name="messages.csv",
                mime="text/csv",
            )

# ---------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------
st.divider()
st.caption(f"© {datetime.now().year} {NAME} · {SECTION}")
