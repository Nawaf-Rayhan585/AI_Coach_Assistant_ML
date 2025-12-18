# AI_Coach_Assistant_ML 🔥

**AI_Coach_Assistant_ML** is your personal **AI career coach** that helps you discover **jobs, roles, and skills** tailored to your experience, interests, and goals.  
Built with **Streamlit** and a **lightweight 1B-parameter model**, it runs smoothly on **any desktop** without heavy hardware or API keys.

Think of it as a friendly guide that sits on your computer and gives **career advice instantly**, whether you’re a student, beginner, or someone looking to upskill.

---

## Features ✨

- Suggests **career roles** based on your background and interests.
- Recommends **skills you should learn** to grow in your chosen field.
- Generates a **simple roadmap** for short-term and long-term growth.
- Fully offline — no API keys, no cloud required.
- Lightweight AI model ensures it runs fast even on normal desktops.
- **Interactive and easy-to-use UI** with Streamlit.

---

## Why This Project? 🤔

Most career guidance apps require cloud APIs, internet, or heavy models that are tough to run locally.  
**AI_Coach_Assistant_ML** solves this by using a **1B-parameter model** — small enough to run anywhere, but smart enough to give meaningful recommendations.  
It’s perfect for students, developers, or anyone exploring new career opportunities.

---

## Tech Stack 🛠

- **Streamlit** — For building a clean and interactive UI.
- **Hugging Face Transformers** — For running the AI model.
- **PyTorch / Accelerate** — Backend for fast AI inference.
- **1B-parameter text-to-text model** — Lightweight and efficient.

---

## Quick Start 🚀

1. Install dependencies:

```bash
pip install streamlit transformers torch accelerate
```

2. Intall Model (as your choice)

```bash
ollama pull llama3.2:1b
```

3. Run Project

```bash
streamlit run app.py
```
