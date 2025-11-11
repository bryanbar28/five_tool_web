import streamlit as st
import os

# -------------------------------
# 🌐 Language Selector
# -------------------------------
st.set_page_config(page_title="LC Innovation Platform", layout="wide")

LANGUAGES = {
    "English": "en",
    "Español": "es",
    "Deutsch": "de",
    "日本語": "ja",
    "हिन्दी": "hi",
    "Français": "fr",
    "العربية": "ar"
}
language = st.selectbox("🌍 Select Language", options=list(LANGUAGES.keys()), index=0)
st.session_state["language"] = LANGUAGES[language]
# -------------------------------
# 🗣️ Translation System
# -------------------------------
TRANSLATIONS = {
    "en": {
        "select_language": "🌍 Select Language",
        "choose_page": "📂 Choose a Page",
        "subscription_required": "This page requires a subscription.",
        "generate_profile": "🎯 Generate Profile",
        "additional_notes": "📝 Additional Notes"
    },
    "es": {
        "select_language": "🌍 Seleccionar idioma",
        "choose_page": "📂 Elegir página",
        "subscription_required": "Esta página requiere una suscripción.",
        "generate_profile": "🎯 Generar perfil",
        "additional_notes": "📝 Notas adicionales"
    }
    # You can expand this with more languages later
}

def t(key):
    lang = st.session_state.get("language", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


# -------------------------------
# 🔐 Pricing Access Control
# -------------------------------
PAID_PAGES = {
    "Page 9: M&A Intelligence": 3.99,
    "Page 10: Finding the Right Fit": 3.99,
    "Page 11: Your Ego": 3.99,
    "Page 12: Repository": 9.99
}


def is_unlocked(module_name):
    return st.session_state.get(f"unlocked_{module_name}", False)

def unlock_module(module_name, price):
    if st.button(f"🔓 Unlock {module_name} (${price}/mo)"):
        st.session_state[f"unlocked_{module_name}"] = True
        st.success(f"{module_name} unlocked!")

# -------------------------------
# 📚 Module Navigation
# -------------------------------
PAGES = [
    "Page 1: Behavioral Intelligence",
    "Page 2: Job Description Generator",
    "Page 3: Performance Review Generator",
    "Page 4: Behavior Under Pressure Grid",
    "Page 5: Behavioral Calibration Grid",
    "Page 6: Toxicity in the Workplace",
    "Page 7: Leadership Eligibility",
    "Page 8: SWOT 2.0",
    "Page 9: M&A Intelligence",
    "Page 10: Finding the Right Fit",
    "Page 11: Your Ego",
    "Page 12: Repository"
]

selected_page = st.sidebar.selectbox("📂 Choose a Page", PAGES)

# -------------------------------
# 🧩 Module Logic
# -------------------------------
def render_module_1():
    st.title("🧠 Behavioral Intelligence App")
    st.text_input("e.g. Find job review for certain industries")
    st.text_input("i.e. Generate generic performance review for certain industry")

def render_module_2():
    st.title("📄 Job Description Generator")
    st.text_area("Paste job description or request one by role")

def render_module_3():
    st.title("📋 Performance Review Generator")
    st.text_area("Paste review or request one by role")

def render_module_4():
    st.title("⚾ Behavior Under Pressure Grid")
    st.image("images/module4_behavior_grid.png")
    st.text_area("📝 Additional Notes")
    st.button("🎯 Generate Profile")

def render_module_5():
    st.title("🧠 Behavioral Calibration Grid")
    st.image("images/module5_calibration_grid.png")
    st.text_area("📝 Additional Notes")
    st.button("🎯 Generate Profile")

def render_module_6():
    st.title("☢️ Toxicity in the Workplace")
    st.image("images/module6_toxicity_scale.png")
    st.image("images/module6_toxicity_scoring.png")
    st.text_area("🧠 AI Chat: Ask about Padilla, Hogan, Kaiser, Machiavellianism")
    st.text_area("📝 Additional Notes")
    st.button("🎯 Generate Profile")

def render_module_7():
    st.title("🏆 Leadership Eligibility")
    st.image("images/module7_calibration_grid.png")
    st.image("images/module7_eligibility_filter.png")
    st.image("images/module7_scoring_scale.png")
    st.image("images/module7_diagnostic_rubric.png")
    st.image("images/module7_outcomes.png")

def render_module_8():
    st.title("📊 SWOT 2.0 Strategic Framework")
    st.markdown("Designed by Bryan Barrera & Microsoft Copilot")
    st.text_area("📝 Additional Notes and Input")
    st.text_area("🧠 AI Chat: Ask for SWOT templates, Lean tools, Fishbone diagrams")
    st.button("🎯 Generate SWOT")

def render_module_9():
    st.title("🏢 M&A Intelligence (Premium)")
    st.warning("This module requires a $3.99/mo subscription.")
    st.file_uploader("📁 Upload Resumes", accept_multiple_files=True)
    st.file_uploader("📄 Upload Job Descriptions", accept_multiple_files=True)
    st.file_uploader("📋 Upload Performance Reviews", accept_multiple_files=True)
    st.file_uploader("📁 Upload Training & Education Records", accept_multiple_files=True)
    st.text_area("🏢 Branch Data: Name, Location, Benefits")
    st.button("📊 Generate Analysis")

def render_module_10():
    st.title("📘 Finding the Right Fit (Book)")
    st.warning("This book requires a $3.99/mo subscription.")
    st.markdown("Coming Soon: AI-assisted workbook experience")

def render_module_11():
    st.title("📕 Your Ego: The Real Reason Your Business is Failing")
    st.warning("This book requires a $3.99/mo subscription.")
    st.markdown("Coming Soon: Interactive reading experience")

def render_module_12():
    st.title("🗂️ Repository (Premium)")
    st.warning("This module requires a $9.99/mo subscription.")
    st.file_uploader("📁 Upload any file to store")
    st.text_area("📝 Save generated profiles or notes")
    st.button("💾 Save to Repository")

# -------------------------------
# 🚀 Module Execution
# -------------------------------
PAGE_RENDERERS = {
    PAGES[0]: render_module_1,
    PAGES[1]: render_module_2,
    PAGES[2]: render_module_3,
    PAGES[3]: render_module_4,
    PAGES[4]: render_module_5,
    PAGES[5]: render_module_6,
    PAGES[6]: render_module_7,
    PAGES[7]: render_module_8,
    PAGES[8]: render_module_9,
    PAGES[9]: render_module_10,
    PAGES[10]: render_module_11,
    PAGES[11]: render_module_12
}

if selected_page in PAID_PAGES:
    if is_unlocked(selected_page):
        PAGE_RENDERERS[selected_page]()
    else:
        unlock_page(selected_page, PAID_PAGES[selected_page])
else:
    PAGE_RENDERERS[selected_page]()


