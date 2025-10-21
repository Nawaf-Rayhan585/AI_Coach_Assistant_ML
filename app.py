import streamlit as st
from career_agent import CareerAgent

st.set_page_config(page_title="AI Career Coach (Ollama)", layout="centered")
st.title("🧠 AI Career Coach Agent — Llama 3.2 (3B)")
st.caption("Runs fully offline with Ollama — no API keys needed!")

agent = CareerAgent()

with st.form("career_form"):
    user_text = st.text_area(
        "Describe your background, skills, and goals:",
        height=150,
        placeholder="e.g. I know Python and JavaScript, want to become an ML Engineer..."
    )
    top_k = st.slider("How many role suggestions?", 1, 5, 3)
    submitted = st.form_submit_button("Get Recommendations")

if submitted:
    if not user_text.strip():
        st.warning("Please enter your background or interests.")
    else:
        with st.spinner("Finding best-fit roles..."):
            top_roles = agent.recommend_roles(user_text, k=top_k)

        st.subheader("Top matched roles:")
        for i, t in enumerate(top_roles, 1):
            job = t["job"]
            st.markdown(f"**{i}. {job['title']}** — Match `{t['score']:.3f}`")
            st.write(job["description"])
            st.divider()

        with st.spinner("Generating personalized learning roadmap using Llama3.2..."):
            answer = agent.generate_plan(user_text, top_roles)
        st.subheader("🎯 Personalized Career Roadmap")
        st.markdown(answer)
